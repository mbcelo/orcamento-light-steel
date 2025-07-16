if st.session_state.etapa == "dados_cliente":
    st.subheader("👤 Dados do Cliente")

    nome = st.text_input("Nome completo")
    endereco = st.text_input("Endereço")
    email = st.text_input("Email")
    celular = st.text_input("Celular")

    if st.button("✅ Salvar cliente e avançar"):
        st.session_state.cliente_dados = {
            "nome": nome,
            "endereco": endereco,
            "email": email,
            "celular": celular
        }
        st.success(f"Cliente '{nome}' salvo com sucesso!")
        st.session_state.etapa = "dados_obra"  # Avança para próxima etapa
