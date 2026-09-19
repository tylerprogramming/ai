const puppeteer = require('puppeteer');

const url = process.argv[2];
const ss = process.argv[3];
const fullPath = `${ss}`
const timeout = 75000;

(async () => {
    const browser = await puppeteer.launch( {
        headless: "new",
    } );

    const page = await browser.newPage();

    await page.setViewport( {
        width: 1920,
        height: 1080,
        deviceScaleFactor: 1,
    } );

    await page.goto( url, {
        waitUntil: "networkidle0",
        timeout: timeout,
    } );

    await page.screenshot( {
        path: fullPath,
        fullPage: true,
    } );

    await browser.close();
})();
