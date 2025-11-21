from urllib.parse import urlparse

def extrair_partes_url(url: str):
    """
    Recebe: https://www.kabum.com.br/hardware/ssd-2-5/ssd-pcie-nvme
    Retorna: ['hardware', 'ssd-2-5', 'ssd-pcie-nvme']
    """
    if not url:
        return []
    
    path = urlparse(url).path
    # Remove strings vazias e barras extras
    partes = [p for p in path.split("/") if p]
    
    return partes