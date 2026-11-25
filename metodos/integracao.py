from utils import converter_numero


# ---------- Regra do Trapézio Repetida ----------
# I = h/2 * [ f(x0) + 2*f(x1) + ... + 2*f(x_m-1) + f(xm) ]

def trapezio_repetido(funcao, limite_a, limite_b, subintervalos):
    if limite_a >= limite_b:
        raise ValueError("O limite inferior (a) deve ser menor que o limite superior (b).")
    if subintervalos < 1:
        raise ValueError("O número de subintervalos deve ser pelo menos 1.")

    largura = (limite_b - limite_a) / subintervalos

    pontos = []          # cada ponto: (i, x, f(x), coeficiente)
    soma = 0.0

    for i in range(subintervalos + 1):
        x = limite_a + i * largura
        valor = funcao(x)

        # Extremos entram 1 vez; pontos do meio entram 2 vezes
        if i == 0 or i == subintervalos:
            coeficiente = 1
        else:
            coeficiente = 2

        soma = soma + coeficiente * valor
        pontos.append((i, x, valor, coeficiente))

    integral = largura / 2 * soma
    return integral, pontos, largura


# ---------- Regra 1/3 de Simpson Repetida ----------
# I = h/3 * [ f(x0) + 4*f(x1) + 2*f(x2) + 4*f(x3) + ... + 4*f(x_m-1) + f(xm) ]
# Exige número PAR de subintervalos

def simpson_repetido(funcao, limite_a, limite_b, subintervalos):
    if limite_a >= limite_b:
        raise ValueError("O limite inferior (a) deve ser menor que o limite superior (b).")
    if subintervalos < 2:
        raise ValueError("Na regra de Simpson o número de subintervalos deve ser pelo menos 2.")
    if subintervalos % 2 != 0:
        raise ValueError("Na regra 1/3 de Simpson o número de subintervalos deve ser PAR.")

    largura = (limite_b - limite_a) / subintervalos

    pontos = []          # cada ponto: (i, x, f(x), coeficiente)
    soma = 0.0

    for i in range(subintervalos + 1):
        x = limite_a + i * largura
        valor = funcao(x)

        # Extremos: 1  |  posições ímpares: 4  |  posições pares do meio: 2
        if i == 0 or i == subintervalos:
            coeficiente = 1
        elif i % 2 == 1:
            coeficiente = 4
        else:
            coeficiente = 2

        soma = soma + coeficiente * valor
        pontos.append((i, x, valor, coeficiente))

    integral = largura / 3 * soma
    return integral, pontos, largura


# ---------- Caso discreto (tabela de valores de x e f(x)) ----------

def ler_lista_de_numeros(texto, nome):
    # Transforma "0 5 10 15" em [0.0, 5.0, 10.0, 15.0]
    lista = []
    for valor in texto.replace(";", " ").split():
        lista.append(converter_numero(valor, nome))

    if len(lista) == 0:
        raise ValueError("Informe os valores de " + nome + ".")
    return lista


def integracao_discreta(valores_x, valores_y):
    if len(valores_x) != len(valores_y):
        raise ValueError("x e f(x) devem ter a mesma quantidade de valores (x tem "
                         + str(len(valores_x)) + " e f(x) tem " + str(len(valores_y)) + ").")
    if len(valores_x) < 2:
        raise ValueError("São necessários pelo menos 2 pontos.")

    subintervalos = len(valores_x) - 1

    # Os valores de x precisam estar em ordem crescente
    for i in range(subintervalos):
        if valores_x[i + 1] <= valores_x[i]:
            raise ValueError("Os valores de x devem estar em ordem crescente (sem repetir).")

    # Verifica se o espaçamento é igual entre todos os pontos
    largura = valores_x[1] - valores_x[0]
    espacamento_igual = True
    for i in range(subintervalos):
        if abs((valores_x[i + 1] - valores_x[i]) - largura) > 0.000001 * largura:
            espacamento_igual = False

    if espacamento_igual and subintervalos % 2 == 0:
        # Simpson 1/3: coeficientes 1, 4, 2, 4, ..., 4, 1
        soma = valores_y[0] + valores_y[subintervalos]
        for i in range(1, subintervalos):
            if i % 2 == 1:
                soma = soma + 4 * valores_y[i]
            else:
                soma = soma + 2 * valores_y[i]

        integral = largura / 3 * soma
        metodo_usado = "Simpson 1/3 repetida (espaçamento h = " + str(round(largura, 6)) + ")"

    else:
        # Trapézio: soma a área de cada trapézio entre pontos vizinhos
        integral = 0.0
        for i in range(subintervalos):
            base = valores_x[i + 1] - valores_x[i]
            integral = integral + base * (valores_y[i] + valores_y[i + 1]) / 2

        if espacamento_igual:
            motivo = "número ímpar de subintervalos"
        else:
            motivo = "espaçamento irregular"
        metodo_usado = "Trapézios (" + motivo + ")"

    return integral, metodo_usado