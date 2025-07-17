import streamlit as st
import json
import os

st.set_page_config(page_title="📋 Clientes Cadastrados", layout="wide")
st.title("📋 Histórico de Clientes - Steel Facility")

# Identifique o usuário atual
usuario_logado = st.text_input("Usuário logado", value="", placeholder="Digite seu nome de usuário")

if usuario_logado:
    caminho = os.path.join("clientes", f"{usuario_logado}_clientes.json")

    if os.path.exists(caminho):
        with open(caminho, "r", encoding="utf-8") as f:
            clientes = json.load(f)

        st.success(f"{len(clientes)} cliente(s) cadastrados por '{usuario_logado}'")

        for i, cliente in enumerate(clientes, 1):
            with st.expander(f"👤 Cliente {i}: {cliente['nome']}"):
                st.write(f"**Endereço:** {cliente['endereco']}")
                st.write(f"**Email:** {cliente['email']}")
                st.write(f"**Celular:** {cliente['celular']}")

                # Aqui você pode inserir botão para criar proposta com esse cliente
                # ou abrir em outro módulo
    else:
        st.info(f"Nenhum cliente encontrado para '{usuario_logado}'")
else:
    st.warning("Digite o nome de usuário para visualizar os clientes salvos")
