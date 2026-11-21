import streamlit as st

from utils import criar_funcao, criar_derivada, converter_numero, converter_inteiro
from metodos.raizes import bissecao, falsa_posicao, newton, secante

def mostrar_aba_raizes():
    # ----- Escolha do método e da função -----
    metodo = st.selectbox("Método", ["Bissecção", "Falsa Posição", "Newton-Raphson", "Secante"])

    texto_funcao = st.text_input("f(x) =", "x**2 - 2")
    st.caption("Exemplos: x**3 - 9*x + 3  |  cos(x) - x  |  exp(-x) - x  (use ** para potência)")

    # ----- Campos que dependem do método escolhido -----
    col1, col2 = st.columns(2)
    if metodo == "Bissecção" or metodo == "Falsa Posição":
        texto_a = col1.text_input("a (início do intervalo)", "1")
        texto_b = col2.text_input("b (fim do intervalo)", "2")
    elif metodo == "Newton-Raphson":
        texto_x0 = col1.text_input("x0 (chute inicial)", "1")
    else:
        texto_x0 = col1.text_input("x0", "1")
        texto_x1 = col2.text_input("x1", "2")

    # ----- Campos comuns a todos os métodos -----
    col3, col4 = st.columns(2)
    texto_tol = col3.text_input("Tolerância", "0.000001")
    texto_max = col4.text_input("Máx. iterações", "100")

    # ----- Botão de calcular -----
    if not st.button("Calcular"):
        return

    try:
        # Dados comuns a todos os métodos
        f = criar_funcao(texto_funcao)
        tol = converter_numero(texto_tol, "Tolerância")
        max_iter = converter_inteiro(texto_max, "Máx. iterações")
        if tol <= 0 or max_iter < 1:
            raise ValueError("A tolerância deve ser maior que zero e o máximo de iterações pelo menos 1.")

        # Dados e execução de cada método
        if metodo == "Bissecção" or metodo == "Falsa Posição":
            colunas = ["k", "a", "b", "c", "f(c)", "erro"]
            a = converter_numero(texto_a, "a")
            b = converter_numero(texto_b, "b")
            if a >= b:
                raise ValueError("O valor de a deve ser menor que o valor de b.")
            if metodo == "Bissecção":
                raiz, iteracoes = bissecao(f, a, b, tol, max_iter)
            else:
                raiz, iteracoes = falsa_posicao(f, a, b, tol, max_iter)

        elif metodo == "Newton-Raphson":
            colunas = ["k", "x", "f(x)", "f'(x)", "x_novo", "erro"]
            x0 = converter_numero(texto_x0, "x0")
            df = criar_derivada(texto_funcao)
            raiz, iteracoes = newton(f, df, x0, tol, max_iter)

        else:
            colunas = ["k", "x0", "x1", "x2", "f(x2)", "erro"]
            x0 = converter_numero(texto_x0, "x0")
            x1 = converter_numero(texto_x1, "x1")
            raiz, iteracoes = secante(f, x0, x1, tol, max_iter)

    except ValueError as erro:
        mensagem = str(erro)
        if mensagem == "math domain error":
            mensagem = "A função não está definida em algum ponto testado (ex.: log de número negativo)."
        st.error(mensagem)
        return
    except Exception:
        st.error("A função não pôde ser calculada em algum ponto (ex.: divisão por zero).")
        return

    # ----- Mostra o resultado -----
    st.success("Raiz aproximada: " + str(raiz) + "  (" + str(len(iteracoes)) + " iterações)")

    # Monta a tabela: cada linha é um dicionário {nome da coluna: valor}
    tabela = []
    for iteracao in iteracoes:
        linha = {}
        for nome, numero in zip(colunas, iteracao):
            linha[nome] = f"{numero:.8g}"
        tabela.append(linha)

    st.dataframe(tabela, hide_index=True)