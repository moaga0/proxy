from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import os
import logging

# ======================
# Logging 설정
# ======================
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger(__name__)

# ======================
# 크롤링 설정
# ======================
BASE_URL = "https://xn--939au0g4vj8sq.net/theme/go/_list_cmp_tpl.php"
CATEGORIES = [2005, 2010, 2015, 2020, 2025, 2030, 2035]
PAGES = range(6)

OUTPUT_DIR = "output/html"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ======================
# Selenium 옵션
# ======================
options = Options()
options.add_argument("--headless=new")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
)

logger.info("ChromeDriver 초기화 시작")

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=options
)

logger.info("ChromeDriver 준비 완료")

# ======================
# 크롤링 시작
# ======================
try:
    for ca in CATEGORIES:
        logger.info(f"[CATEGORY START] ca={ca}")

        for page in PAGES:
            url = f"{BASE_URL}?ca={ca}&rpage={page}&row_num=28"
            file_path = f"{OUTPUT_DIR}/{ca}_{page}.html"

            logger.info(f"요청 시작 ▶ ca={ca}, page={page}")
            logger.debug(f"URL={url}")

            try:
                driver.get(url)
                time.sleep(2)

                html = driver.page_source
                size_kb = len(html.encode("utf-8")) // 1024

                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(html)

                logger.info(
                    f"저장 완료 ▶ {file_path} ({size_kb} KB)"
                )

            except Exception as e:
                logger.error(
                    f"페이지 수집 실패 ▶ ca={ca}, page={page}, error={e}",
                    exc_info=True
                )

        logger.info(f"[CATEGORY END] ca={ca}")

finally:
    driver.quit()
    logger.info("ChromeDriver 종료")
