import streamlit as st
import requests
import plotly.express as px

# ========== CONFIGURAÇÕES ==========
st.set_page_config(
    page_title="Enrico Tráfego Profissional",
    page_icon="📊",
    layout="wide"
)

# ========== LOGO E TÍTULOS ========== 
col_logo, col_titulo = st.columns([1, 4])
with col_logo:
    st.image("https://raw.githubusercontent.com/guieenrico/dashboard-clientes/main/logo-branca.png", width=180)
with col_titulo:
    st.markdown("## Enrico Tráfego Profissional")
    st.markdown("### Relatório de Campanhas via API do Facebook")

st.markdown("---")

# ========== TOKEN E ID ==========
ACCESS_TOKEN = "EAAQym7OJhWgBO3m2qvjKHBHiF0J2aZCGNcae9qaSz6OuwMQ8fXmJPkXacu3wAcHXrxGaXTOjsWwZCPP5MK9G6Q0ac1ZBPl5WSk3nP5OLqao0ZBwTXMXKgrvGHkXhgcj2Pzeaf2RGbVz2JH9HzMUXKmL73XQCMXKsPPhtphuqjZBGCZBoV7ZBHeU2NhT9BqetK45PtswOVZCPvMcKbHwZD"
AD_ACCOUNT_ID = "1060262399036879"

def get_campaigns():
    url = f"https://graph.facebook.com/v19.0/act_{AD_ACCOUNT_ID}/campaigns"
    params = {
        "fields": "name",
        "access_token": ACCESS_TOKEN
    }
    res = requests.get(url, params=params).json()
    return res.get("data", [])

def get_campaign_insights(campaign_id):
    url = f"https://graph.facebook.com/v19.0/{campaign_id}/insights"
    params = {
        "access_token": ACCESS_TOKEN,
        "fields": "campaign_name,spend,impressions,reach,actions",
        "level": "campaign",
        "time_increment": 1
    }
    res = requests.get(url, params=params).json()
    return res.get("data", [])

# ========== OBTÊM CAMPANHAS ==========
campaigns = get_campaigns()

if not campaigns:
    st.warning("Nenhuma campanha encontrada. Verifique o token e a conta de anúncio.")
    st.stop()

campaign_names = [c["name"] for c in campaigns]
campaign_ids = {c["name"]: c["id"] for c in campaigns}

selected_campaign_name = st.selectbox("Escolha a campanha:", campaign_names)
campaign_id = campaign_ids[selected_campaign_name]

insights = get_campaign_insights(campaign_id)

if not insights:
    st.warning("Nenhum dado encontrado para esta campanha.")
    st.stop()

data = insights[0]

gasto = float(data.get("spend", 0))
impressoes = int(data.get("impressions", 0))
alcance = int(data.get("reach", 0))
acoes = data.get("actions", [])

# Mapeia ações
acoes_dict = {a["action_type"]: int(a["value"]) for a in acoes}

# ========== MÉTRICAS ==========
st.markdown(f"### 📊 Dados da campanha: **{selected_campaign_name}**")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Gasto", f"R$ {gasto:,.2f}")
col2.metric("Impressões", f"{impressoes:,}")
col3.metric("Alcance", f"{alcance:,}")
col4.metric("👥 Compras", f"{acoes_dict.get('omni_purchase', 0)}")

# ========== TABELA DE EVENTOS ==========
st.markdown("### 🧾 Eventos Registrados")
for nome, valor in acoes_dict.items():
    st.markdown(f"- **{nome.replace('_', ' ').title()}**: {valor}")

# ========== GRÁFICO ========== 
st.markdown("### 📈 Gráfico de desempenho")
grafico_df = {
    "Métrica": list(acoes_dict.keys()),
    "Valor": list(acoes_dict.values())
}
fig = px.bar(grafico_df, x="Métrica", y="Valor", color="Métrica", text="Valor")
fig.update_traces(texttemplate='%{text}', textposition='outside')
fig.update_layout(xaxis_title="Evento", yaxis_title="Quantidade")
st.plotly_chart(fig, use_container_width=True)

# ========== RODAPÉ ========== 
st.markdown("---")
st.markdown(
    "<p style='text-align: center; font-size: 14px;'>Desenvolvido por <b>Enrico Tráfego Profissional</b> • Integração via API da Meta</p>",
    unsafe_allow_html=True
)
