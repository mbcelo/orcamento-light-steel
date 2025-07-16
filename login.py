import streamlit as st
import pandas as pd
import hashlib
import os
from PIL import Image

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def carregar_usuarios():
    if os.path.exists("usuarios.csv"):
        return pd.read_csv("usuarios.csv")
    else:
        return pd.DataFrame(columns=["usuario", "senha_hash"])

def autenticar(usuario, senha, df):
    senha_hash = hash_password(senha)
    return not df[(df["usuario"] == usuario) & (df["senha_hash"] == senha_hash)].empty

def tela_login_cliente():
    col1, col2 = st.columns([1, 3])
    with col1:
        st.image("logo.png", width=180)
    with col2:
        st.markdown("## Bem-vindo à Steel Facility")
        st.markdown("Selecione abaixo se deseja **entrar** ou **cadastrar novo usuário** para acessar sua proposta personalizada.")

    escolha = st.radio("Acesso", ["Entrar", "Cadastrar novo usuário"])
    df_usuarios = carregar_usuarios()

    if escolha == "Entrar":
        usuario = st.text_input("Usuário")
        senha = st.text_input("Senha", type="password")
        if st.button("Entrar"):
            if autenticar(usuario, senha, df_usuarios):
                st.session_state["usuario_logado"] = usuario
                st.success(f"Olá, {usuario}! A proposta está carregando…")
            else:
                st.error("Usuário ou senha incorretos.")

    elif escolha == "Cadastrar novo usuário":
        novo_usuario = st.text_input("Novo usuário")
        nova_senha = st.text_input("Nova senha", type="password")
        if st.button("Cadastrar"):
            if novo_usuario and nova_senha:
                senha_hash = hash_password(nova_senha)
                novo_dado = pd.DataFrame([[novo_usuario, senha_hash]], columns=["usuario", "senha_hash"])
                df_usuarios = pd.concat([df_usuarios, novo_dado], ignore_index=True)
                df_usuarios.to_csv("usuarios.csv", index=False)
                st.success("Usuário cadastrado com sucesso!")
            else:
                st.warning("Preencha todos os campos.")