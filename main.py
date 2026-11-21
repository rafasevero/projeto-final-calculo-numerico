import streamlit as st

from interface.aba_raizes import mostrar_aba_raizes

# Configura a página
st.set_page_config(page_title="Cálculo Numérico", layout="wide")
st.title("Cálculo Numérico")

# Cria as abas
abas = st.tabs(["Raízes"])

# Conteúdo de cada aba
with abas[0]:
    mostrar_aba_raizes()

# Quando as outras abas ficarem prontas:
# abas = st.tabs(["Raízes", "Sistemas Lineares", "Interpolação", "Integração"])
# with abas[1]:
#     mostrar_aba_sistemas()