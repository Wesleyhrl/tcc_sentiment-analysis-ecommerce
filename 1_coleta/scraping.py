import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pymongo import MongoClient


# CONFIGURAÇÕES SELENIUM
options = webdriver.ChromeOptions()
options.add_argument("--headless=new")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-notifications")

driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 15)


# CONEXÃO MONGODB
client = MongoClient("mongodb://localhost:27017/")
db = client["kabum_scraping"]
collection = db["produtos"]
sitemaps_collection = db["sitemaps"]


def extract_brand_model(text: str, dados_produto: dict):
    """Extrai marca e modelo do texto técnico"""
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    for line in lines:
        item_text = line.lstrip('- ').strip()
        if item_text.startswith("Marca:"):
            dados_produto["produto"]["marca"] = item_text.replace("Marca:", "").strip()
        elif item_text.startswith("Modelo:"):
            dados_produto["produto"]["modelo"] = item_text.replace("Modelo:", "").strip()


def scrape_produto(url: str):
    """Extrai dados de um único produto"""
    driver.get(url)
    dados_produto = {"produto": {}, "avaliacoes": []}

    # --- Produto ---
    try:
        titulo = wait.until(EC.presence_of_element_located(
            (By.XPATH, '//*[@id="main-content"]/div[1]/div[1]/div[1]/div[2]/div/h1'))
        ).text.strip()
        dados_produto["produto"]["titulo"] = titulo
    except:
        dados_produto["produto"]["titulo"] = None

    try:
        breadcrumb_nav = wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, "nav[aria-label='Breadcrumb']"))
        )
        breadcrumb_items = breadcrumb_nav.find_elements(By.CSS_SELECTOR, "ol li")
        dados_produto["produto"]["localizacao"] = breadcrumb_items[-2].find_element(
            By.TAG_NAME, "a").get_attribute("href")
        dados_produto["produto"]["codigo"] = breadcrumb_items[-1].text.replace(
            "Código", "").strip()
    except:
        dados_produto["produto"]["localizacao"] = None
        dados_produto["produto"]["codigo"] = None

    try:
        loja = wait.until(EC.presence_of_element_located(
            (By.XPATH, '//*[@id="main-content"]/div[1]/div[1]/div[1]/div[2]/div/div[3]'))
        ).text.replace("\n", "").strip()
        dados_produto["produto"]["loja"] = loja
    except:
        dados_produto["produto"]["loja"] = None

    try:
        descricao_section = wait.until(EC.presence_of_element_located((By.ID, "descriptionSection")))
        descricao = descricao_section.find_element(By.CSS_SELECTOR, "div#description").text.strip()
        dados_produto["produto"]["descricao"] = descricao
    except:
        dados_produto["produto"]["descricao"] = None

    try:
        tech_info_section = wait.until(EC.presence_of_element_located((By.ID, "technicalInfoSection")))
        tech_info = tech_info_section.find_element(By.CSS_SELECTOR, "div").text.strip()
        extract_brand_model(tech_info, dados_produto)
        dados_produto["produto"]["informacoes_tecnicas"] = tech_info
    except:
        dados_produto["produto"]["informacoes_tecnicas"] = None

    # --- Avaliações ---
    pagina_atual = 1
    review_id = 1
    while True:
        try:
            review_containers = wait.until(EC.presence_of_all_elements_located(
                (By.CSS_SELECTOR, "div.sc-9e789c55-0.grUenq"))
            )
        except:
            break

        for container in review_containers:
            try:
                autor = container.find_element(By.CSS_SELECTOR, "span.sc-d5f48f0e-1.heSJqR").text.strip()
            except:
                autor = "Anônimo"

            try:
                nota = container.find_element(By.CSS_SELECTOR, "div.ratingStarsContainer").get_attribute("aria-label")
                nota = nota.split(":")[1].strip() if nota else None
            except:
                nota = None

            try:
                data = container.find_element(By.CSS_SELECTOR, "span.sc-d5f48f0e-2.brbMqG").text.strip()
                data = data.replace("Avaliado em ", "")
            except:
                data = None

            try:
                comentario = container.find_element(By.CSS_SELECTOR, "span.sc-9e789c55-8.eUnvhx").text.strip()
            except:
                comentario = ""

            try:
                titulo_avaliacao = container.find_element(By.CSS_SELECTOR, "h5.sc-d5f48f0e-3.gByuuW").text.strip()
            except:
                titulo_avaliacao = ""

            dados_produto["avaliacoes"].append({
                "id": review_id,
                "pagina": pagina_atual,
                "autor": autor,
                "nota": nota,
                "data": data,
                "titulo": titulo_avaliacao,
                "comentario": comentario
            })
            review_id += 1

        try:
            next_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "li.next")))
            if "disabled" in next_button.get_attribute("class"):
                break
            driver.execute_script("arguments[0].click();", next_button.find_element(By.CSS_SELECTOR, "a.nextLink"))
            time.sleep(3)
            pagina_atual += 1
        except:
            break

    dados_produto["produto"]["total_avaliacoes_coletadas"] = len(dados_produto["avaliacoes"])
    dados_produto["produto"]["url"] = url
    dados_produto["produto"]["data_extracao"] = time.strftime("%Y-%m-%d %H:%M:%S")
    return dados_produto


def load_sitemap_urls():
    """Carrega URLs de produto armazenadas no MongoDB"""
    documentos_sitemaps = sitemaps_collection.find()
    total_urls, urls_produto = 0, []

    for doc in documentos_sitemaps:
        origem = doc["sitemap"]["origem"]
        urls = [item["url"] for item in doc["urls"] if "/produto/" in item["url"]]
        print(f"Sitemap '{origem}' -> {len(urls)} URLs de produto")
        urls_produto.extend(urls)
        total_urls += len(urls)

    if not urls_produto:
        print("Nenhuma URL encontrada. Execute primeiro o sitemap.py")
        return []

    print(f"\nTotal geral de URLs de produto: {total_urls}")
    return urls_produto


def save_produto(dados: dict):
    """Salva/atualiza produto no MongoDB"""
    codigo_produto = dados["produto"]["codigo"]
    filtro = {"_id": codigo_produto}
    novo_documento = {"$set": dados}
    resultado = collection.update_one(filtro, novo_documento, upsert=True)

    if resultado.upserted_id:
        print(f"NOVO: Produto inserido com o ID {resultado.upserted_id}")
    else:
        print(f"ATUALIZADO: Produto {codigo_produto} atualizado.")
