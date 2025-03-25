import streamlit as st
import requests

# ========== CONFIG ==========

st.set_page_config(page_title="Enrico Tráfego Profissional", page_icon="📊", layout="wide")

st.markdown("""
<div style="text-align: center;">
    <img src="https://raw.githubusercontent.com/guieenrico/dashboard-clientes/main/logo-branca.png" width="300"/>
</div>
""", unsafe_allow_html=True)

st.markdown("<h2 style='text-align: center;'>Relatório de Campanhas via API do Facebook</h2>", unsafe_allow_html=True)
st.markdown("---")

# ========== TOKEN E CONTA ==========

access_token = "EAAQym7OJhWgBOxZC5zYGhxMYPJUqSaZBj4yZAuvmMnOlIpvpK7wRSHo1hyhTT6PvbLFgToRucZAZBD1s23azDdZAuNFIEQcV2zoa6swp94W8mjZBVnw4Yy9qERKKve1z6F0ASYmqVQ5jx2ErUsynFM4LCHaklOQVFnyH7DxsOVqrJ6HiuQXizNymtNN7ReZBUuDulAuxOPRoEb2XYYEbQ98dXJyMZBBbiHwG5"
ad_account_id = "1060262399036879"

# ========== BUSCA TODAS AS CAMPANHAS ==========

url = f"https://graph.facebook.com/v19.0/act_{ad_account_id}/campaigns"
params = {
    "fields": "name",
    "access_token": access_token
}
response = requests.get(url, params=params).json()
campanhas = response.get("data", [])

# ========== SELECTBOX POR NOME ==========
nomes = [camp["name"] for camp in campanhas]
nome_escolhido = st.selectbox("Escolha a campanha:", nomes)

# ========== BUSCA ID SELECIONADO ==========
id_escolhido = next((camp["id"] for camp in campanhas if camp["name"] == nome_escolhido), None)

if not id_escolhido:
    st.warning("ID da campanha não encontrado.")
else:
    # ========== DADOS DA CAMPANHA ==========
    url_detalhes = f"https://graph.facebook.com/v19.0/{id_escolhido}/insights"
    params_detalhes = {
        "access_token": access_token,
        "fields": "campaign_name,spend,impressions,reach,actions",
        "level": "campaign",
        "time_increment": 0
    }

    dados = requests.get(url_detalhes, params=params_detalhes).json()
    resultados = dados.get("data", [])

    if resultados:
        dados = resultados[0]
        st.markdown(f"### 📊 {dados.get('campaign_name')}")
        st.markdown(f"**💸 Gasto:** R$ {float(dados.get('spend', 0)):,.2f}")
        st.markdown(f"**📢 Impressões:** {dados.get('impressions', '-')}")    
        st.markdown(f"**👥 Alcance:** {dados.get('reach', '-')}")

        if "actions" in dados:
            for acao in dados["actions"]:
                nome = acao["action_type"]
                valor = acao["value"]
                st.markdown(f"**{nome.replace('_', ' ').capitalize()}:** {valor}")
    else:
        st.warning("Nenhum dado encontrado para essa campanha.")
