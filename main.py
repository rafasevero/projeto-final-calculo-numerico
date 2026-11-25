import streamlit as st

from interface.aba_raizes import mostrar_aba_raizes
from interface.aba_sistemas import mostrar_aba_sistemas
from interface.aba_interpolacao import mostrar_aba_interpolacao
from interface.aba_integracao import mostrar_aba_integracao

# Configura a página
st.set_page_config(page_title="Cálculo Numérico", layout="wide")
st.title("Cálculo Numérico")

# Cria as abas
abas = st.tabs(["Raízes", "Sistemas Lineares", "Interpolacao", "Integração"])
# Conteúdo de cada aba
with abas[0]:
    mostrar_aba_raizes()
with abas[1]:
    mostrar_aba_sistemas()
with abas[2]:
    mostrar_aba_interpolacao()
with abas[3]:
    mostrar_aba_integracao()

# Quando as outras abas ficarem prontas:
# abas = st.tabs(["Raízes", "Sistemas Lineares", "Interpolação", "Integração"])
# with abas[1]:
#     mostrar_aba_sistemas()