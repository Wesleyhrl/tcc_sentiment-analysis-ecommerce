import sys
from sitemap import process_sitemap
from scraping import load_sitemap_urls, scrape_produto, save_produto, init_driver, close_driver
from logger_config import setup_logger
from resume import iniciar_estatisticas, atualizar_estatisticas
logger = setup_logger()

def main():
    logger.info("==== Início da execução do scraping ====")
    iniciar_estatisticas()
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
    atualizar_estatisticas(urls_carregadas=total_urls)

    # --- 3. Scraping de cada produto ---
    init_driver()
    for url in urls:
        logger.info(f"Extraindo: {url}")

        tentativas = 0
        max_tentativas = 3

        while tentativas < max_tentativas:
            try:
                dados = scrape_produto(url)
                save_produto(dados)
                logger.info(f"Produto salvo.")
                processadas += 1
                atualizar_estatisticas(processados=processadas)
                break
            except Exception as e:
                tentativas += 1
                total_erros += 1
                atualizar_estatisticas(erros=total_erros)
                logger.warning(f"Falha ao extrair {url} (tentativa {tentativas}/{max_tentativas}): {e}")
                if tentativas < max_tentativas:
                    logger.info("Reiniciando o driver...")
                    close_driver()
                    init_driver()
                if tentativas == max_tentativas:
                    logger.error(f"Produto {url} ignorado após {max_tentativas} tentativas.")

    close_driver()
    logger.info("==== Fim da execução do scraping ====")


if __name__ == "__main__":
    main()
