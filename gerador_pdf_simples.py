from xhtml2pdf import pisa
import streamlit as st

def gerar_pdf(cliente, html_content):
    file_name = f"proposta_{cliente.replace(' ', '_')}.pdf"
    with open(file_name, "wb") as f:
        pisa.CreatePDF(html_content, dest=f)
    return file_name
