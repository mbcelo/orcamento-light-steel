import streamlit as st
from gerador_pdf_simples import gerar_pdf
import json
import os

def executar_app(usuario_logado):
    st.set_page_config(page_title="🧾 Proposta Steel Facility", layout="centered")

    etapas = ["cliente", "obra", "custos", "proposta"]
    if "etapa_atual" not in st.session_state:
        st.session_state.etapa_atual = 0  # começa na etapa cliente

    etapa = etapas[st.session_state.etapa_atual]
    st.markdown(f"## Etapa {st.session_state.etapa_atual + 1} de {len(etapas)} — {etapa.capitalize()}")

    # Função para salvar cliente
    def salvar_cliente(usuario, dados):
        os.makedirs("clientes", exist_ok=True)
        caminho = os.path.join("clientes", f"{usuario}_clientes.json")
        try:
            with open(caminho, "r", encoding="utf-8") as f:
                clientes = json.load(f)
        except:
            clientes = []
        clientes.append(dados)
        with open(caminho, "w", encoding="utf-8") as f:
            json.dump(clientes, f, indent=2)

    # Etapa 1: Cliente
    if etapa == "cliente":
        nome = st.text_input("Nome completo")
        endereco = st.text_input("Endereço")
        email = st.text_input("Email")
        celular = st.text_input("Celular")

        col1, col2 = st.columns(2)
        with col1:
            if st.button("Avançar ➡️"):
                if all([nome, endereco, email, celular]):
                    st.session_state.cliente = {
                        "nome": nome,
                        "endereco": endereco,
                        "email": email,
                        "celular": celular
                    }
                    salvar_cliente(usuario_logado, st.session_state.cliente)
                    st.session_state.etapa_atual += 1
                else:
                    st.warning("Preencha todos os campos para continuar")

    # Etapa 2: Obra
    elif etapa == "obra":
        area = st.number_input("Área da obra (m²)", min_value=0.0)
        dias = st.number_input("Prazo (dias)", min_value=1)
        equipe = st.number_input("Funcionários envolvidos", min_value=1)

        col1, col2 = st.columns(2)
        with col1:
            if st.button("⬅️ Voltar"):
                st.session_state.etapa_atual -= 1
        with col2:
            if st.button("Avançar ➡️"):
                st.session_state.obra = {
                    "area": area,
                    "dias": dias,
                    "equipe": equipe
                }
                st.session_state.etapa_atual += 1

    # Etapa 3: Custos
    elif etapa == "custos":
        mao_obra = st.number_input("Mão de obra (R$)", min_value=0.0)
        alimentacao = st.number_input("Alimentação (R$)", min_value=0.0)
        hospedagem = st.number_input("Hospedagem (R$)", min_value=0.0)
        deslocamento = st.number_input("Deslocamento (R$)", min_value=0.0)
        viagens = st.number_input("Viagens (R$)", min_value=0.0)
        ferramentas = st.number_input("Ferramentas (R$)", min_value=0.0)
        lucro_perc = st.slider("Margem de lucro (%)", 0, 100, 20) / 100

        col1, col2 = st.columns(2)
        with col1:
            if st.button("⬅️ Voltar"):
                st.session_state.etapa_atual -= 1
        with col2:
            if st.button("Avançar ➡️"):
                st.session_state.custos = {
                    "mao_obra": mao_obra,
                    "alimentacao": alimentacao,
                    "hospedagem": hospedagem,
                    "deslocamento": deslocamento,
                    "viagens": viagens,
                    "ferramentas": ferramentas,
                    "lucro_perc": lucro_perc
                }
                st.session_state.etapa_atual += 1

    # Etapa 4: Proposta (geração do PDF)
    elif etapa == "proposta":
        cliente = st.session_state.cliente
        obra = st.session_state.obra
        custos = st.session_state.custos

        subtotal = sum([
            custos["mao_obra"],
            custos["alimentacao"],
            custos["hospedagem"],
            custos["deslocamento"],
            custos["viagens"],
            custos["ferramentas"]
        ])
        lucro = subtotal * custos["lucro_perc"]
        total = subtotal + lucro

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
                <li>Mão de obra: R${custos['mao_obra']:.2f}</li>
                <li>Alimentação: R${custos['alimentacao']:.2f}</li>
                <li>Hospedagem: R${custos['hospedagem']:.2f}</li>
                <li>Deslocamento + Viagens: R${custos['deslocamento'] + custos['viagens']:.2f}</li>
                <li>Ferramentas: R${custos['ferramentas']:.2f}</li>
                <li>Subtotal: R${subtotal:.2f}</li>
                <li>Lucro ({custos['lucro_perc'] * 100:.0f}%): R${lucro:.2f}</li>
                <li><strong>Total:</strong> R${total:.2f}</li>
            </ul>
        </body>
        </html>
        """

        caminho_pdf = gerar_pdf(cliente["nome"], html)
        st.success("✅ Proposta gerada com sucesso!")

        with open(caminho_pdf, "rb") as f:
            st.download_button("📥 Baixar proposta PDF", f, file_name=caminho_pdf)

        if st.button("🔄 Criar nova proposta"):
            st.session_state.etapa_atual = 0
            for chave in ["cliente", "obra", "custos"]:
                st.session_state.pop(chave, None)
