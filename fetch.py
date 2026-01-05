from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time, os

BASE_URL = "https://xn--939au0g4vj8sq.net/theme/go/_list_cmp_tpl.php"

CATEGORIES = [2005,2010,2015,2020,2025,2030,2035]
PAGES = range(6)

options = Options()
options.add_argument("--headless=new")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
)

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=options
)

os.makedirs("output/html", exist_ok=True)

for ca in CATEGORIES:
    for page in PAGES:
        url = f"{BASE_URL}?ca={ca}&rpage={page}&row_num=28"
        driver.get(url)
        time.sleep(2)

        path = f"output/html/{ca}_{page}.html"
        with open(path, "w", encoding="utf-8") as f:
            f.write(driver.page_source)

driver.quit()
