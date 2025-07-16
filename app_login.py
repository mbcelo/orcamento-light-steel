with st.expander("✍️ Registrar novo usuário"):
    new_username = st.text_input("Novo usuário")
    new_name = st.text_input("Nome completo")
    new_email = st.text_input("Email")
    new_password = st.text_input("Senha", type="password")
    confirm_password = st.text_input("Confirmar senha", type="password")

    if st.button("Registrar"):
        if not all([new_username, new_name, new_email, new_password, confirm_password]):
            st.warning("Preencha todos os campos!")
        elif new_password != confirm_password:
            st.error("As senhas não conferem")
        elif new_username in config['credentials']['usernames']:
            st.error("Este usuário já existe")
        else:
            # Gerar a senha criptografada
            hashed_pw = stauth.Hasher([new_password]).generate()[0]

            # Adicionar novo usuário
            config['credentials']['usernames'][new_username] = {
                'name': new_name,
                'email': new_email,
                'password': hashed_pw
            }

            # Salvar no config_login.yaml
            with open('config_login.yaml', 'w') as file:
                yaml.dump(config, file, default_flow_style=False)

            st.success(f"Usuário '{new_username}' registrado com sucesso!")
