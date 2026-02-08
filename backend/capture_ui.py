from playwright.sync_api import sync_playwright
import time
import os

def capture_ui():
    base_url = "http://localhost:5173"
    capture_dir = "/tmp/ui_captures"
    os.makedirs(capture_dir, exist_ok=True)
    
    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context(viewport={"width": 1280, "height": 800})
        page = context.new_page()
        
        # Log console messages
        page.on("console", lambda msg: print(f"CONSOLE {msg.type}: {msg.text}"))
        page.on("pageerror", lambda exc: print(f"PAGE ERROR: {exc}"))

        try:
            print(f"Navigating to {base_url}...")
            page.goto(base_url, timeout=60000)
            
            # Wait for any content in #root
            print("Waiting for app to mount...")
            page.wait_for_selector("#root > *", timeout=30000)
            
            time.sleep(5) # Extra buffer for animations
            
            # Screenshot 1: Dashboard
            page.screenshot(path=f"{capture_dir}/01_dashboard.png", full_page=True)
            print("Captured Dashboard")
            
            # Navigate to Calendar
            # The app likely uses client-side routing. Let's try to find common links.
            calendar_btn = page.locator("a[href*='/calendar'], button:has-text('일정'), button:has-text('Calendar')")
            if calendar_btn.count() > 0:
                calendar_btn.first.click()
                time.sleep(3)
                page.screenshot(path=f"{capture_dir}/03_calendar.png", full_page=True)
                print("Captured Calendar")
            else:
                # Try physical navigation
                page.goto(f"{base_url}/calendar")
                time.sleep(3)
                page.screenshot(path=f"{capture_dir}/03_calendar_nav.png", full_page=True)
                print("Captured Calendar via Nav")

        except Exception as e:
            print(f"Error during capture: {e}")
            page.screenshot(path=f"{capture_dir}/error_final.png")
            # Log the HTML for debugging
            with open(f"{capture_dir}/page_debug.html", "w") as f:
                f.write(page.content())
        finally:
            browser.close()

if __name__ == "__main__":
    capture_ui()
