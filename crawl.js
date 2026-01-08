const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const OUTPUT_DIR = 'output/html';
fs.mkdirSync(OUTPUT_DIR, { recursive: true });

const categories = ['2005', '2010', '2015', '2020', '2025', '2030', '2035'];

(async () => {
  const browser = await chromium.launch({
    headless: true,
    args: [
      '--disable-dev-shm-usage',
      '--no-sandbox'
    ]
  });

  const context = await browser.newContext({
    userAgent:
      'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120 Safari/537.36'
  });

  const page = await context.newPage();
  page.setDefaultTimeout(30000);

  for (const ca of categories) {
    for (let pageNo = 0; pageNo <= 60; pageNo++) {
      const url = `https://xn--939au0g4vj8sq.net/theme/go/_list_cmp_tpl.php?ca=${ca}&rpage=${pageNo}&row_num=28`;

      console.log(`[INFO] Fetching ▶ ca=${ca}, page=${pageNo}`);

      try {
        const response = await page.goto(url, {
          waitUntil: 'domcontentloaded',
          timeout: 20000
        });

        if (!response || !response.ok()) {
          console.warn(`[WARN] HTTP FAIL ▶ ca=${ca}, page=${pageNo}`);
          break;
        }

        const html = await page.content();
        const filePath = path.join(OUTPUT_DIR, `${ca}_${pageNo}.html`);
        fs.writeFileSync(filePath, html);

        console.log(`[OK] Saved ▶ ${filePath}`);

        await page.waitForTimeout(1500); // 서버 배려용 딜레이 (착한 크롤러)
      } catch (e) {
        console.warn(`[WARN] Failed ▶ ca=${ca}, page=${pageNo}`);
        console.warn(e.message);
        break; // 해당 카테고리 종료
      }
    }
  }

  await browser.close();
})();
