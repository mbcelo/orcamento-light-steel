import streamlit as st
from gerador_pdf_simples import gerar_pdf

st.set_page_config(page_title="🧾 Gerador de Proposta PDF", layout="centered")
st.title("🧾 Gerador de Proposta PDF - Steel Facility")

st.markdown("Preencha os dados abaixo para gerar sua proposta com visual profissional:")

cliente = st.text_input("Nome do cliente")
area = st.number_input("Área da obra (m²)", min_value=0.0, step=1.0)
dias = st.number_input("Prazo de execução (dias)", min_value=1)
funcionarios = st.number_input("Quantidade de funcionários", min_value=1)

st.markdown("### 💰 Custos estimados")
total_mao_obra = st.number_input("Mão de obra (R$)", min_value=0.0, step=100.0)
total_alimentacao = st.number_input("Alimentação (R$)", min_value=0.0, step=50.0)
total_hospedagem = st.number_input("Hospedagem (R$)", min_value=0.0, step=50.0)
total_deslocamento = st.number_input("Deslocamento (R$)", min_value=0.0, step=50.0)
total_viagens = st.number_input("Viagens (R$)", min_value=0.0, step=50.0)
total_ferramentas = st.number_input("Ferramentas (R$)", min_value=0.0, step=50.0)

lucro_perc = st.slider("Margem de lucro (%)", min_value=0, max_value=100, value=20) / 100.0

if st.button("📤 Gerar PDF da proposta"):
    subtotal = (
        total_mao_obra +
        total_alimentacao +
        total_hospedagem +
        total_deslocamento +
        total_viagens +
        total_ferramentas
    )
    lucro = subtotal * lucro_perc
    valor_final = subtotal + lucro

    html = gerar_html(
        cliente, area, dias, funcionarios,
        total_mao_obra, total_alimentacao, total_hospedagem,
        total_deslocamento, total_viagens, total_ferramentas,
        subtotal, lucro, valor_final, lucro_perc
    )

    gerar_pdf(cliente, html)
    st.success(f"✅ PDF gerado para o cliente {cliente}")
    st.markdown(f"📎 Arquivo salvo como: `proposta_{cliente.replace(' ', '_')}.pdf`")
