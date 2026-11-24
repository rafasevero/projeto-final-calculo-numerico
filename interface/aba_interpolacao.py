import streamlit as st

from utils import converter_numero, converter_lista
from metodos.interpolacao import lagrange, newton_interpolacao

def mostrar_aba_interpolacao():
    metodo = st.selectbox("Método de interpolação", ["Lagrange", "Newton (diferenças divididas)"])

    texto_xs = st.text_input("Valores de x", "0 1 2 3")
    texto_ys = st.text_input("Valores de f(x)", "1 2 5 10")
    st.caption("Separe os valores por espaço. Use o mesmo número de valores em x e em f(x).")
    texto_x = st.text_input("x a interpolar", "1.5")

    if not st.button("Calcular interpolação"):
        return

    try:
        xs = converter_lista(texto_xs, "Valores de x")
        ys = converter_lista(texto_ys, "Valores de f(x)")
        x = converter_numero(texto_x, "x a interpolar")

        if metodo == "Lagrange":
            resultado, passos = lagrange(xs, ys, x)
        else:
            resultado, tabela_dd, coeficientes = newton_interpolacao(xs, ys, x)

    except ValueError as erro:
        st.error(str(erro))
        return

    st.success("P(" + str(x) + ") = " + str(resultado))

    if x < min(xs) or x > max(xs):
        st.warning("x está fora do intervalo dos pontos informados (extrapolação). O resultado pode ser pouco confiável.")

    if metodo == "Lagrange":
        st.write("Termos da soma: P(x) = soma de f(xᵢ)·Lᵢ(x)")
        tabela = []
        for passo in passos:
            linha = {}
            linha["i"] = str(passo[0])
            linha["xᵢ"] = f"{passo[1]:.8g}"
            linha["f(xᵢ)"] = f"{passo[2]:.8g}"
            linha["Lᵢ(x)"] = f"{passo[3]:.8g}"
            linha["f(xᵢ)·Lᵢ(x)"] = f"{passo[4]:.8g}"
            tabela.append(linha)
        st.dataframe(tabela, hide_index=True)

    else:
        st.write("Tabela de diferenças divididas (a coluna 'ordem k' tem as diferenças de ordem k)")
        n = len(xs)
        tabela = []
        for i in range(n):
            linha = {"x": f"{xs[i]:.8g}"}
            for ordem in range(n):
                nome = "ordem " + str(ordem)
                if i < len(tabela_dd[ordem]):
                    linha[nome] = f"{tabela_dd[ordem][i]:.8g}"
                else:
                    linha[nome] = ""
            tabela.append(linha)
        st.dataframe(tabela, hide_index=True)

        st.write("Polinômio: P(x) = c0 + c1(x - x0) + c2(x - x0)(x - x1) + ...")
        linhas = []
        for k in range(len(coeficientes)):
            linhas.append("c" + str(k) + " = " + f"{coeficientes[k]:.8g}")
        st.code("\n".join(linhas))