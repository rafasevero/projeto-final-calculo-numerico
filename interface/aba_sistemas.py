import streamlit as st

from utils import converter_numero, converter_inteiro
from metodos.sistemas import (ler_matriz, ler_vetor, eliminacao_gauss, fatoracao_lu,
                              gauss_seidel, criterio_linhas, criterio_sassenfeld)


def mostrar_vetor(nome, vetor):
    # Mostra y1 = ..., y2 = ..., ou x1 = ..., x2 = ...
    for posicao in range(len(vetor)):
        st.write(nome + str(posicao + 1) + " = " + format(vetor[posicao], ".6f"))


def mostrar_aba_sistemas():
    # ----- Escolha do método e dos dados -----
    metodo = st.selectbox("Método", ["Eliminação de Gauss", "Fatoração LU", "Gauss-Seidel"],
                          key="sis_metodo")

    texto_matriz = st.text_area("Matriz A (uma linha por linha, números separados por espaço)",
                                "3 -2 5\n6 -9 12\n-5 0 2", key="sis_matriz")
    texto_vetor = st.text_input("Vetor b (números separados por espaço)", "20 51 1", key="sis_vetor")

    # ----- Campos que dependem do método -----
    usar_pivoteamento = True
    if metodo == "Eliminação de Gauss":
        usar_pivoteamento = st.checkbox("Usar pivoteamento parcial", value=True, key="sis_pivoteamento")

    if metodo == "Gauss-Seidel":
        col1, col2, col3 = st.columns(3)
        texto_chute = col1.text_input("Chute inicial x(0)", "0 0 0", key="sis_chute")
        texto_tolerancia = col2.text_input("Tolerância", "0.001", key="sis_tolerancia")
        texto_max = col3.text_input("Máx. iterações", "100", key="sis_max")

    # ----- Botão de calcular -----
    if not st.button("Calcular", key="sis_calcular"):
        return

    try:
        matriz = ler_matriz(texto_matriz)
        vetor = ler_vetor(texto_vetor, len(matriz), "b")

        if metodo == "Eliminação de Gauss":
            solucao = eliminacao_gauss(matriz, vetor, usar_pivoteamento)

        elif metodo == "Fatoração LU":
            solucao, matriz_L, matriz_U, y = fatoracao_lu(matriz, vetor)

        else:
            chute = ler_vetor(texto_chute, len(matriz), "x(0)")
            tolerancia = converter_numero(texto_tolerancia, "Tolerância")
            max_iteracoes = converter_inteiro(texto_max, "Máx. iterações")
            if tolerancia <= 0 or max_iteracoes < 1:
                raise ValueError("A tolerância deve ser maior que zero e o máximo de iterações pelo menos 1.")

            solucao, iteracoes = gauss_seidel(matriz, vetor, chute, tolerancia, max_iteracoes)
            valor_linhas = criterio_linhas(matriz)
            valor_sassenfeld = criterio_sassenfeld(matriz)

    except ValueError as erro:
        st.error(str(erro))
        return

    # ----- Mostra o resultado -----
    if metodo == "Fatoração LU":
        st.subheader("Matriz L")
        st.dataframe(matriz_L)

        st.subheader("Matriz U")
        st.dataframe(matriz_U)

        st.subheader("Passo 1: resolvendo L·y = b")
        mostrar_vetor("y", y)

        st.subheader("Passo 2: resolvendo U·x = y")
        mostrar_vetor("x", solucao)

    elif metodo == "Gauss-Seidel":
        st.subheader("Critérios de convergência")
        if valor_linhas < 1:
            st.write("Critério das linhas: " + format(valor_linhas, ".4f") + " < 1 (satisfeito)")
        else:
            st.write("Critério das linhas: " + format(valor_linhas, ".4f") + " ≥ 1 (não satisfeito)")
        if valor_sassenfeld < 1:
            st.write("Critério de Sassenfeld: " + format(valor_sassenfeld, ".4f") + " < 1 (satisfeito)")
        else:
            st.write("Critério de Sassenfeld: " + format(valor_sassenfeld, ".4f") + " ≥ 1 (não satisfeito)")

        st.subheader("Iterações")
        tabela = []
        for rodada, valores, erro in iteracoes:
            linha = {"k": rodada}
            for posicao in range(len(valores)):
                linha["x" + str(posicao + 1)] = f"{valores[posicao]:.8g}"
            linha["erro relativo"] = f"{erro:.8g}"
            tabela.append(linha)
        st.dataframe(tabela, hide_index=True)

        st.subheader("Solução aproximada")
        mostrar_vetor("x", solucao)

    else:
        st.subheader("Solução")
        mostrar_vetor("x", solucao)