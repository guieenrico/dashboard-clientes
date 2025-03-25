import streamlit as st
import requests
from datetime import datetime, timedelta

# ========== CONFIGURAÇÕES ==========
st.set_page_config(
    page_title="Enrico Tráfego Profissional",
    page_icon="📊",
    layout="wide"
)

# ========== DADOS DA META ==========
ACCESS_TOKEN = "EAAQym7OJhWgBO3m2qvjKHBHiF0J2aZCGNcae9qaSz6OuwMQ8fXmJPkXacu3wAcHXrxGaXTOjsWwZCPP5MK9G6Q0ac1ZBPl5WSk3nP5OLqao0ZBwTXMXKgrvGHkXhgcj2Pzeaf2RGbVz2JH9HzMUXKmL73XQCMXKsPPhtphuqjZBGCZBoV7ZBHeU2NhT9BqetK45PtswOVZCPvMcKbHwZD"
AD_ACCOUNT_ID = "act_1060262399036879"

# ========== CHAMAR A API ==========
def get_facebook_insights():
    url = f"https://graph.facebook.com/v18.0/{AD_ACCOUNT_ID}/insights"
    params = {
        "access_token": ACCESS_TOKEN,
        "fields": "campaign_name,spend,impressions,reach,actions",
        "date_preset": "last_30d",
        "level": "campaign"
    }
    response = requests.get(url, params=params)
    return response.json()

# ========== COLETAR DADOS ==========
dados = get_facebook_insights()

# ========== INTERFACE ==========
st.image("https://raw.githubusercontent.com/guieenrico/dashboard-clientes/main/logo-branca.png", width=250)
st.markdown("## Enrico Tráfego Profissional")
st.markdown("### Relatório de Campanhas via API do Facebook")

st.markdown("---")

if "data" in dados:
    for campanha in dados["data"]:
        st.subheader(f'📊 {campanha["campaign_name"]}')
        st.write(f'**Gasto**: R$ {float(campanha["spend"]):,.2f}')
        st.write(f'**Impressões**: {campanha["impressions"]}')
        st.write(f'**Alcance**: {campanha["reach"]}')
        acoes = campanha.get("actions", [])
        for acao in acoes:
            st.write(f'{acao["action_type"].capitalize()}: {acao["value"]}')
        st.markdown("---")
else:
    st.error("Não foi possível carregar os dados da API. Verifique o token ou a conta de anúncios.")
