
import streamlit as st
import pandas as pd
import plotly.express as px

# ========== CONFIGURAÇÕES ==========
st.set_page_config(
    page_title="Enrico Tráfego Profissional",
    page_icon="📊",
    layout="wide"
)

# ========== LOGO ==========
col_logo, col_titulo = st.columns([1, 4])
with col_logo:
    st.image("logo-clara.png", width=260)
with col_titulo:
    st.markdown("## Enrico Tráfego Profissional")
    st.markdown("### Painel de Resultados de Campanhas")

# ========== BOTÃO WHATSAPP ==========
link_painel = "https://painel.enricotrafegoprofissional.com.br"
mensagem = f"Olá! Acesse seu painel de resultados: {link_painel}"
url_whatsapp = f"https://wa.me/?text={mensagem.replace(' ', '%20')}"

st.markdown(f'''
    <a href="{url_whatsapp}" target="_blank">
        <button style="background-color:#25D366;color:white;padding:10px 20px;border:none;border-radius:5px;font-size:16px;margin-top:10px">
            📲 Compartilhar no WhatsApp
        </button>
    </a>
''', unsafe_allow_html=True)

st.markdown("---")

# ========== CARREGAR DADOS ==========
df = pd.read_csv("dados.csv")
clientes = df["cliente"].unique()
cliente_selecionado = st.sidebar.selectbox("🧑‍💼 Selecione o cliente", clientes)
df_cliente = df[df["cliente"] == cliente_selecionado]
tipo = df_cliente["tipo_cliente"].iloc[0]

# ========== MÉTRICAS POR TIPO DE CLIENTE ==========
st.markdown(f"### 📊 Dados do cliente: **{cliente_selecionado}**")
if tipo == "ecom":
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Gasto", f'R$ {df_cliente["gasto"].sum():,.2f}')
    col2.metric("Total de Compras", int(df_cliente["compras"].sum()))
    col3.metric("ROAS Médio", f'{df_cliente["roas"].mean():.2f}')
    col4.metric("💰 Valor de Vendas", f'R$ {df_cliente["valor_conversao"].sum():,.2f}')

elif tipo in ["imovel", "branding_leads"]:
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Gasto", f'R$ {df_cliente["gasto"].sum():,.2f}')
    col2.metric("Leads", int(df_cliente["leads"].sum()))
    col3.metric("Alcance", int(df_cliente["alcance"].sum()))
    col4.metric("Freq. Média", f'{df_cliente["freq"].mean():.2f}')

    st.markdown("### 👥 Novas Pessoas Alcançadas")
    st.metric("Total", int(df_cliente["novas_pessoas"].sum()))

# ========== GRÁFICO ==========
st.markdown("### 📊 Gráfico por Campanha")
coluna_grafico = "roas" if tipo == "ecom" else "leads"
fig = px.bar(df_cliente, x="campanha", y=coluna_grafico, color="campanha", text=coluna_grafico)
fig.update_traces(texttemplate='%{text:.2f}', textposition='outside')
fig.update_layout(yaxis_title=coluna_grafico.upper(), xaxis_title="Campanha")
st.plotly_chart(fig, use_container_width=True)

# ========== TABELA ==========
st.markdown("### 📋 Dados Detalhados")
st.dataframe(df_cliente, use_container_width=True)

# ========== RODAPÉ ==========
st.markdown("---")
st.markdown(
    "<p style='text-align: center; font-size: 14px;'>Desenvolvido por <b>Enrico Tráfego Profissional</b> • Painel versão beta</p>",
    unsafe_allow_html=True
)
