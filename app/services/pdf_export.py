from weasyprint import HTML
from flask import render_template
import tempfile
import os

def generate_pdf(template_name, data, lang):
    html_content = render_template(
        f"cv_templates/{template_name}.html",
        data=data,
        lang=lang
    )

    tmp_pdf = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")

    HTML(string=html_content, base_url=os.getcwd()).write_pdf(tmp_pdf.name)

    return tmp_pdf.name
