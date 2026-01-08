const fs = require('fs');
const path = require('path');
const { chromium } = require('playwright');

const OUTPUT_DIR = 'output/html';
const CATEGORIES = ['2005', '2010', '2015', '2020', '2025', '2030', '2035'];
const MAX_PAGE = 60;
const TIMEOUT = 15000;

if (!fs.existsSync(OUTPUT_DIR)) {
  fs.mkdirSync(OUTPUT_DIR, { recursive: true });
}

(async () => {
  const browser = await chromium.launch({
    headless: true
  });

  const context = await browser.newContext({
    userAgent:
      'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 ' +
      '(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
  });

  const page = await context.newPage();

  for (const ca of CATEGORIES) {
    for (let pageNo = 0; pageNo <= MAX_PAGE; pageNo++) {
      const url =
        `https://xn--939au0g4vj8sq.net/theme/go/_list_cmp_tpl.php` +
        `?ca=${ca}&rpage=${pageNo}&row_num=28`;

      console.log(`[INFO] Fetching ▶ ca=${ca}, page=${pageNo}`);

      let success = false;

      for (let retry = 1; retry <= 3; retry++) {
        try {
          const response = await page.request.get(url, {
            timeout: TIMEOUT,
            headers: {
              'Accept': 'text/html,application/xhtml+xml',
              'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8',
              'Referer': 'https://xn--939au0g4vj8sq.net/',
            }
          });

          if (!response.ok()) {
            throw new Error(`HTTP ${response.status()}`);
          }

          const html = await response.text();

          if (html.length < 500) {
            throw new Error('HTML too small (blocked)');
          }

          const filePath =
            path.join(OUTPUT_DIR, `${ca}_${pageNo}.html`);
          fs.writeFileSync(filePath, html);

          console.log(
            `[OK] Saved ▶ ${filePath} (${html.length} bytes)`
          );

          success = true;
          break;
        } catch (err) {
          console.warn(
            `[WARN] Retry ${retry} ▶ ca=${ca}, page=${pageNo} (${err.message})`
          );
          await new Promise(r => setTimeout(r, 2000));
        }
      }

      if (!success) {
        console.error(
          `[ERROR] Failed ▶ ca=${ca}, page=${pageNo}`
        );
        break; // ❗ 해당 카테고리 중단 → 다음 ca
      }
    }
  }

  await browser.close();
})();
