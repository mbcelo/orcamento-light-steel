import streamlit as st
from gerador_pdf_simples import gerar_pdf

def executar_app():
    st.title("🧾 Gerador de Proposta - Steel Facility")

    # Etapa inicial
    if "etapa" not in st.session_state:
        st.session_state.etapa = "cliente"

    # Etapa 1 - Cadastro do Cliente
    if st.session_state.etapa == "cliente":
        st.subheader("👤 Dados do Cliente")
        nome = st.text_input("Nome completo")
        endereco = st.text_input("Endereço")
        email = st.text_input("Email")
        celular = st.text_input("Celular")

        if st.button("✅ Salvar cliente e avançar"):
            if all([nome, endereco, email, celular]):
                st.session_state.cliente = {
                    "nome": nome,
                    "endereco": endereco,
                    "email": email,
                    "celular": celular
                }
                st.success("Cliente salvo com sucesso!")
                st.session_state.etapa = "obra"
            else:
                st.warning("Preencha todos os campos")

    # Etapa 2 - Dados da Obra
    elif st.session_state.etapa == "obra":
        st.subheader("🏗️ Dados da Obra")
        area = st.number_input("Área (m²)", min_value=0.0)
        dias = st.number_input("Prazo (dias)", min_value=1)
        equipe = st.number_input("Nº de funcionários", min_value=1)

        if st.button("✅ Salvar dados da obra"):
            st.session_state.obra = {
                "area": area,
                "dias": dias,
                "equipe": equipe
            }
            st.session_state.etapa = "custos"

    # Etapa 3 - Custos
    elif st.session_state.etapa == "custos":
        st.subheader("💰 Custos da Proposta")
        mao_obra = st.number_input("Mão de obra", min_value=0.0)
        alimentacao = st.number_input("Alimentação", min_value=0.0)
        hospedagem = st.number_input("Hospedagem", min_value=0.0)
        deslocamento = st.number_input("Deslocamento", min_value=0.0)
        viagens = st.number_input("Viagens", min_value=0.0)
        ferramentas = st.number_input("Ferramentas", min_value=0.0)
        lucro_perc = st.slider("Margem de lucro (%)", 0, 100, 20) / 100

        if st.button("✅ Gerar PDF"):
            subtotal = sum([mao_obra, alimentacao, hospedagem, deslocamento, viagens, ferramentas])
            lucro = subtotal * lucro_perc
            total = subtotal + lucro

            cliente = st.session_state.cliente
            obra = st.session_state.obra

            html = f"""
            <html>
            <body style='font-family:Arial; padding:30px'>
                <h1>Proposta - Steel Facility</h1>
                <h2>👤 Cliente</h2>
                <p><strong>Nome:</strong> {cliente['nome']}</p>
                <p><strong>Endereço:</strong> {cliente['endereco']}</p>
                <p><strong>Email:</strong> {cliente['email']}</p>
                <p><strong>Celular:</strong> {cliente['celular']}</p>

                <h2>🏗️ Obra</h2>
                <p><strong>Área:</strong> {obra['area']} m²</p>
                <p><strong>Prazo:</strong> {obra['dias']} dias</p>
                <p><strong>Equipe:</strong> {obra['equipe']} profissionais</p>

                <h2>💰 Custos</h2>
                <ul>
                    <li>Mão de obra: R${mao_obra:.2f}</li>
                    <li>Alimentação: R${alimentacao:.2f}</li>
                    <li>Hospedagem: R${hospedagem:.2f}</li>
                    <li>Deslocamento: R${deslocamento:.2f}</li>
                    <li>Viagens: R${viagens:.2f}</li>
                    <li>Ferramentas: R${ferramentas:.2f}</li>
                    <li>Subtotal: R${subtotal:.2f}</li>
                    <li>Lucro ({lucro_perc * 100:.0f}%): R${lucro:.2f}</li>
                    <li><strong>Total:</strong> R${total:.2f}</li>
                </ul>
            </body>
            </html>
            """

            caminho_pdf = gerar_pdf(cliente["nome"], html)

            with open(caminho_pdf, "rb") as f:
                st.download_button("📥 Baixar proposta PDF", f, file_name=caminho_pdf)

            st.success("✅ Proposta gerada com sucesso!")
            st.session_state.etapa = "cliente"
