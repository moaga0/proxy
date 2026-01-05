import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException, WebDriverException
from webdriver_manager.chrome import ChromeDriverManager

# =====================
# 기본 설정
# =====================
BASE_URL = "https://xn--939au0g4vj8sq.net/theme/go/_list_cmp_tpl.php"
OUTPUT_DIR = "output/html"

VISIT_CA = [2005, 2010, 2015, 2020, 2025, 2030, 2035]
SHIPPING_CA = [3005, 3010, 3015, 3020, 3030]
PAGES = range(0, 1)

PAGE_TIMEOUT = 15
RETRY = 2
SLEEP = 0.5

os.makedirs(OUTPUT_DIR, exist_ok=True)

# =====================
# 로그 설정
# =====================
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

# =====================
# Chrome 옵션
# =====================
chrome_options = Options()
chrome_options.add_argument("--headless=new")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=1920,1080")
chrome_options.add_argument("--disable-blink-features=AutomationControlled")

# 리소스 로딩 차단 (속도 핵심)
prefs = {
    "profile.managed_default_content_settings.images": 2,
    "profile.managed_default_content_settings.fonts": 2,
    "profile.managed_default_content_settings.stylesheets": 2,
}
chrome_options.add_experimental_option("prefs", prefs)

# eager 로딩
chrome_options.page_load_strategy = "eager"

# =====================
# 드라이버 생성
# =====================
driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=chrome_options
)
driver.set_page_load_timeout(PAGE_TIMEOUT)

# =====================
# 수집 함수
# =====================
def fetch(ca: int, page: int):
    url = f"{BASE_URL}?ca={ca}&rpage={page}&row_num=28"
    filename = f"{OUTPUT_DIR}/{ca}_{page}.html"

    for attempt in range(1, RETRY + 2):
        try:
            logging.info(f"Fetching ▶ ca={ca}, page={page} (try {attempt})")
            driver.get(url)

            html = driver.page_source
            with open(filename, "w", encoding="utf-8") as f:
                f.write(html)

            size_kb = os.path.getsize(filename) // 1024
            logging.info(f"Saved ▶ {filename} ({size_kb} KB)")
            return

        except TimeoutException:
            logging.warning(f"Timeout ▶ ca={ca}, page={page}")

        except WebDriverException as e:
            logging.error(f"WebDriver error ▶ {e}")

        time.sleep(1)

    logging.error(f"페이지 수집 실패 ▶ ca={ca}, page={page}")

# =====================
# 실행
# =====================
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
    logging.info("크롤링 종료 (정상 종료)")
