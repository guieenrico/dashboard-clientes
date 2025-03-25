import streamlit as st
import requests
import pandas as pd
import plotly.express as px

# ========== CONFIG ==========
st.set_page_config(page_title="Enrico Tráfego Profissional", page_icon="📊", layout="wide")
ACCESS_TOKEN = "EAAQym7OJhWgBO0ZCZAIP0fUAc4Aie8cRPOEUZADUjAFQLZB5p7Da63sZAFTjig1SdGZCgfc06mPaSNoZAsspnnz95DZAyBK12VvgE8hmNetbtECYkZB1UpOZBLv1fzKB60HpdEFbAdlopOESzcuHJoXCVwlckI3OAosg1qaeUUpAvPW26VxzqDIYKzeTPgoSADClHixrj1ZCb2GZBe2yQVAZD"
AD_ACCOUNT_ID = "1060262399036879"

# ========== HEADER ==========
col_logo, col_title = st.columns([1, 4])
with col_logo:
    st.image("https://raw.githubusercontent.com/guieenrico/dashboard-clientes/main/logo-branca.png", width=140)
with col_title:
    st.markdown("# Enrico Tráfego Profissional")
    st.markdown("### Relatório de Campanhas via API do Facebook")
st.markdown("---")

# ========== BUSCAR CAMPANHAS ==========
campaigns_url = f"https://graph.facebook.com/v18.0/act_{AD_ACCOUNT_ID}/campaigns"
params = {"access_token": ACCESS_TOKEN, "fields": "name", "limit": 100}
resp = requests.get(campaigns_url, params=params).json()
campaigns = resp.get("data", [])

if not campaigns:
    st.warning("Nenhuma campanha foi encontrada. Verifique se o token e a conta de anúncios estão corretos.")
    st.stop()

campaign_names = {camp["name"]: camp["id"] for camp in campaigns}
selected_campaign = st.selectbox("Escolha a campanha:", list(campaign_names.keys()))

# ========== BUSCAR DADOS DA CAMPANHA ==========
def get_campaign_insights(campaign_id):
    insights_url = f"https://graph.facebook.com/v18.0/{campaign_id}/insights"
    fields = ",".join([
        "spend",
        "impressions",
        "reach",
        "actions"
    ])
    params = {
        "access_token": ACCESS_TOKEN,
        "fields": fields,
        "date_preset": "lifetime",
        "limit": 1
    }
    res = requests.get(insights_url, params=params).json()
    return res.get("data", [])

data = get_campaign_insights(campaign_names[selected_campaign])

if not data:
    st.warning("Nenhum dado encontrado para esta campanha.")
    st.stop()

info = data[0]
spend = float(info.get("spend", 0))
impressions = int(info.get("impressions", 0))
reach = int(info.get("reach", 0))
actions = info.get("actions", [])

# ========== FORMATAR AÇÕES ==========
actions_dict = {a["action_type"]: int(a["value"]) for a in actions}

# ========== EXIBIR MÉTRICAS ==========
st.markdown(f"## 📊 {selected_campaign}")
col1, col2, col3 = st.columns(3)
col1.metric("💸 Gasto", f"R$ {spend:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
col2.metric("👁️ Impressões", f"{impressions:,}".replace(",", "."))
col3.metric("📍 Alcance", f"{reach:,}".replace(",", "."))

st.markdown("### ✅ Resultados da campanha")
for tipo, valor in actions_dict.items():
    st.markdown(f"- **{tipo.replace('_', ' ').capitalize()}**: {valor}")

# ========== GRÁFICO ==========
df_chart = pd.DataFrame.from_dict(actions_dict, orient='index', columns=['Quantidade']).reset_index()
df_chart.columns = ['Ação', 'Quantidade']
fig = px.bar(df_chart, x="Ação", y="Quantidade", color="Ação", text="Quantidade")
fig.update_traces(textposition='outside')
fig.update_layout(yaxis_title="Quantidade", xaxis_title="Tipo de Ação")
st.plotly_chart(fig, use_container_width=True)

# ========== RODAPÉ ==========
st.markdown("---")
st.markdown("<p style='text-align: center;'>Desenvolvido por <b>Enrico Tráfego Profissional</b> • Relatório via API da Meta</p>", unsafe_allow_html=True)
