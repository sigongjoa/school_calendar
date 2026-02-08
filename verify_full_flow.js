const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

const SCREENSHOT_DIR = path.join(__dirname, 'screenshots');
if (!fs.existsSync(SCREENSHOT_DIR)) {
    fs.mkdirSync(SCREENSHOT_DIR, { recursive: true });
}

(async () => {
    const browser = await chromium.launch({ headless: true });
    const page = await browser.newPage();

    // Capture console logs
    page.on('console', msg => console.log('PAGE LOG:', msg.text()));
    page.on('pageerror', err => console.log('PAGE ERROR:', err.message));

    await page.setViewportSize({ width: 1280, height: 800 });

    const baseUrl = 'http://localhost:5173/';

    try {
        console.log('Navigating to Dashboard...');
        const response = await page.goto(baseUrl, { waitUntil: 'networkidle', timeout: 30000 });
        console.log('Response status:', response.status());

        // Wait for ANY visible text that indicates the app is loaded
        console.log('Waiting for #root to be populated...');
        await page.waitForFunction(() => document.getElementById('root')?.innerHTML.length > 0, { timeout: 15000 });

        await page.waitForTimeout(3000);
        console.log('Capturing Dashboard...');
        await page.screenshot({ path: path.join(SCREENSHOT_DIR, '01_dashboard.png') });

        // Change to School Management
        console.log('Navigating to School Management...');
        await page.goto(baseUrl + '#/schools', { waitUntil: 'load' });
        await page.waitForTimeout(3000);
        await page.screenshot({ path: path.join(SCREENSHOT_DIR, '02_school_management.png') });

        // Search
        const inputs = page.locator('input');
        if (await inputs.count() > 0) {
            console.log('Found input, filling...');
            const searchInput = inputs.first();
            await searchInput.clear();
            await searchInput.fill('시지');
            await page.keyboard.press('Enter');
            console.log('Waiting for search results to appear...');
            await page.waitForSelector('text=시지중학교', { timeout: 10000 });
            await page.waitForTimeout(1000); // UI stabilization
            await page.screenshot({ path: path.join(SCREENSHOT_DIR, '03_search_results.png') });
        }

        // 4. Calendar View and Toggles
        console.log('Navigating to Calendar...');
        await page.goto(baseUrl + '#/calendar', { waitUntil: 'networkidle' });
        await page.waitForTimeout(3000);

        // Go to March 2026
        console.log('Moving to March 2026...');
        const nextButtons = page.locator('button').filter({ has: page.locator('svg.lucide-chevron-right') });
        if (await nextButtons.count() > 0) {
            await nextButtons.first().click();
            await page.waitForTimeout(2000);
        }

        console.log('Capturing full Calendar (March)...');
        await page.screenshot({ path: path.join(SCREENSHOT_DIR, '04_calendar_full.png') });

        // Toggle schools off to verify dynamic filtering
        console.log('Toggling 시지중학교 and 시지고등학교 off...');
        await page.click('text=시지중학교');
        await page.waitForTimeout(500);
        await page.click('text=시지고등학교');
        await page.waitForTimeout(2000);
        await page.screenshot({ path: path.join(SCREENSHOT_DIR, '05_calendar_filtered.png') });

        console.log('Done capturing.');
    } catch (err) {
        console.error('Test FAILED:', err);
        await page.screenshot({ path: path.join(SCREENSHOT_DIR, 'FAIL_STATE.png') });
        console.log('FAIL_STATE screenshot saved.');
    } finally {
        await browser.close();
    }
})();
