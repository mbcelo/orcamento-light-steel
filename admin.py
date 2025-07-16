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

def painel_administrador():
    st.markdown("## Painel de Administração 👤🔐")
    df = carregar_usuarios()

    st.subheader("Usuários cadastrados:")
    if df.empty:
        st.info("Nenhum usuário cadastrado ainda.")
    else:
        for idx, row in df.iterrows():
            col1, col2, col3, col4 = st.columns([2, 2, 2, 1])
            with col1:
                st.write(f"👤 {row['usuario']}")
            with col2:
                nova_senha = st.text_input(f"Nova senha para {row['usuario']}", type="password", key=f"senha_{idx}")
                if nova_senha:
                    df.at[idx, 'senha_hash'] = hash_password(nova_senha)
                    df.to_csv("usuarios.csv", index=False)
                    st.success(f"Senha de '{row['usuario']}' atualizada com sucesso!")
            with col3:
                novo_tipo = st.selectbox(f"Tipo de {row['usuario']}", ["cliente", "admin"], index=["cliente", "admin"].index(row["tipo"]), key=f"tipo_{idx}")
                if novo_tipo != row["tipo"]:
                    df.at[idx, "tipo"] = novo_tipo
                    df.to_csv("usuarios.csv", index=False)
                    st.success(f"Tipo de '{row['usuario']}' atualizado para {novo_tipo}!")
            with col4:
                if st.button(f"Excluir", key=f"excluir_{idx}"):
                    df = df.drop(idx)
                    df.to_csv("usuarios.csv", index=False)
                    st.warning(f"Usuário '{row['usuario']}' excluído.")
                    st.experimental_rerun()

    st.markdown("---")
    st.subheader("Adicionar novo usuário:")
    novo_usuario = st.text