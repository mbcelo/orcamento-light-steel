import streamlit_authenticator as stauth

# Substitua por sua senha real
hashed = stauth.Hasher(['minha_senha_segura']).generate()
print(hashed)
