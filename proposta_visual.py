import streamlit as st
import base64

def gerar_html_proposta(cliente, area, dias, funcionarios, total_mao_obra,
                        total_alimentacao, total_hospedagem, total_deslocamento,
                        total_viagens, total_ferramentas, subtotal, lucro,
                        valor_final, lucro_perc):

    html = f"""
    <html>
    <head>
    <style>
        body {{
            font-family: 'Segoe UI', sans-serif;
            margin: 0;
            padding: 40px;
            color: #333;
            background-color: #f7f9fa;
        }}
        .pagina {{
            page-break-after: always;
        }}
        h1, h2 {{
            color: #2c5e4e;
        }}
        .info, .valores {{
            margin-bottom: 30px;
        }}
        .valores ul {{
            list-style: none;
            padding: 0;
        }}
        .valores li {{
            padding: 6px 0;
            font-size: 16px;
        }}
        .assinatura {{
            margin-top: 60px;
            font-style: italic;
            text-align: right;
        }}
        .rodape {{
            text-align: center;
            font-size: 12px;
            color: #999;
            margin-top: 60px;
        }}
    </style>
    </head>
    <body>

    <div class="pagina">
        <h1>Steel Facility</h1>
        <h2>Informações da Obra</h2>
        <div class="info">
            <p><strong>Cliente:</strong> {cliente}</p>
            <p><strong>Área da obra:</strong> {area:.0f} m²</p>
            <p><strong>Prazo de execução:</strong> {dias} dias</p>
            <p><strong>Equipe:</strong> {funcionarios + 1} profissionais</p>
        </div>

        <h2>Condições Gerais</h2>
        <p>Pagamento a combinar.</p>
        <p>Início previsto conforme disponibilidade do cliente.</p>

        <div class="rodape">Página 1 de 2</div>
    </div>

    <div class="pagina">
        <h2>Proposta Financeira</h2>
        <div class="valores">
            <ul>
                <li>Mão de obra: <strong>R${total_mao_obra:,.2f}</strong></li>
                <li>Alimentação: <strong>R${total_alimentacao:,.2f}</strong></li>
                <li>Hospedagem: <strong>R${total_hospedagem:,.2f}</strong></li>
                <li>Deslocamento + viagens: <strong>R${total_deslocamento + total_viagens:,.2f}</strong></li>
                <li>Ferramentas: <strong>R${total_ferramentas:,.2f}</strong></li>
                <li>Subtotal: <strong>R${subtotal:,.2f}</strong></li>
                <li>Lucro ({lucro_perc * 100:.0f}%): <strong>R${lucro:,.2f}</strong></li>
                <li>Valor final: <strong>R${valor_final:,.2f}</strong></li>
            </ul>
        </div>

        <div class="assinatura">
            ____________________________<br>
            Assinatura responsável
        </div>

        <div class="rodape">Página 2 de 2</div>
    </div>

    </body>
    </html>
    """

    return html

def exportar_proposta_html(cliente, html_proposta):
    html_bytes = html_proposta.encode("utf-8")
    b64 = base64.b64encode(html_bytes).decode("utf-8")
    file_name = f"proposta_{cliente.replace(' ', '_')}.html"
    href = f'<a href="data:text/html;base64,{b64}" download="{file_name}">📥 Baixar proposta em HTML</a>'
    st.markdown(href, unsafe_allow_html=True)