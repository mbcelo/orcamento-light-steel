import streamlit as st
from gerador_pdf_simples import gerar_pdf

def executar_app():
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

        html = f"""
        <html>
        <head>
        <style>
            body {{
                font-family: 'Segoe UI', sans-serif;
                padding: 40px;
                color: #333;
                background-color: #f7f9fa;
            }}
            h1, h2 {{
                color: #2c5e4e;
            }}
            .pagina {{
                page-break-after: always;
            }}
            .assinatura {{
                margin-top: 50px;
                text-align: right;
                font-style: italic;
            }}
        </style>
        </head>
        <body>

        <div class="pagina">
            <h1>Steel Facility</h1>
            <h2>Informações da Obra</h2>
            <p><strong>Cliente:</strong> {cliente}</p>
            <p><strong>Área:</strong> {area:.0f} m²</p>
            <p><strong>Prazo:</strong> {dias} dias</p>
            <p><strong>Equipe:</strong> {funcionarios + 1} profissionais</p>

            <h2>Condições</h2>
            <p>Pagamento a combinar.<br>Início conforme disponibilidade do cliente.</p>
        </div>

        <div class="pagina">
            <h2>Proposta Financeira</h2>
            <ul>
                <li>Mão de obra: R${total_mao_obra:,.2f}</li>
                <li>Alimentação: R${total_alimentacao:,.2f}</li>
                <li>Hospedagem: R${total_hospedagem:,.2f}</li>
                <li>Deslocamento + Viagens: R${total_deslocamento + total_viagens:,.2f}</li>
                <li>Ferramentas: R${total_ferramentas:,.2f}</li>
                <li>Subtotal: R${subtotal:,.2f}</li>
                <li>Lucro ({lucro_perc * 100:.0f}%): R${lucro:,.2f}</li>
                <li><strong>Valor final: R${valor_final:,.2f}</strong></li>
            </ul>
            <div class="assinatura">___________________________<br>Assinatura responsável</div>
        </div>

        </body>
        </html>
        """

        pdf_gerado = gerar_pdf(cliente, html)

        with open(pdf_gerado, "rb") as f:
            st.download_button("📥 Baixar PDF da proposta", f, file_name=pdf_gerado)
