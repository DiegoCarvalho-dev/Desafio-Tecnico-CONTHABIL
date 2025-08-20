import os
import time
import random
import logging
import requests
import re
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from urllib.parse import urljoin, urlparse
import json

# Configuração de logging SEM EMOJIS
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("scraper.log", encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

API_URL = "http://127.0.0.1:8000/publicacoes/"


# ---------------------------
# Setup do navegador - CORRIGIDO
# ---------------------------
def setup_driver():
    try:
        options = webdriver.ChromeOptions()

        # Remover headless temporariamente para debugging
        # options.add_argument("--headless=new")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)

        # User agents aleatórios
        user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Safari/605.1.15",
        ]
        options.add_argument(f"user-agent={random.choice(user_agents)}")

        download_dir = os.path.join(os.getcwd(), "data", "pdfs")
        os.makedirs(download_dir, exist_ok=True)

        prefs = {
            "download.default_directory": download_dir,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "plugins.always_open_pdf_externally": True,
            "profile.default_content_settings.popups": 0,
            "safebrowsing.enabled": True
        }
        options.add_experimental_option("prefs", prefs)

        # CORREÇÃO: Obter o caminho correto do ChromeDriver
        driver_manager = ChromeDriverManager()
        driver_path = driver_manager.install()

        # Verificar se o caminho está correto (deve terminar com .exe)
        if not driver_path.endswith('.exe'):
            # Procurar o arquivo chromedriver.exe no diretório
            driver_dir = os.path.dirname(driver_path)
            for file in os.listdir(driver_dir):
                if file.lower() == 'chromedriver.exe':
                    driver_path = os.path.join(driver_dir, file)
                    break
            else:
                # Se não encontrar, tentar um caminho diferente
                driver_path = os.path.join(driver_dir, 'chromedriver.exe')

        logger.info(f"ChromeDriver path: {driver_path}")

        # Verificar se o arquivo existe
        if not os.path.exists(driver_path):
            raise FileNotFoundError(f"ChromeDriver não encontrado em: {driver_path}")

        service = Service(executable_path=driver_path)
        driver = webdriver.Chrome(service=service, options=options)

        # Ocultar automação
        driver.execute_script(
            "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
        )

        logger.info("Driver configurado com sucesso")
        return driver, download_dir

    except Exception as e:
        logger.error(f"Erro ao configurar driver: {e}")
        raise


# ---------------------------
# Upload PDF no 0x0.st
# ---------------------------
def upload_to_transfer_sh(file_path: str) -> str | None:
    """Upload usando transfer.sh - funciona melhor que 0x0.st"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }

        file_name = os.path.basename(file_path)

        with open(file_path, "rb") as f:
            response = requests.put(
                f"https://transfer.sh/{file_name}",
                data=f,
                headers=headers,
                timeout=60
            )

        if response.status_code == 200:
            return response.text.strip()
        logger.error(f"Falha ao enviar para transfer.sh: {response.status_code} - {response.text}")
        return None
    except Exception as e:
        logger.error(f"Erro no upload para transfer.sh: {e}")
        return None

# ---------------------------
# Upload PDF (função principal atualizada)
# ---------------------------
def upload_file(file_path: str) -> str | None:
    """Função principal de upload - usa transfer.sh"""
    return upload_to_transfer_sh(file_path)


# ---------------------------
# Registrar publicação na API
# ---------------------------
def create_publicacao(url: str, competencia: str, data_publicacao: str, titulo: str = ""):
    try:
        payload = {
            "url": url,
            "competencia": competencia,
            "data_publicacao": data_publicacao,
            "titulo": titulo
        }
        response = requests.post(API_URL, json=payload, timeout=30)
        if response.status_code == 201:
            logger.info(f"Publicacao salva: {url}")
            return True
        else:
            logger.error(f"Erro ao salvar no banco: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        logger.error(f"Falha ao conectar na API: {e}")
        return False


# ---------------------------
# Download PDF
# ---------------------------
def download_pdf(url: str, download_dir: str, file_name: str) -> str | None:
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }

        response = requests.get(url, headers=headers, stream=True, timeout=60)
        response.raise_for_status()

        # Verificar se é realmente um PDF
        content_type = response.headers.get('content-type', '')
        if 'pdf' not in content_type.lower():
            logger.warning(f"URL não é um PDF: {content_type}")
            return None

        file_path = os.path.join(download_dir, file_name)

        # Garantir nome de arquivo único
        counter = 1
        base_name, ext = os.path.splitext(file_path)
        while os.path.exists(file_path):
            file_path = f"{base_name}_{counter}{ext}"
            counter += 1

        with open(file_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)

        # Verificar se o arquivo foi baixado corretamente
        if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
            logger.info(f"PDF baixado: {file_path} ({os.path.getsize(file_path)} bytes)")
            return file_path
        else:
            logger.error("Arquivo PDF vazio ou não foi salvo")
            return None

    except Exception as e:
        logger.error(f"Erro ao baixar PDF de {url}: {e}")
        return None


# ---------------------------
# Extrair data do título/nome do arquivo
# ---------------------------
def extract_date_from_text(text: str) -> str:
    try:
        # Padrões comuns de datas em diários oficiais
        patterns = [
            r'(\d{2})/(\d{2})/(\d{4})',
            r'(\d{2})-(\d{2})-(\d{4})',
            r'(\d{4})-(\d{2})-(\d{2})',
            r'(\d{2})\.(\d{2})\.(\d{4})',
        ]

        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                groups = match.groups()
                if len(groups) == 3:
                    if len(groups[2]) == 4:  # AAAA
                        return f"{groups[2]}-{groups[1].zfill(2)}-{groups[0].zfill(2)}"
                    else:  # DD/MM/AA
                        return f"20{groups[2]}-{groups[1].zfill(2)}-{groups[0].zfill(2)}"

        # Se não encontrar data, usar data atual
        return datetime.now().strftime("%Y-%m-%d")

    except Exception as e:
        logger.error(f"Erro ao extrair data: {e}")
        return datetime.now().strftime("%Y-%m-%d")


# ---------------------------
# Obter mês anterior
# ---------------------------
def get_previous_month():
    today = datetime.now()
    first_day = today.replace(day=1)
    previous_month = first_day - timedelta(days=1)
    return previous_month.strftime("%m/%Y")


# ---------------------------
# Scraper principal simplificado
# ---------------------------
def scrape_diarios(driver, month_year: str, download_dir: str):
    try:
        logger.info("Acessando site da prefeitura de Natal...")
        driver.get("https://www.natal.rn.gov.br/dom")

        # Aguardar carregamento
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        time.sleep(3)

        # Salvar página para análise
        page_source = driver.page_source
        with open("page_source.html", "w", encoding="utf-8") as f:
            f.write(page_source)
        logger.info("Pagina salva em page_source.html para analise")

        # Analisar a estrutura da página
        logger.info("Analisando estrutura da página...")

        # Procurar todos os links PDF
        pdf_links = driver.find_elements(By.XPATH, "//a[contains(@href, '.pdf')]")
        logger.info(f"Encontrados {len(pdf_links)} links PDF")

        mes, ano = month_year.split("/")
        competencia = f"{ano}-{mes.zfill(2)}"

        processed_count = 0
        for i, link in enumerate(pdf_links):
            try:
                href = link.get_attribute("href")
                link_text = link.text.strip()

                logger.info(f"Processando link {i + 1}: {href}")

                # FILTRAR: Apenas links que contenham "dom_" no caminho (diários oficiais)
                if (href and href.lower().endswith('.pdf') and
                        '/dom/' in href.lower() and
                        'dom_' in href.lower()):

                    # Extrair data do texto do link ou do URL
                    data_publicacao = extract_date_from_text(link_text or href)

                    # Nome do arquivo mais descritivo
                    file_name = f"diario_{data_publicacao.replace('-', '')}_{i + 1}.pdf"

                    # Download do PDF
                    file_path = download_pdf(href, download_dir, file_name)

                    if file_path:
                        # Upload para serviço de arquivos (agora usando transfer.sh)
                        uploaded_url = upload_file(file_path)  # ← LINHA CORRIGIDA

                        if uploaded_url:
                            # Registrar no banco
                            success = create_publicacao(uploaded_url, competencia, data_publicacao, link_text)
                            if success:
                                processed_count += 1
                                logger.info(f"Arquivo {i + 1} processado com sucesso!")

                    # Delay entre requisições
                    time.sleep(random.uniform(1, 3))
                else:
                    logger.info(f"Link {i + 1} ignorado (não é diário oficial): {href}")

            except Exception as e:
                logger.error(f"Erro ao processar link {i + 1}: {e}")
                continue

        logger.info(f"Processamento concluído. {processed_count} arquivos processados com sucesso")

    except Exception as e:
        logger.error(f"Erro no scraping: {e}", exc_info=True)
        driver.save_screenshot("scraper_error.png")
    finally:
        if driver:
            driver.quit()


# ---------------------------
# Executar
# ---------------------------
def run_scraper(month_year=None):
    if month_year is None:
        month_year = get_previous_month()

    logger.info(f"Iniciando scraper para {month_year}")

    try:
        driver, download_dir = setup_driver()
        scrape_diarios(driver, month_year, download_dir)
    except Exception as e:
        logger.error(f"Erro fatal: {e}", exc_info=True)


if __name__ == "__main__":
    run_scraper("08/2024")  # Usar mês atual para teste