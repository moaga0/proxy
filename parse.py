from bs4 import BeautifulSoup
import os, json

INPUT_DIR = "output/html"
OUTPUT_DIR = "output/parsed"

os.makedirs(OUTPUT_DIR, exist_ok=True)

results = []

for file in os.listdir(INPUT_DIR):
    if not file.endswith(".html"):
        continue

    with open(os.path.join(INPUT_DIR, file), encoding="utf-8") as f:
        soup = BeautifulSoup(f, "lxml")

    items = soup.select("li")  # 실제 selector는 필요시 조정

    for item in items:
        title = item.get_text(strip=True)
        if not title:
            continue

        results.append({
            "source": file,
            "title": title
        })

with open(f"{OUTPUT_DIR}/result.json", "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)
