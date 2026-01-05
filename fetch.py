import os
import time
import logging

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException, WebDriverException
from webdriver_manager.chrome import ChromeDriverManager


# =========================
# 기본 설정
# =========================
BASE_URL = "https://xn--939au0g4vj8sq.net/theme/go/_list_cmp_tpl.php"
OUTPUT_DIR = "output/html"

VISIT_CATEGORIES = ["2005", "2010", "2015", "2020", "2025", "2030", "2035"]
MAX_PAGE = 1   # ✅ 0,1,2까지만

os.makedirs(OUTPUT_DIR, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)


# =========================
# Chrome Driver 생성
# =========================
def create_driver() -> webdriver.Chrome:
    options = Options()

    # Headless
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    # ✅ 1️⃣ 리소스 차단
    prefs = {
        "profile.managed_default_content_settings.images": 2,
        "profile.managed_default_content_settings.stylesheets": 2,
        "profile.managed_default_content_settings.fonts": 2,
        "profile.managed_default_content_settings.cookies": 2,
        "profile.managed_default_content_settings.plugins": 2,
        "profile.managed_default_content_settings.popups": 2,
        "profile.managed_default_content_settings.geolocation": 2,
        "profile.managed_default_content_settings.notifications": 2,
    }
    options.add_experimental_option("prefs", prefs)

    # ✅ 2️⃣ eager 로딩
    options.page_load_strategy = "eager"

    service = Service(ChromeDriverManager().install())

    driver = webdriver.Chrome(service=service, options=options)

    # ✅ 3️⃣ timeout 최소화
    driver.set_page_load_timeout(20)
    driver.implicitly_wait(3)

    return driver


# =========================
# 페이지 수집
# =========================
def fetch_pages():
    driver = create_driver()

    try:
for ca in VISIT_CATEGORIES:
    for page in range(MAX_PAGE):
        url = f"{BASE_URL}?ca={ca}&rpage={page}&row_num=28"
        output_path = f"{OUTPUT_DIR}/{ca}_{page}.html"

        logger.info(f"Fetching ▶ ca={ca}, page={page}")

        try:
            start = time.time()
            try:
                driver.get(url)
            except TimeoutException:
                logger.warning(
                    f"Timeout 발생, 로딩 중단 ▶ ca={ca}, page={page}"
                )
                driver.execute_script("window.stop();")

            html = driver.page_source

            if not html or len(html) < 300:
                logger.warning(
                    f"HTML 비정상 ▶ ca={ca}, page={page}, size={len(html) if html else 0}"
                )
                continue

            with open(output_path, "w", encoding="utf-8") as f:
                f.write(html)

            elapsed = round(time.time() - start, 2)
            size_kb = round(len(html.encode("utf-8")) / 1024, 1)

            logger.info(
                f"Saved ▶ {output_path} ({size_kb} KB, {elapsed}s)"
            )

        except Exception as e:
            logger.error(
                f"페이지 수집 실패 ▶ ca={ca}, page={page}, error={e}"
            )


    finally:
        driver.quit()
        logger.info("Driver closed")


# =========================
# Entry Point
# =========================
if __name__ == "__main__":
    fetch_pages()
