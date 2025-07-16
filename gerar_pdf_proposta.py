import pdfkit

def gerar_html(cliente, area, dias, funcionarios, total_mao_obra,
               total_alimentacao, total_hospedagem, total_deslocamento,
               total_viagens, total_ferramentas, subtotal, lucro,
               valor_final, lucro_perc):

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
    return html

def gerar_pdf(cliente, html):
    filename = f"proposta_{cliente.replace(' ', '_')}.pdf"
    pdfkit.from_string(html, filename)
    print(f"✅ PDF gerado: {filename}")
