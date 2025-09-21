import sys
from sitemap import process_sitemap
from scraping import load_sitemap_urls, scrape_produto, save_produto, driver


def main():
    # --- 1. Processar sitemap(s) ---
    sitemaps = [
        "https://www.kabum.com.br/sitemap/hardware.xml",
    ]

    try:
        for url in sitemaps:
            process_sitemap(url)
    except RuntimeError as e:
        print(f"Erro crítico no processamento do sitemap: {e}")
        print("Encerrando aplicação.")
        exit(1)  # código de erro no SO
        sys.exit(1)  # código de erro no SO

    # --- 2. Carregar URLs de produtos ---
    urls = load_sitemap_urls()
    if not urls:
        print("Nenhuma URL encontrada. Encerrando.")
        return

    # --- 3. Scraping de cada produto ---
    for url in urls:
        print(f"\nExtraindo: {url}")
        try:
            dados = scrape_produto(url)
            save_produto(dados)
        except Exception as e:
            print(f"Erro ao extrair {url}: {e}")

    driver.quit()


if __name__ == "__main__":
    main()
