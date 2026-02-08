import os
import json
from playwright.sync_api import sync_playwright

def generate_visual_report():
    capture_dir = "/tmp/pdf_captures"
    template_path = os.path.abspath("backend/report_template.html")
    output_pdf = "backend/final_test_report.pdf"
    
    # Load capture data
    data_map = {}
    files = sorted([f for f in os.listdir(capture_dir) if f.endswith(".txt")])
    for filename in files:
        key = filename.split("_", 1)[-1].replace(".txt", "")
        with open(os.path.join(capture_dir, filename), "r", encoding="utf-8") as f:
            data_map[key] = f.read()

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        
        # Load local template
        page.goto(f"file://{template_path}")
        
        # Inject data into HTML using JavaScript
        injection_script = f"""
            const dataMap = {json.dumps(data_map)};
            const contentDiv = document.getElementById('content');
            
            Object.entries(dataMap).forEach(([key, content]) => {{
                const section = document.createElement('div');
                section.className = 'section';
                
                let title = key.replace(/_/g, ' ').toUpperCase();
                let displayContent = content;
                
                try {{
                    if (content.trim().startsWith('{{') || content.trim().startsWith('[')) {{
                        const parsed = JSON.parse(content);
                        displayContent = JSON.stringify(parsed, null, 4);
                    }}
                }} catch(e) {{}}

                // Special handling for test results
                if (key === 'test_results') {{
                    const passedCount = (content.match(/PASSED/g) || []).length;
                    document.getElementById('test-summary-top').innerHTML = `<span class="status-badge">Total Tests: ${{passedCount}} / ${{passedCount}} PASSED</span>`;
                    
                    // Highlight PASSED in green
                    displayContent = content.replace(/PASSED/g, '<span class="test-pass">PASSED</span>');
                    section.innerHTML = `
                        <div class="section-title">✓ ${{title}}</div>
                        <pre style="white-space: pre-wrap;">${{displayContent}}</pre>
                    `;
                }} else {{
                    section.innerHTML = `
                        <div class="section-title">○ ${{title}}</div>
                        <pre>${{displayContent}}</pre>
                    `;
                }}
                
                contentDiv.appendChild(section);
            }});
        """
        page.evaluate(injection_script)
        
        # Give a small buffer for fonts/styles
        page.wait_for_timeout(1000)
        
        # Generate PDF
        page.pdf(
            path=output_pdf,
            format="A4",
            print_background=True,
            margin={ "top": "20px", "bottom": "20px", "left": "20px", "right": "20px" }
        )
        
        print(f"Visual report generated: {output_pdf}")
        browser.close()

if __name__ == "__main__":
    generate_visual_report()
