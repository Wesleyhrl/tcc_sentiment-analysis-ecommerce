import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pymongo import MongoClient
from selenium.common.exceptions import  WebDriverException
from pymongo.errors import PyMongoError


# CONFIGURAÇÕES SELENIUM
options = webdriver.ChromeOptions()
options.add_argument("--headless=new")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-notifications")
options.add_argument("--blink-settings=imagesEnabled=false")

def init_driver():
    global driver, wait
    driver = webdriver.Chrome(options=options)
    time.sleep(2)  # Espera o driver iniciar
    wait = WebDriverWait(driver, 15)


def close_driver():
    global driver
    driver.quit()

# CONEXÃO MONGODB
client = MongoClient("mongodb://localhost:27017/")
db = client["kabum_scraping"]
collection = db["produtos"]
sitemaps_collection = db["sitemaps"]

def pausa(min_seg=1, max_seg=4):
    """Pausa aleatória entre min_seg e max_seg segundos"""
    tempo = random.uniform(min_seg, max_seg)
    time.sleep(tempo)

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
    try:
        driver.get(url)
    except WebDriverException as e:
        raise RuntimeError(f"Falha ao carregar página {url}: {e}")
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
    
    try:
        review_section = wait.until(EC.presence_of_element_located((By.ID, "reviewsSection")))
        nota_review = review_section.find_element(By.CSS_SELECTOR, "span.sc-781b7e7f-1.hdvIZL").text.strip()
        dados_produto["produto"]["classificacao"] = float(nota_review)
    except:
        tech_info = None

    # --- Avaliações ---
    pagina_atual = 1
    review_id = 1

    avaliacoes_unicas = set()  #evita avaliações duplicadas

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

            # chave única para evitar duplicatas
            chave = f"{autor}-{data}-{titulo_avaliacao}-{comentario}"
            # verifica se já existe essa avaliação antes de adicionar ao produto
            if chave not in avaliacoes_unicas:
                # adiciona chave ao conjunto de avaliações únicas
                avaliacoes_unicas.add(chave)

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
            #salva primeiro comentário da página atual
            try:
                first_comment_before = review_containers[0].text.strip()
            except:
                first_comment_before = None
            # Clica na próxima página
            driver.execute_script("arguments[0].click();", next_button.find_element(By.CSS_SELECTOR, "a.nextLink"))
            # Espera a página carregar verificando se o primeiro comentário mudou
            wait.until(
                lambda d: (
                    d.find_elements(By.CSS_SELECTOR, "div.sc-9e789c55-0.grUenq")
                    and d.find_elements(By.CSS_SELECTOR, "div.sc-9e789c55-0.grUenq")[0].text.strip() != first_comment_before
                )
            )
       


            pausa(2, 4) # Pausa entre páginas
            pagina_atual += 1
        except:
            break

    dados_produto["produto"]["total_avaliacoes_coletadas"] = len(dados_produto["avaliacoes"])
    dados_produto["produto"]["url"] = url
    dados_produto["produto"]["data_extracao"] = time.strftime("%Y-%m-%d %H:%M:%S")

    pausa(3, 6) # Pausa entre produtos

    return dados_produto


def load_sitemap_urls():
    """Carrega URLs de produto armazenadas no MongoDB, ignorando as já processadas"""
    documentos_sitemaps = sitemaps_collection.find()
    urls_produto = []

    for doc in documentos_sitemaps:
        urls = [item["url"] for item in doc["urls"] if "/produto/" in item["url"]]
        urls_produto.extend(urls)

    if not urls_produto:
        return []

    # Buscar apenas URLs que ainda não estão na coleção de produtos
    urls_processadas = collection.distinct("produto.url")
    urls_faltantes = list(set(urls_produto) - set(urls_processadas))

    return urls_faltantes


def save_produto(dados: dict):
    """Salva/atualiza produto no MongoDB"""
    try:
        codigo_produto = dados["produto"]["codigo"]
        if not codigo_produto:
            raise ValueError("Produto sem código identificado, não pode salvar.")

        filtro = {"_id": codigo_produto}
        novo_documento = {"$set": dados}
        resultado = collection.update_one(filtro, novo_documento, upsert=True)

        #if resultado.upserted_id:
        #   print(f"NOVO: Produto inserido com o ID {resultado.upserted_id}")
        #else:
        #   print(f"ATUALIZADO: Produto {codigo_produto} atualizado.")
    except PyMongoError as e:
        raise Exception(f"[ERRO MONGO] Falha ao salvar produto {dados.get('produto', {}).get('titulo')}: {e}")
    except Exception as e:
        raise Exception((f"[ERRO] Falha inesperada ao salvar produto: {e}"))
