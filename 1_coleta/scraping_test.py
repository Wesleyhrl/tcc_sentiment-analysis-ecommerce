import json
import time
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

url = "https://www.kabum.com.br/produto/603223/fonte-husky-sledger-650w-80-plus-bronze-cybenetics-bronze-pfc-ativo-bivolt-hfn650pt"

options = webdriver.ChromeOptions()
options.add_argument("--headless=new")

# Opções para resolver os erros
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--disable-notifications')


driver = webdriver.Chrome(options=options)
driver.get(url)

wait = WebDriverWait(driver, 15)

# Dicionário para armazenar todos os dados
dados_produto = {
    "produto": {},
    "avaliacoes": []
}


def extract_brand_model(text: str):
    """
    Extrai a marca e o modelo de uma string de texto e atualiza o dicionário global dados_produto.

    Args:
        text (str): O texto bruto contendo as informações técnicas.
    """
    lines = [line.strip() for line in text.split('\n') if line.strip()]

    for line in lines:
        item_text = line.lstrip('- ').strip()

        # Extrai e atualiza a marca e o modelo
        if item_text.startswith("Marca:"):
            dados_produto["produto"]["marca"] = item_text.replace(
                "Marca:", "").strip()
        elif item_text.startswith("Modelo:"):
            dados_produto["produto"]["modelo"] = item_text.replace(
                "Modelo:", "").strip()


# Extrair dados do produto
try:
    # Título do produto
    titulo = wait.until(
        EC.presence_of_element_located(
            (By.XPATH, '//*[@id="main-content"]/div[1]/div[1]/div[1]/div[2]/div/h1'))
    ).text.strip()
    dados_produto["produto"]["titulo"] = titulo
except Exception as e:
    print(f"Erro ao extrair título: {str(e)}")
    dados_produto["produto"]["titulo"] = None


# Extrair local (breadcrumb)
try:
    breadcrumb_nav = wait.until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, "nav[aria-label='Breadcrumb']"))
    )

    # Extrai todos os itens do breadcrumb
    breadcrumb_items = breadcrumb_nav.find_elements(By.CSS_SELECTOR, "ol li")

    dados_produto["produto"]["localizacao"] = breadcrumb_items[-2].find_element(
        By.TAG_NAME, "a").get_attribute("href")
    dados_produto["produto"]["codigo"] = breadcrumb_items[-1].text.replace(
        "Código", "").strip()

except Exception as e:
    print(f"Erro ao extrair localização: {str(e)}")
    dados_produto["produto"]["localizacao"] = None
    dados_produto["produto"]["codigo"] = None

try:
    loja = wait.until(
        EC.presence_of_element_located(
            (By.XPATH, '//*[@id="main-content"]/div[1]/div[1]/div[1]/div[2]/div/div[3]'))
    ).text.replace("\n", "").strip()
    dados_produto["produto"]["loja"] = loja
except Exception as e:
    print(f"Erro ao extrair título: {str(e)}")
    dados_produto["produto"]["loja"] = None

try:
    # Descrição do produto
    descricao_section = wait.until(
        EC.presence_of_element_located((By.ID, "descriptionSection"))
    )
    descricao = descricao_section.find_element(
        By.CSS_SELECTOR, "div#description").text.strip()
    dados_produto["produto"]["descricao"] = descricao
except Exception as e:
    print(f"Erro ao extrair descrição: {str(e)}")
    dados_produto["produto"]["descricao"] = None


try:
    # Informações técnicas
    tech_info_section = wait.until(
        EC.presence_of_element_located((By.ID, "technicalInfoSection"))
    )
    tech_info = tech_info_section.find_element(
        By.CSS_SELECTOR, "div.sc-7e0ca514-0").text.strip()
    extract_brand_model(tech_info)  # Extrai marca e modelo

    dados_produto["produto"]["informacoes_tecnicas"] = tech_info

except Exception as e:
    print(f"Erro ao extrair informações técnicas: {str(e)}")
    dados_produto["produto"]["informacoes_tecnicas"] = None

# Extrair avaliações
pagina_atual = 1
limite_paginas = 100  # limite máximo
ultima_avaliacao = {}
tentativas_duplicacao = 0;

while True:
    print(f"Extraindo página {pagina_atual}...")

    # Encontra todos os containers de avaliação

    review_containers = wait.until(
        EC.presence_of_all_elements_located(
            (By.CSS_SELECTOR, "div.sc-9e789c55-0.grUenq"))
    )

    if not review_containers:
        print("Nenhuma avaliação encontrada nesta página.")

    for container in review_containers:
        try:
            autor = container.find_element(
                By.CSS_SELECTOR, "span.sc-69a11a32-1.FofEv").text.strip()
        except:
            autor = "Anônimo"

        try:
            nota = container.find_element(
                By.CSS_SELECTOR, "div.ratingStarsContainer").get_attribute("aria-label")
            nota = nota.split(":")[1].strip() if nota else None
        except:
            nota = None

        try:
            data = container.find_element(
                By.CSS_SELECTOR, "span.sc-69a11a32-2.bIGeMU").text.strip()
            data = data.replace("Avaliado em ", "")
        except:
            data = None

        try:
            comentario = container.find_element(
                By.CSS_SELECTOR, "span.sc-9e789c55-8.eUnvhx").text.strip()
        except:
            comentario = ""

        try:
            titulo_avaliacao = container.find_element(
                By.CSS_SELECTOR, "h5.sc-69a11a32-3.bZhNfY").text.strip()
        except:
            titulo_avaliacao = ""

        avaliacao_atual = {
            "pagina": pagina_atual,
            "autor": autor,
            "nota": nota,
            "data": data,
            "titulo": titulo_avaliacao,
            "comentario": comentario
        }
        
        dados_produto["avaliacoes"].append(avaliacao_atual)

        # Verifica duplicação de avaliações
        if(ultima_avaliacao and avaliacao_atual == ultima_avaliacao):
            tentativas_duplicacao += 1
            print(f"AVISO: Avaliações duplicadas na página {pagina_atual}. Tentativa {tentativas_duplicacao}/3")
            if tentativas_duplicacao >= 3:
                print("Muitas tentativas com conteúdo duplicado. Parando extração.")
                break
            try:
                if( pagina_atual > 1 ):
                    previous_button1 = wait.until(EC.element_to_be_clickable(
                        (By.CSS_SELECTOR, "li.next a.prevLink")
                    ))
                    driver.execute_script("arguments[0].click();", previous_button1)
                    time.sleep(2)

                    next_button1 = wait.until(EC.element_to_be_clickable(
                        (By.CSS_SELECTOR, "li.next a.nextLink")
                    ))
                    driver.execute_script("arguments[0].click();", next_button1)
                    time.sleep(2)
                    continue
                else:
                    driver.refresh()
                    time.sleep(3)
                    continue

            except Exception as e:
                print(f"Falha ao tentar corrigir duplicação: {str(e)}")
                break     
        else:
            tentativas_duplicacao = 0

    ultima_avaliacao = avaliacao_atual

    # Limite de páginas
    if pagina_atual >= limite_paginas:
        print("Limite de páginas atingido.")
        break

    # Tenta avançar para a próxima página
    try:

        next_button = wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "li.next")
        ))
        # Verifica se a classe "disabled" está presente na <li>
        if "disabled" in next_button.get_attribute("class"):
            print("Última página de avaliações atingida.")
            break

        next_button_link = wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "li.next a.nextLink")
        ))
        driver.execute_script("arguments[0].click();", next_button_link)

        time.sleep(3)  # tempo para carregar nova página

        # Espera a nova página carregar
        wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, "div.sc-9e789c55-0.grUenq")
        ))

        pagina_atual += 1
    except Exception as e:
        print(f"Erro ao mudar de página: {str(e)}")
        break


# Armazenar dados do produto
dados_produto["produto"]["total_avaliacoes_coletadas"] = len(
    dados_produto["avaliacoes"])
dados_produto["produto"]["url"] = url
dados_produto["produto"]["data_extracao"] = time.strftime("%Y-%m-%d %H:%M:%S")

# Salva em JSON
with open("dados_produto_kabum.json", "w", encoding="utf-8") as f:
    json.dump(dados_produto, f, indent=4, ensure_ascii=False)

print(
    f"Extração concluída. {dados_produto['produto']['total_avaliacoes_coletadas']} avaliações coletadas.")
driver.quit()
