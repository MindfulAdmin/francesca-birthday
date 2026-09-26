// Render print/index.html to a PDF using the installed Chrome.
// Usage: node render-pdf.js <input.html> <output.pdf>
// Needs playwright-core: set PLAYWRIGHT_CORE to its path, or install it here.
const { chromium } = require(process.env.PLAYWRIGHT_CORE || 'playwright-core');
const { pathToFileURL } = require('url');

(async () => {
  const [input, output] = process.argv.slice(2);
  const browser = await chromium.launch({ channel: 'chrome' });
  const page = await browser.newPage();
  await page.goto(pathToFileURL(input).href, { waitUntil: 'networkidle' });
  await page.evaluate(() => document.fonts.ready);
  await page.pdf({ path: output, preferCSSPageSize: true, printBackground: true });
  await browser.close();
})();
