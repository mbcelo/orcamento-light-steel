import streamlit as st
from PIL import Image
import pandas as pd
import hashlib
import os

# 🎨 Aparência geral
st.set_page_config(page_title="Orçamento Light Steel Frame", layout="wide")
logo = Image.open("logo.png")

# 🔐 Funções de autenticação
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
        st.image(logo, width=180)
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

# 🔒 Verificação de login
if "usuario_logado" not in st.session_state:
    tela_login_cliente()
    st.stop()

# 🎯 Início da interface do app após login
st.title("Orçamento de Projeto - Light Steel Frame 🏗️")

# 🔷 Informações do projeto
st.sidebar.header("Informações do Projeto")
cliente = st.sidebar.text_input("Nome do Cliente", value="Residencial Silva")
area = st.sidebar.number_input("Área da obra (m²)", min_value=0.0, value=450.0)
dias = st.sidebar.number_input("Prazo de execução (dias)", min_value=1, value=90)
funcionarios = st.sidebar.number_input("Nº de funcionários (exclui responsável)", min_value=1, value=4)
diaria_func = st.sidebar.number_input("Diária por funcionário (R$)", min_value=0.0, value=200.0)
diaria_resp = st.sidebar.number_input("Diária responsável técnico (R$)", min_value=0.0, value=300.0)

# 🍽️ Custos variáveis
st.sidebar.subheader("Custos diários")
almoco = st.sidebar.number_input("Valor almoço (R$)", value=30.0)
janta = st.sidebar.number_input("Valor janta (R$)", value=30.0)
hospedagem = st.sidebar.number_input("Valor hospedagem (R$)", value=70.0)
desloc_diario = st.sidebar.number_input("Deslocamento diário (R$)", value=30.0)

# 🛣️ Viagens
st.sidebar.subheader("Viagens periódicas")
dist_km = st.sidebar.number_input("Distância por viagem (km ida e volta)", value=110.0)
preco_km = st.sidebar.number_input("Valor por km (R$)", value=2.0)
num_viagens = st.sidebar.number_input("Nº de viagens", value=18)

# 🔧 Ferramentas
st.sidebar.subheader("Ferramentas")
ferramentas_mes = st.sidebar.number_input("Custo ferramentas/mês (R$)", value=5000.0)
meses = st.sidebar.number_input("Meses de uso", min_value=1, value=3)

# 💰 Lucro
lucro_perc = st.sidebar.slider("Percentual de lucro desejado", 0.0, 0.5, 0.25)

# 🧮 Cálculos
total_mao_obra = (funcionarios * diaria_func + diaria_resp) * dias
total_alimentacao = (almoco + janta) * dias * (funcionarios + 1)
total_hospedagem = hospedagem * dias * (funcionarios + 1)
total_deslocamento = desloc_diario * dias
total_viagens = dist_km * preco_km * num_viagens
total_ferramentas = ferramentas_mes * meses
subtotal = sum([
    total_mao_obra,
    total_alimentacao,
    total_hospedagem,
    total_deslocamento,
    total_viagens,
    total_ferramentas
])
lucro = subtotal * lucro_perc
valor_final = subtotal + lucro

# 📊 Visualização
st.header("Resumo do Orçamento")
st.metric("Subtotal", f"R${subtotal:,.2f}")
st.metric("Lucro estimado", f"R${lucro:,.2f}")
st.metric("Valor final do projeto", f"R${valor_final:,.2f}")

st.subheader("Detalhamento dos custos")
st.table({
    "Categoria": [
        "Mão de obra",
        "Alimentação",
        "Hospedagem",
        "Deslocamento diário",
        "Viagens",
        "Ferramentas"
    ],
    "Valor (R$)": [
        f"{total_mao_obra:,.2f}",
        f"{total_alimentacao:,.2f}",
        f"{total_hospedagem:,.2f}",
        f"{total_deslocamento:,.2f}",
        f"{total_viagens:,.2f}",
        f"{total_ferramentas:,.2f}"
    ]
})

# 📋 Proposta comercial gerada
st.subheader("Proposta Comercial")
proposta = f"""
Cliente: {cliente}
Área da obra: {area:.0f} m²
Prazo de execução: {dias} dias
Equipe: {funcionarios + 1} profissionais (inclui responsável técnico)

Custos estimados:
- Mão de obra direta: R${total_mao_obra:,.2f}
- Alimentação: R${total_alimentacao:,.2f}
- Hospedagem: R${total_hospedagem:,.2f}
- Deslocamento e viagens: R${total_deslocamento + total_viagens:,.2f}
- Ferramentas: R${total_ferramentas:,.2f}
Subtotal: R${subtotal:,.2f}
Lucro ({lucro_perc * 100:.0f}%): R${lucro:,.2f}

💬 Valor total da proposta: R${valor_final:,.2f}

Condições:
- Pagamento a combinar.
- Início previsto conforme disponibilidade do cliente.
"""

st.text_area("Texto da proposta", proposta, height=300)
