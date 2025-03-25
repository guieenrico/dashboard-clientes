
import streamlit as st
import pandas as pd
import plotly.express as px

# Carregar os dados
df = pd.read_csv("dados.csv")

# Sidebar para selecionar cliente (simulado)
clientes = df["cliente"].unique()
cliente_selecionado = st.sidebar.selectbox("Selecione o cliente", clientes)

# Filtrar os dados
df_cliente = df[df["cliente"] == cliente_selecionado]

st.title("Dashboard de Tráfego Profissional")
st.subheader(f"Cliente: {cliente_selecionado}")

col1, col2, col3 = st.columns(3)
col1.metric("Total Gasto", f'R$ {df_cliente["gasto"].sum():,.2f}')
col2.metric("Total de Compras", int(df_cliente["compras"].sum()))
col3.metric("ROAS Médio", f'{df_cliente["roas"].mean():.2f}')

# Gráfico de barras ROAS por campanha
fig = px.bar(df_cliente, x="campanha", y="roas", title="ROAS por Campanha", color="campanha")
st.plotly_chart(fig)

# Tabela completa
st.subheader("Dados Detalhados")
st.dataframe(df_cliente)
