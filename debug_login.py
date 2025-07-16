import streamlit as st
import pandas as pd
import hashlib
import os

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def carregar_usuarios():
    if os.path.exists("usuarios.csv"):
        return pd.read_csv("usuarios.csv")
    else:
        return pd.DataFrame(columns=["usuario", "senha_hash", "tipo"])

st.title("🔍 Debug de Login - Steel Facility")

df = carregar_usuarios()
st.subheader("📋 Usuários carregados do arquivo CSV")
st.dataframe(df)

st.subheader("🧪 Teste de autenticação manual")

usuario_teste = st.text_input("Usuário de teste")
senha_teste = st.text_input("Senha de teste", type="password")

if usuario_teste and senha_teste:
    senha_hash_teste = hash_password(senha_teste)
    st.write(f"🔑 Hash gerado: `{senha_hash_teste}`")

    filtro = df[(df["usuario"] == usuario_teste)]
    if filtro.empty:
        st.error("❌ Usuário não encontrado no arquivo.")
    else:
        hash_real = filtro["senha_hash"].values[0]
        if senha_hash_teste == hash_real:
            st.success("✅ Autenticação bem-sucedida! Senha confere.")
            st.write(f"👤 Tipo de usuário: `{filtro['tipo'].values[0]}`")
        else:
            st.error("🔒 Senha incorreta para o usuário informado.")