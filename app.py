import streamlit as st
import requests

# ========== CONFIG ==========
st.set_page_config(page_title="Enrico Tráfego Profissional", page_icon="📊", layout="wide")

# ========== LOGO ==========
st.markdown("""
<div style="text-align: center;">
    <img src="https://raw.githubusercontent.com/guieenrico/dashboard-clientes/main/logo-branca.png" width="300"/>
</div>
""", unsafe_allow_html=True)

st.markdown("<h2 style='text-align: center;'>Relatório de Campanhas via API do Facebook</h2>", unsafe_allow_html=True)
st.markdown("---")

# ========== TOKEN E CONFIG ==========
access_token = "EAAQym7OJhWgBOxZC5zYGhxMYPJUqSaZBj4yZAuvmMnOlIpvpK7wRSHo1hyhTT6PvbLFgToRucZAZBD1s23azDdZAuNFIEQcV2zoa6swp94W8mjZBVnw4Yy9qERKKve1z6F0ASYmqVQ5jx2ErUsynFM4LCHaklOQVFnyH7DxsOVqrJ6HiuQXizNymtNN7ReZBUuDulAuxOPRoEb2XYYEbQ98dXJyMZBBbiHwG5"
ad_account_id = "act_1060262399036879"

# ========== BUSCA DE CAMPANHAS ==========
def buscar_lista_campanhas():
    url = f"https://graph.facebook.com/v19.0/{ad_account_id}/campaigns"
    params = {
        "fields": "name",
        "access_token": access_token
    }
    resposta = requests.get(url, params=params).json()
    campanhas = resposta.get("data", [])
    return campanhas

campanhas = buscar_lista_campanhas()
nomes_campanhas = [campanha["name"] for campanha in campanhas] if campanhas else []
campaign_name = st.selectbox("Escolha a campanha:", nomes_campanhas)

# ========== BUSCA DE DADOS ==========
def buscar_dados_da_campanha(nome_campanha):
    campanha_id = None
    for campanha in campanhas:
        if campanha["name"].lower() == nome_campanha.lower():
            campanha_id = campanha["id"]
            break

    if not campanha_id:
        return None, f"Nenhum dado encontrado para a campanha: {nome_campanha}"

    url_detalhes = f"https://graph.facebook.com/v19.0/{campanha_id}/insights"
    params_detalhes = {
        "access_token": access_token,
        "fields": "campaign_name,spend,impressions,reach,actions",
        "level": "campaign",
        "time_increment": 0
    }

    dados = requests.get(url_detalhes, params=params_detalhes).json()
    return dados.get("data", []), None

# ========== EXIBIÇÃO ==========
dados, erro = buscar_dados_da_campanha(campaign_name)

if erro:
    st.warning(erro)
elif dados:
    dados = dados[0]

    st.markdown(f"### 📊 {dados.get('campaign_name')}")
    st.markdown(f"**💸 Gasto:** R$ {float(dados.get('spend', 0)):,.2f}")
    st.markdown(f"**📢 Impressões:** {dados.get('impressions', '-')}")
    st.markdown(f"**👥 Alcance:** {dados.get('reach', '-')}")

    # Listar ações específicas
    if "actions" in dados:
        for acao in dados["actions"]:
            nome = acao["action_type"]
            valor = acao["value"]
            st.markdown(f"**{nome.replace('_', ' ').capitalize()}:** {valor}")
else:
    st.info("Buscando dados...")
