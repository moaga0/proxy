import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import WebDriverException
from webdriver_manager.chrome import ChromeDriverManager

BASE_URL = "https://xn--939au0g4vj8sq.net/theme/go/_list_cmp_tpl.php"
OUTPUT_DIR = "output/html"

VISIT_CA = [2005, 2010, 2015, 2020, 2025, 2030, 2035]
SHIPPING_CA = [3005, 3010, 3015, 3020, 3030]
PAGES = range(0, 1)

RETRY = 3
LOAD_WAIT = 3       # 핵심: 무조건 이 시간만 기다림
SLEEP = 0.3

os.makedirs(OUTPUT_DIR, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

# Chrome 옵션
options = Options()
options.add_argument("--headless=new")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-gpu")
options.add_argument("--disable-blink-features=AutomationControlled")
options.page_load_strategy = "none"  # 중요 포인트

prefs = {
    "profile.managed_default_content_settings.images": 2,
    "profile.managed_default_content_settings.fonts": 2,
    "profile.managed_default_content_settings.stylesheets": 2,
}
options.add_experimental_option("prefs", prefs)

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=options
)

def fetch(ca: int, page: int):
    url = f"{BASE_URL}?ca={ca}&rpage={page}&row_num=28"
    path = f"{OUTPUT_DIR}/{ca}_{page}.html"

    for attempt in range(1, RETRY + 1):
        try:
            logging.info(f"Fetching ▶ ca={ca}, page={page} (try {attempt})")
            driver.get(url)

            # 무조건 일정 시간만 대기
            time.sleep(LOAD_WAIT)

            # 강제로 로딩 중단
            driver.execute_script("window.stop();")

            html = driver.page_source
            with open(path, "w", encoding="utf-8") as f:
                f.write(html)

            size_kb = os.path.getsize(path) // 1024
            logging.info(f"Saved ▶ {path} ({size_kb} KB)")
            return

        except WebDriverException as e:
            logging.warning(f"Retry ▶ ca={ca}, page={page}, reason={str(e)[:80]}")
            time.sleep(1)

    logging.error(f"페이지 수집 실패 ▶ ca={ca}, page={page}")

try:
    for ca in VISIT_CA:
        for page in PAGES:
            fetch(ca, page)
            time.sleep(SLEEP)

    for ca in SHIPPING_CA:
        for page in PAGES:
            fetch(ca, page)
            time.sleep(SLEEP)

finally:
    driver.quit()
    logging.info("크롤링 종료")
