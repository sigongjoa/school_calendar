import os
import subprocess
from playwright.sync_api import sync_playwright

def run_verification():
    # 1. Capture screenshots
    print("Capturing screenshots with Playwright (Node.js)...")
    subprocess.run(["node", "verify_full_flow.js"], check=True)

    # 2. Generate PDF
    print("Generating PDF report...")
    report_html = os.path.abspath("report_screenshots.html")
    output_pdf = os.path.abspath("final_visual_report.pdf")
    screenshot_dir = "/tmp/screenshots"

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        
        # We need to serve the screenshots so the relative paths in HTML work, 
        # or we can use file:// with absolute paths. 
        # For simplicity, we'll set the base URL to the screenshot directory.
        page.goto(f"file://{report_html}")
        
        # Give a small buffer for fonts/styles/images to load
        page.wait_for_timeout(3000)
        
        page.pdf(
            path=output_pdf,
            format="A4",
            print_background=True,
            margin={ "top": "20px", "bottom": "20px", "left": "20px", "right": "20px" }
        )
        
        print(f"Success! PDF generated at: {output_pdf}")
        browser.close()

if __name__ == "__main__":
    run_verification()
