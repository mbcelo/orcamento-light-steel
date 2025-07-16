import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
import app_gerador_pdf

st.set_page_config(page_title="🔐 Login Steel Facility", layout="centered")

# Carrega config
with open('config_login.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

# Cria autenticação
authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)

# Login
name, authentication_status, username = authenticator.login("Login", "main")

if authentication_status:
    authenticator.logout("🚪 Logout", "sidebar")
    st.sidebar.success(f"Logado como: {name}")
    app_gerador_pdf.executar_app()

elif authentication_status is False:
    st.error("Usuário ou senha incorretos")

elif authentication_status is None:
    st.warning("Insira suas credenciais")

# Registro de usuário (opcional)
with st.expander("✍️ Registrar novo usuário"):
    new_username = st.text_input("Novo usuário")
    new_name = st.text_input("Nome completo")
    new_email = st.text_input("Email")
    new_password = st.text_input("Senha", type="password")

    if st.button("Registrar"):
        if all([new_username, new_name, new_email, new_password]):
            new_hashed_pw = stauth.Hasher([new_password]).generate()[0]
            config['credentials']['usernames'][new_username] = {
                'name': new_name,
                'email': new_email,
                'password': new_hashed_pw
            }

            with open('config_login.yaml', 'w') as file:
                yaml.dump(config, file, default_flow_style=False)
            st.success(f"Usuário '{new_username}' registrado com sucesso!")
        else:
            st.warning("Preencha todos os campos para registrar")
