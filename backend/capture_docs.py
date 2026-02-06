from playwright.sync_api import sync_playwright
import time

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        try:
            print("Navigating to docs...")
            page.goto("http://127.0.0.1:8015/docs", timeout=60000)
            page.wait_for_selector("h2", timeout=60000) # Wait for some content
            print("Page loaded. taking screenshot...")
            page.screenshot(path="api_docs_screenshot.png", full_page=True)
            print("Screenshot saved to api_docs_screenshot.png")
        except Exception as e:
            print(f"Error: {e}")
        finally:
            browser.close()

if __name__ == "__main__":
    run()
