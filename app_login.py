import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
import app_gerador_pdf

st.set_page_config(page_title="🔐 Login - Steel Facility", layout="centered")

# Carregar config_login.yaml
with open('config_login.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

# Criar autenticação
authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)

name, authentication_status, username = authenticator.login("Login", "main")

if authentication_status:
    st.success(f"Bem-vindo, {name} 👷‍♂️")
    app_gerador_pdf.executar_app()

elif authentication_status is False:
    st.error("Usuário ou senha incorretos")

elif authentication_status is None:
    st.warning("Insira suas credenciais para acessar o app")
