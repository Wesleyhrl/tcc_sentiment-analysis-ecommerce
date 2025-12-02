import time
import requests
from lxml import etree
from database import get_database


# CONFIG MONGODB 
db = get_database()
collection = db["sitemaps"]

# HEADERS
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/115.0 Safari/537.36"
}


def process_sitemap(url: str):
    """Extrai URLs de um sitemap XML e salva no MongoDB.
       Lança exceção em caso de erro crítico."""
    try:
        resp = requests.get(url, headers=headers, timeout=15)
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Erro de conexão com {url}: {e}")

    if resp.status_code != 200:
        raise RuntimeError(f"Erro ao acessar {url}: status {resp.status_code}")

    try:
        parser = etree.XMLParser(ns_clean=True, recover=True, encoding="utf-8")
        xml = etree.fromstring(resp.content, parser=parser)
    except Exception as e:
        raise RuntimeError(f"Erro ao processar XML de {url}: {e}")

    ns = {"ns": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    data = {"sitemap": {}, "urls": []}

    for u in xml.findall("ns:url", ns):
        loc = u.find("ns:loc", ns).text
        lastmod = u.find("ns:lastmod", ns)
        data["urls"].append(
            {"url": loc, "lastmod": lastmod.text if lastmod is not None else None}
        )

    data["sitemap"] = {
        "origem": url,
        "data_extracao": time.strftime("%Y-%m-%d %H:%M:%S"),
        "total_urls": len(data["urls"])
    }

    try:
        collection.delete_many({"sitemap.origem": url})
        collection.insert_one(data)
    except Exception as e:
        raise RuntimeError(f"Erro ao salvar no MongoDB ({url}): {e}")

    print(f"Salvo {len(data['urls'])} URLs no MongoDB (kabum_scraping.sitemaps)")
    return data
