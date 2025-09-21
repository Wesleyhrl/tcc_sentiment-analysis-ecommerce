import sys
from sitemap import process_sitemap
from scraping import load_sitemap_urls, scrape_produto, save_produto, init_driver, close_driver


def main():
    # --- 1. Processar sitemap(s) ---
    sitemaps = [
        "https://www.kabum.com.br/sitemap/hardware.xml",
    ]

    try:
        for url in sitemaps:
            process_sitemap(url)
    except RuntimeError as e:
        print(f"[ERRO CRÍTICO] Falha no processamento do sitemap: {e}")
        print("Encerrando aplicação.")
        sys.exit(1)

    # --- 2. Carregar URLs de produtos ---
    try:
        urls = load_sitemap_urls()
    except Exception as e:
        print(f"[ERRO CRÍTICO] Falha ao carregar URLs do MongoDB: {e}")
        sys.exit(1)
    if not urls:
        print("[ERRO] Nenhuma URL encontrada. Encerrando...")
        return

    # --- 3. Scraping de cada produto ---
    init_driver()
    for url in urls[:2]:
        print(f"\nExtraindo: {url}")
        tentativas = 0
        max_tentativas =  3

        while tentativas < max_tentativas:
            try:
                dados = scrape_produto(url)
                save_produto(dados)
                break  # sucesso, sai do loop de tentativas
            except Exception as e:
                tentativas += 1
                print(f"[ERRO] Falha ao extrair {url} (tentativa {tentativas}/{max_tentativas}): {e}")
                if(tentativas == 0):
                    print("Reiniciando o driver...")
                    close_driver()
                    init_driver()
                if tentativas == max_tentativas:
                    print(f"[FALHA] Produto {url} ignorado após {max_tentativas} tentativas.")
    close_driver()


if __name__ == "__main__":
    main()
