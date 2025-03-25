import streamlit as st
import pandas as pd
import plotly.express as px

# ========== CONFIGURAÇÕES ========== #
st.set_page_config(page_title="Enrico Tráfego Profissional", page_icon="📊", layout="wide")

# ========== LOGO E TÍTULO ========== #
col_logo, col_titulo = st.columns([1, 4])
with col_logo:
    st.image("https://raw.githubusercontent.com/guieenrico/dashboard-clientes/main/logo-branca.png", width=200)
with col_titulo:
    st.markdown("## Enrico Tráfego Profissional")
    st.markdown("### Painel de Resultados de Campanhas")

st.markdown("---")

# ========== DADOS ========== #
df = pd.read_csv("[Ricci-Burguer-Feliz-Natal-2-+-Bysell]-Campanhas-1-de-mar-de-2025-25-de-mar-de-2025.csv")

# ========== SELECIONAR CAMPANHA ========== #
campanhas = df["Nome da campanha"].unique()
campanha_selecionada = st.selectbox("🧠 Escolha a campanha", campanhas)
df_campanha = df[df["Nome da campanha"] == campanha_selecionada].copy()

# ========== MÉTRICAS ========== #
st.markdown(f"### 📊 Dados da campanha: **{campanha_selecionada}**")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Gasto", f'R$ {df_campanha["Valor usado (BRL)"].sum():,.2f}')
col2.metric("Total de Compras", int(df_campanha["Compras"].sum()))
col3.metric("ROAS Médio", f'{df_campanha["Retorno sobre o investimento em publicidade (ROAS) das compras"].mean():.2f}')
col4.metric("💰 Valor de Vendas", f'R$ {df_campanha["Valor de conversão da compra"].sum():,.2f}')

# ========== GRÁFICO ========== #
st.markdown("### 📈 ROAS por Campanha")
fig = px.bar(df, x="Nome da campanha", y="Retorno sobre o investimento em publicidade (ROAS) das compras",
             color="Nome da campanha", text="Retorno sobre o investimento em publicidade (ROAS) das compras")
fig.update_traces(texttemplate='%{text:.2f}', textposition='outside')
fig.update_layout(yaxis_title="ROAS", xaxis_title="Campanha")
st.plotly_chart(fig, use_container_width=True)

# ========== TABELA ========== #
st.markdown("### 📋 Dados Detalhados")
st.dataframe(df_campanha, use_container_width=True)

# ========== RODAPÉ ========== #
st.markdown("---")
st.markdown("<p style='text-align: center; font-size: 14px;'>Desenvolvido por <b>Enrico Tráfego Profissional</b> • Painel versão beta</p>", unsafe_allow_html=True)
