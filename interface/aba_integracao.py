import streamlit as st

from utils import criar_funcao, converter_numero, converter_inteiro
from metodos.integracao import (trapezio_repetido, simpson_repetido,
                                integracao_discreta, ler_lista_de_numeros)


def mostrar_aba_integracao():
    # ----- Escolha do método -----
    metodo = st.selectbox("Método", ["Regra do Trapézio Repetida",
                                     "Regra 1/3 de Simpson Repetida",
                                     "Caso discreto (dados tabelados)"],
                          key="int_metodo")

    # ----- Campos que dependem do método -----
    if metodo == "Caso discreto (dados tabelados)":
        texto_x = st.text_input("Valores de x (separados por espaço)", "0 5 10 15 20", key="int_x")
        texto_y = st.text_input("Valores de f(x) (separados por espaço)", "0 32.5 130 292.5 520", key="int_y")
    else:
        texto_funcao = st.text_input("f(x) =", "exp(x)", key="int_funcao")
        st.caption("Exemplos: exp(x)  |  x**2 + 1  |  sin(x)  (use ** para potência)")

        col1, col2, col3 = st.columns(3)
        texto_a = col1.text_input("a (limite inferior)", "0", key="int_a")
        texto_b = col2.text_input("b (limite superior)", "1", key="int_b")
        texto_m = col3.text_input("Subintervalos (m)", "10", key="int_m")
        if metodo == "Regra 1/3 de Simpson Repetida":
            st.caption("No Simpson, m deve ser par.")

    # ----- Botão de calcular -----
    if not st.button("Calcular", key="int_calcular"):
        return

    try:
        if metodo == "Caso discreto (dados tabelados)":
            valores_x = ler_lista_de_numeros(texto_x, "x")
            valores_y = ler_lista_de_numeros(texto_y, "f(x)")
            integral, metodo_usado = integracao_discreta(valores_x, valores_y)

        else:
            funcao = criar_funcao(texto_funcao)
            limite_a = converter_numero(texto_a, "a")
            limite_b = converter_numero(texto_b, "b")
            subintervalos = converter_inteiro(texto_m, "Subintervalos (m)")

            if metodo == "Regra do Trapézio Repetida":
                integral, pontos, largura = trapezio_repetido(funcao, limite_a, limite_b, subintervalos)
            else:
                integral, pontos, largura = simpson_repetido(funcao, limite_a, limite_b, subintervalos)

    except ValueError as erro:
        mensagem = str(erro)
        if mensagem == "math domain error":
            mensagem = "A função não está definida em algum ponto do intervalo (ex.: log de número negativo)."
        st.error(mensagem)
        return
    except Exception:
        st.error("A função não pôde ser calculada em algum ponto (ex.: divisão por zero).")
        return

    # ----- Mostra o resultado -----
    if metodo == "Caso discreto (dados tabelados)":
        st.write("Método utilizado: " + metodo_usado)

        tabela = []
        for i in range(len(valores_x)):
            tabela.append({"i": i, "xi": f"{valores_x[i]:.8g}", "f(xi)": f"{valores_y[i]:.8g}"})
        st.dataframe(tabela, hide_index=True)

    else:
        st.write("h = (b - a) / m = " + format(largura, ".6g"))

        tabela = []
        for i, x, valor, coeficiente in pontos:
            tabela.append({"i": i, "xi": f"{x:.8g}", "f(xi)": f"{valor:.8g}", "coeficiente": coeficiente})
        st.dataframe(tabela, hide_index=True)

    st.success("Integral aproximada = " + format(integral, ".8f"))