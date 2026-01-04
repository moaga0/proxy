import os
import time
import requests

BASE_URL = "https://xn--939au0g4vj8sq.net/theme/go/_list_cmp_tpl.php"
VISIT_CATEGORIES = [2005, 2010, 2015, 2020, 2025, 2030, 2035]
SHIPPING_CATEGORIES = [3005, 3010, 3015, 3020, 3030]

TIMEOUT = 15
SLEEP_SEC = 1

def fetch_and_save(ca: int, page: int, target_dir: str):
    url = f"{BASE_URL}?ca={ca}&rpage={page}&row_num=28"
    file_path = f"{target_dir}/{ca}_{page}.html"

    print(f"[START] ca={ca} page={page}", flush=True)
    print(f"[REQUEST] {url}", flush=True)

    try:
        start = time.time()
        res = requests.get(url, timeout=TIMEOUT)
        elapsed = round(time.time() - start, 2)

        print(
            f"[RESPONSE] ca={ca} page={page} "
            f"status={res.status_code} elapsed={elapsed}s size={len(res.text)}",
            flush=True
        )

        if res.status_code != 200 or not res.text.strip():
            print(
                f"[WARN] invalid response ca={ca} page={page}",
                flush=True
            )
            return

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(res.text)

        print(f"[SAVE] {file_path}", flush=True)

    except requests.exceptions.Timeout:
        print(f"[TIMEOUT] ca={ca} page={page}", flush=True)

    except requests.exceptions.RequestException as e:
        print(
            f"[ERROR] ca={ca} page={page} exception={repr(e)}",
            flush=True
        )

    finally:
        print(f"[SLEEP] {SLEEP_SEC}s", flush=True)
        time.sleep(SLEEP_SEC)


def run():
    print("========== FETCH START ==========", flush=True)

    os.makedirs("cache/visit", exist_ok=True)
    os.makedirs("cache/shipping", exist_ok=True)

    print("[INIT] directories prepared", flush=True)

    print("========== VISIT ==========", flush=True)
    for ca in VISIT_CATEGORIES:
        for page in range(0, 6):
            fetch_and_save(ca, page, "cache/visit")

    print("========== SHIPPING ==========", flush=True)
    for ca in SHIPPING_CATEGORIES:
        for page in range(0, 6):
            fetch_and_save(ca, page, "cache/shipping")

    print("========== FETCH END ==========", flush=True)


if __name__ == "__main__":
    run()
