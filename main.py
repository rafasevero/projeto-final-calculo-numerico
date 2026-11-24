import streamlit as st

from interface.aba_raizes import mostrar_aba_raizes
from interface.aba_sistemas import mostrar_aba_sistemas

# Configura a página
st.set_page_config(page_title="Cálculo Numérico", layout="wide")
st.title("Cálculo Numérico")

# Cria as abas
abas = st.tabs(["Raízes", "Sistemas Lineares"])
# Conteúdo de cada aba
with abas[0]:
    mostrar_aba_raizes()
with abas[1]:
    mostrar_aba_sistemas()

# Quando as outras abas ficarem prontas:
# abas = st.tabs(["Raízes", "Sistemas Lineares", "Interpolação", "Integração"])
# with abas[1]:
#     mostrar_aba_sistemas()