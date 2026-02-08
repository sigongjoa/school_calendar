const { chromium } = require('playwright');
const path = require('path');

(async () => {
    const browser = await chromium.launch({ headless: true });
    const page = await browser.newPage();

    await page.setViewportSize({ width: 1280, height: 800 });

    console.log('Navigating to http://localhost:5176/');
    try {
        await page.goto('http://localhost:5176/', { waitUntil: 'networkidle', timeout: 30000 });

        // Manual wait to ensure animations and fonts are settled
        await page.waitForTimeout(2000);

        // 1. Calendar Page
        console.log('Capturing Calendar Page...');
        await page.screenshot({ path: '/root/.gemini/antigravity/brain/8da12625-442c-4236-bd40-8e9a7fc34d3f/calendar_view_final.png' });

        // 2. Navigation to School Management
        console.log('Navigating to School Management...');
        await page.click('text=학교 관리');
        await page.waitForTimeout(1000);
        await page.screenshot({ path: '/root/.gemini/antigravity/brain/8da12625-442c-4236-bd40-8e9a7fc34d3f/school_management_view_final.png' });

        // 3. Search Test
        console.log('Performing Search Test...');
        await page.fill('input', '대치');
        await page.click('button:has-text("추가")');
        await page.waitForTimeout(2000);
        await page.screenshot({ path: '/root/.gemini/antigravity/brain/8da12625-442c-4236-bd40-8e9a7fc34d3f/search_results_view_final.png' });

        console.log('Final screenshots captured.');
    } catch (err) {
        console.error('Error during Playwright test:', err);
    } finally {
        await browser.close();
    }
})();
