import streamlit as st
import hashlib

st.set_page_config(page_title="🔐 Gerador de Senha Hash", layout="centered")
st.title("🔐 Gerador de Senha com Hash SHA256")

st.markdown("Digite uma senha abaixo para gerar o hash correspondente e usá-la no seu sistema de login:")

senha = st.text_input("Senha a ser convertida", type="password")

if senha:
    hash_senha = hashlib.sha256(senha.encode()).hexdigest()
    st.markdown("### 🔎 Hash Gerado:")
    st.code(hash_senha, language="text")
    st.success("Copie este hash e cole no arquivo `usuarios.csv` junto com o nome e tipo do usuário.")
else:
    st.info("Digite a senha acima para gerar o hash.")