import os
import json
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.units import inch
from reportlab.lib import colors

# Font path for Korean support
KOREAN_FONT_PATH = "/usr/share/fonts/truetype/nanum/NanumGothic.ttf"
KOREAN_FONT_NAME = "NanumGothic"

def setup_fonts():
    if os.path.exists(KOREAN_FONT_PATH):
        pdfmetrics.registerFont(TTFont(KOREAN_FONT_NAME, KOREAN_FONT_PATH))
        return KOREAN_FONT_NAME
    return "Helvetica"

def draw_section_title(c, text, y_pos, font_name):
    c.setFont(font_name, 14)
    c.setFillColor(colors.blue)
    c.drawString(1 * inch, y_pos, text)
    c.setFillColor(colors.black)
    return y_pos - 20

def draw_text_lines(c, text, x, y, font_name, font_size, line_height, limit_y=1*inch):
    c.setFont(font_name, font_size)
    lines = text.split('\n')
    for line in lines:
        if y < limit_y:
            c.showPage()
            y = 10.5 * inch
            c.setFont(font_name, font_size)
        c.drawString(x, y, line)
        y -= line_height
    return y

def generate_report():
    font_name = setup_fonts()
    output_file = "test_result_report.pdf"
    c = canvas.Canvas(output_file, pagesize=A4)
    width, height = A4

    # Title
    c.setFont(font_name, 20)
    c.drawCentredString(width / 2, height - (1 * inch), "NEIS API 연동 및 테스트 결과 보고서")
    
    y = height - (1.5 * inch)
    
    capture_dir = "/tmp/pdf_captures"
    files = sorted([f for f in os.listdir(capture_dir) if f.endswith(".txt")])
    
    for filename in files:
        file_path = os.path.join(capture_dir, filename)
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            
        section_name = filename.split("_", 1)[-1].replace(".txt", "").replace("_", " ").title()
        y = draw_section_title(c, f"Section: {section_name}", y, font_name)
        
        # If it's JSON, pretty print it if possible, otherwise just raw
        try:
            if content.strip().startswith("{") or content.strip().startswith("["):
                data = json.loads(content)
                content = json.dumps(data, indent=4, ensure_ascii=False)
        except:
            pass
            
        y = draw_text_lines(c, content, 1 * inch, y, font_name, 9, 12)
        y -= 20 # Gap between sections

    c.save()
    print(f"Report generated: {output_file}")

if __name__ == "__main__":
    generate_report()
