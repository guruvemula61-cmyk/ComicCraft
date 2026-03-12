from fpdf import FPDF
import os
from datetime import datetime


def clean_text(text: str):
    """
    Clean text so FPDF (latin-1) does not crash
    """
    if not text:
        return ""

    # Remove markdown
    text = text.replace("**", "")

    # Replace common unicode characters
    replacements = {
        "’": "'",
        "‘": "'",
        "“": '"',
        "”": '"',
        "—": "-",
        "–": "-",
        "…": "...",
    }

    for k, v in replacements.items():
        text = text.replace(k, v)

    # Final safe encoding
    text = text.encode("latin-1", "replace").decode("latin-1")

    return text


def save_pdf(layout):

    export_folder = "static/exports"
    os.makedirs(export_folder, exist_ok=True)

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)

    for panel in layout:

        pdf.add_page()

        # Panel Title
        pdf.set_font("Arial", "B", 16)

        title = f"Panel {panel.get('panel')} - {panel.get('title')}"
        title = clean_text(title)

        pdf.cell(0, 10, title, ln=True)

        # Image
        image_path = panel.get("image_path")

        if image_path and os.path.exists(image_path):

            try:
                pdf.image(image_path, x=10, y=30, w=180)

            except Exception:
                pdf.ln(10)
                pdf.set_font("Arial", "I", 12)
                pdf.cell(0, 10, "Image could not be loaded", ln=True)

        else:
            pdf.ln(10)
            pdf.set_font("Arial", "I", 12)
            pdf.cell(0, 10, "Image not available", ln=True)

        pdf.ln(110)

        # Story text
        pdf.set_font("Arial", "", 12)

        text = clean_text(panel.get("text", ""))

        pdf.multi_cell(0, 8, text)

    # Generate filename
    filename = f"comic_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"

    file_path = os.path.join(export_folder, filename)

    pdf.output(file_path)

    # Return web path
    return "/" + file_path.replace("\\", "/")