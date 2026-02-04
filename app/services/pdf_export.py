import pdfkit
from flask import render_template
import os

def generate_pdf(template, form_data, language):
    # render HTML من template
    html = render_template(f"cv_templates/{template}.html", data=form_data, lang=language)
    # اسم ملف مؤقت
    slug = form_data.get("slug", "temp")
    output_path = f"/tmp/cv_{slug}.pdf"

    # تحويل HTML إلى PDF
    pdfkit.from_string(html, output_path)

    return output_path

