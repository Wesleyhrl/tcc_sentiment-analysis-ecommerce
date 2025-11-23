import time
import random
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pymongo import MongoClient
from selenium.common.exceptions import  WebDriverException
from selenium.common.exceptions import TimeoutException
from pymongo.errors import PyMongoError


# CONFIGURAÇÕES SELENIUM
options = webdriver.ChromeOptions()
options.add_argument("--headless=new")
options.add_argument("--window-size=1920,1080")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-notifications")
options.add_argument("--blink-settings=imagesEnabled=false")

def init_driver():
    global driver, wait
    driver = webdriver.Chrome(options=options)
    time.sleep(2)  # Espera o driver iniciar
    wait = WebDriverWait(driver, 20)


def close_driver():
    global driver
    driver.quit()
    time.sleep(1)

# CONEXÃO MONGODB
client = MongoClient("mongodb://localhost:27017/")
db = client["kabum_scraping"]
collection = db["produtos"]
sitemaps_collection = db["sitemaps"]

def scroll_driver(element):
    """Rola a página até o elemento especificado"""

    ActionChains(driver)\
        .scroll_to_element(element)\
        .perform()
def scroll_to_bottom():
    """Rola a página até o final"""
    # Obtém a altura total da página
    total_height = driver.execute_script("return document.body.scrollHeight")
    
    # Rola até o final usando ActionChains
    ActionChains(driver)\
        .scroll_by_amount(0, total_height)\
        .perform()

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
    # Rola para garantir carregamento de lazy load
    scroll_to_bottom()

    # --- Produto ---
    try:
        titulo = wait.until(EC.presence_of_element_located(
            (By.XPATH, '//*[@id="main-content"]/div[1]/div[1]/div[1]/div[2]/div/h1'))
        ).text.strip()
        dados_produto["produto"]["titulo"] = titulo

        breadcrumb_nav = wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, "nav[aria-label='Breadcrumb']"))
        )
        breadcrumb_items = breadcrumb_nav.find_elements(By.CSS_SELECTOR, "ol li")
        dados_produto["produto"]["localizacao"] = breadcrumb_items[-2].find_element(
            By.TAG_NAME, "a").get_attribute("href")
        dados_produto["produto"]["codigo"] = breadcrumb_items[-1].text.replace(
            "Código", "").strip()
    except Exception as e:
        raise RuntimeError(f"Falha ao extrair informações básicas do produto: {e}")
        

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
        review_element = wait.until(EC.presence_of_element_located((By.ID, "reviewsSection")))
        scroll_driver(review_element)
        nota_element = wait.until(lambda d: d.find_element(By.CSS_SELECTOR, "span.sc-781b7e7f-1.hdvIZL"))
        # Aguarda até que a nota seja diferente de vazio
        wait.until(lambda _: nota_element.text.strip() != "")

        nota_review = nota_element.text.strip()

        dados_produto["produto"]["classificacao"] = float(nota_review)
    except TimeoutException:
        dados_produto["produto"]["classificacao"] = 0    
    except Exception as e:
        dados_produto["produto"]["classificacao"] = 0
        

    # --- Avaliações ---
    pagina_atual = 1
    review_id = 1

    avaliacoes_unicas = set()  #evita avaliações duplicadas
    
    tentativas_nav = 0
    
    # Se a nota for 0, nem tenta buscar reviews
    if dados_produto["produto"]["classificacao"] > 0:
        while True:
            try:
                # Tenta pegar os containers de review
                review_containers = wait.until(EC.presence_of_all_elements_located(
                    (By.CSS_SELECTOR, "div.sc-9e789c55-0.grUenq"))
                )
                
                # Reseta contador de erro de navegação se carregou container com sucesso
                tentativas_nav = 0 

                for container in review_containers:
                    try:
                        autor = container.find_element(By.CSS_SELECTOR, "span.sc-d5f48f0e-1.heSJqR").text.strip()
                        nota_attr = container.find_element(By.CSS_SELECTOR, "div.ratingStarsContainer").get_attribute("aria-label")
                        nota = nota_attr.split(":")[1].strip() if nota_attr else None
                        data = container.find_element(By.CSS_SELECTOR, "span.sc-d5f48f0e-2.brbMqG").text.replace("Avaliado em ", "").strip()
                        comentario = container.find_element(By.CSS_SELECTOR, "span.sc-9e789c55-8.eUnvhx").text.strip()
                        titulo_av = container.find_element(By.CSS_SELECTOR, "h5.sc-d5f48f0e-3.gByuuW").text.strip()

                        chave = f"{autor}-{data}-{titulo_av}-{comentario[:30]}" # Chave um pouco mais curta
                        if chave not in avaliacoes_unicas:
                            avaliacoes_unicas.add(chave)
                            dados_produto["avaliacoes"].append({
                                "id": review_id,
                                "pagina": pagina_atual,
                                "autor": autor,
                                "nota": nota,
                                "data": data,
                                "titulo": titulo_av,
                                "comentario": comentario
                            })
                            review_id += 1
                    except Exception:
                        continue # Se falhar 1 review específico, pula ele

                # --- Paginação ---
                try:
                    next_li = driver.find_element(By.CSS_SELECTOR, "li.next")
                    if "disabled" in next_li.get_attribute("class"):
                        break # Fim das páginas
                    
                    next_button = next_li.find_element(By.TAG_NAME, "a")
                    
                    # Guarda estado antes de clicar
                    first_text_before = review_containers[0].text.strip()
                    
                    driver.execute_script("arguments[0].click();", next_button)
                    
                    # Espera a lista mudar
                    wait.until(lambda d: 
                        d.find_elements(By.CSS_SELECTOR, "div.sc-9e789c55-0.grUenq")[0].text.strip() != first_text_before
                    )
                    
                    pausa(2, 4)
                    pagina_atual += 1

                except Exception as e:
                    break
            
            except Exception as e:
                # Erro genérico no loop de reviews
                tentativas_nav += 1
                if tentativas_nav >= 2:
                    break

    dados_produto["produto"]["total_avaliacoes_coletadas"] = len(dados_produto["avaliacoes"])
    dados_produto["produto"]["url"] = url
    dados_produto["produto"]["data_extracao"] = time.strftime("%Y-%m-%d %H:%M:%S")

    pausa(2, 5) # Pausa entre produtos

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
