from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import os
import logging

# ======================
# Logging
# ======================
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger(__name__)

# ======================
# Config
# ======================
BASE_URL = "https://xn--939au0g4vj8sq.net/theme/go/_list_cmp_tpl.php"
CATEGORIES = [2005, 2010, 2015, 2020, 2025, 2030, 2035]
PAGES = range(1)
OUTPUT_DIR = "output/html"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ======================
# Chrome Options
# ======================
options = Options()
options.add_argument("--headless=new")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-gpu")
options.add_argument("--disable-extensions")
options.add_argument("--disable-background-networking")
options.add_argument("--disable-sync")
options.add_argument("--disable-default-apps")
options.add_argument("--disable-popup-blocking")
options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
)

# ⭐ Selenium 4 방식
# options.page_load_strategy = "none"
options.page_load_strategy = "eager"

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

logger.info("ChromeDriver 초기화")

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=options
)

driver.set_page_load_timeout(20)
driver.set_script_timeout(3)

logger.info("ChromeDriver ready")

# ======================
# Crawl
# ======================
try:
    for ca in CATEGORIES:
        logger.info(f"[CATEGORY START] ca={ca}")

        for page in PAGES:
            url = f"{BASE_URL}?ca={ca}&rpage={page}&row_num=28"
            file_path = f"{OUTPUT_DIR}/{ca}_{page}.html"

            logger.info(f"Request ▶ ca={ca}, page={page}")

            try:
                driver.get(url)

                # ⭐ 끝까지 안 기다림
                time.sleep(3)

                html = driver.page_source
                size_kb = len(html.encode("utf-8")) // 1024

                if size_kb < 10:
                    logger.warning(
                        f"HTML 너무 작음 ▶ ca={ca}, page={page} ({size_kb}KB)"
                    )

                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(html)

                logger.info(
                    f"Saved ▶ {file_path} ({size_kb} KB)"
                )

            except Exception as e:
                logger.error(
                    f"FAIL ▶ ca={ca}, page={page}, error={e}",
                    exc_info=True
                )

        logger.info(f"[CATEGORY END] ca={ca}")

finally:
    driver.quit()
    logger.info("ChromeDriver closed")
