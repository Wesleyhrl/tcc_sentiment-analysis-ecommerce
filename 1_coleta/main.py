import sys
import time
from sitemap import process_sitemap
from scraping import load_sitemap_urls, scrape_produto, save_produto, init_driver, close_driver
from logger_config import setup_logger

logger = setup_logger()

def main():
    inicio = time.time()
    logger.info("==== Início da execução do scraping ====")

    # Contadores
    total_urls = 0
    total_erros = 0
    processadas = 0

    # --- 1. Processar sitemap(s) ---
    sitemaps = [
        "https://www.kabum.com.br/sitemap/hardware.xml",
    ]
    
    try:
        for url in sitemaps:
            process_sitemap(url)
    except RuntimeError as e:
        logger.error(f"Falha no processamento do sitemap: {e}")
        print("Encerrando aplicação.")
        sys.exit(1)
    
    logger.info(f"Sitemaps processados: {sitemaps}")

    # --- 2. Carregar URLs de produtos ---
    try:
        urls = load_sitemap_urls()
    except Exception as e:
        logger.critical(f"Falha ao carregar URLs do MongoDB: {e}")
        sys.exit(1)
    if not urls:
        logger.error("Nenhuma URL encontrada. Encerrando...")
        return

    total_urls = len(urls)
    logger.info(f"Total de URLs de produto carregadas: {total_urls}")

    # --- 3. Scraping de cada produto ---
    init_driver()
    for url in urls:
        partes = url.split('/')
        url_limpa = '/'.join(partes[:5])
        logger.info(f"Extraindo: {url_limpa}")

        tentativas = 0
        max_tentativas = 3

        while tentativas < max_tentativas:
            try:
                dados = scrape_produto(url)
                save_produto(dados)
                processadas += 1
                break
            except Exception as e:
                tentativas += 1
                total_erros += 1
                logger.warning(f"Falha ao extrair {url} (tentativa {tentativas}/{max_tentativas}): {e}")
                if tentativas == 0:
                    logger.info("Reiniciando o driver...")
                    close_driver()
                    init_driver()
                if tentativas == max_tentativas:
                    logger.error(f"Produto {url} ignorado após {max_tentativas} tentativas.")

    close_driver()

    # --- 4. Resumo final ---
    fim = time.time()
    duracao = fim - inicio
    minutos = duracao / 60

    logger.info("==== RESUMO FINAL ====")
    logger.info(f"Tempo total: {minutos:.2f} minutos")
    logger.info(f"Total de URLs carregadas: {total_urls}")
    logger.info(f"Total processadas com sucesso: {processadas}")
    logger.info(f"Total de erros: {total_erros}")
    logger.info("=======================")


if __name__ == "__main__":
    main()
