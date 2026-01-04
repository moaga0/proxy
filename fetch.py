import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

BASE_URL = "https://xn--939au0g4vj8sq.net/theme/go/_list_cmp_tpl.php"
CA_LIST = [2005, 2010, 2015, 2020, 2025, 2030, 2035]
PAGES = range(0, 6)

os.makedirs("html_cache/visit", exist_ok=True)

options = Options()
options.add_argument("--headless=new")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--window-size=1920,1080")

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=options
)

for ca in CA_LIST:
    for page in PAGES:
        url = f"{BASE_URL}?ca={ca}&rpage={page}&row_num=28"
        print(f"Fetching: {url}")

        try:
            driver.get(url)
            time.sleep(3)  # JS 렌더링 대기

            html = driver.page_source
            path = f"html_cache/visit/{ca}_{page}.html"

            with open(path, "w", encoding="utf-8") as f:
                f.write(html)

        except Exception as e:
            print(f"Failed: {e}")

driver.quit()
