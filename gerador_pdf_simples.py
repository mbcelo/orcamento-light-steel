from xhtml2pdf import pisa
import os

def gerar_pdf(cliente, html_content):
    os.makedirs("propostas", exist_ok=True)
    file_name = f"proposta_{cliente.replace(' ', '_')}.pdf"
    caminho = os.path.join("propostas", file_name)

    with open(caminho, "wb") as f:
        pisa.CreatePDF(html_content, dest=f)

    return caminho
