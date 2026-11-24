def validar_pontos(xs, ys):
    if len(xs) != len(ys):
        raise ValueError("Quantidade diferente de valores: x tem " + str(len(xs)) + " e f(x) tem " + str(len(ys)) + ".")

    if len(xs) < 2:
        raise ValueError("Informe pelo menos 2 pontos.")

    for i in range(len(xs)):
        for j in range(i + 1, len(xs)):
            if xs[i] == xs[j]:
                raise ValueError("Há valores de x repetidos (x = " + str(xs[i]) + "). Cada x deve aparecer uma vez.")

def lagrange(xs, ys, x):
    validar_pontos(xs, ys)

    n = len(xs)
    resultado = 0
    passos = []

    for i in range(n):
        Li = 1
        for j in range(n):
            if j != i:
                Li = Li * (x - xs[j]) / (xs[i] - xs[j])

        termo = ys[i] * Li
        resultado = resultado + termo

        passos.append((i, xs[i], ys[i], Li, termo))

    return resultado, passos

def newton_interpolacao(xs, ys, x):
    validar_pontos(xs, ys)

    n = len(xs)
    tabela = [list(ys)]

    for ordem in range(1, n):
        anterior = tabela[ordem - 1]
        coluna = []
        for i in range(n - ordem):
            numerador = anterior[i + 1] - anterior[i]
            denominador = xs[i + ordem] - xs[i]
            coluna.append(numerador / denominador)
        tabela.append(coluna)

    coeficientes = []
    for coluna in tabela:
        coeficientes.append(coluna[0])

    resultado = coeficientes[0]
    produto = 1
    for k in range(1, n):
        produto = produto * (x - xs[k - 1])
        resultado = resultado + coeficientes[k] * produto

    return resultado, tabela, coeficientes