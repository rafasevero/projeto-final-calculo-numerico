import math
import sympy

# A incógnita x, usada por todas as funções
x = sympy.Symbol("x")


def ler_expressao(texto):
    # Remove espaços das pontas
    texto = texto.strip()

    # Campo vazio é erro
    if texto == "":
        raise ValueError("Informe uma função.")

    # Transforma o texto em expressão matemática
    try:
        expressao = sympy.sympify(texto)
    except Exception:
        raise ValueError("Função inválida. Exemplo: x**3 - 9*x + 3")

    # Só pode existir a variável x na função
    outras_variaveis = expressao.free_symbols - {x}
    if len(outras_variaveis) > 0:
        raise ValueError("Use apenas a variável x na função.")

    return expressao


def criar_funcao(texto):
    # Lê e valida o texto
    expressao = ler_expressao(texto)

    # Transforma a expressão em uma função que recebe um número
    f = sympy.lambdify(x, expressao, "math")
    return f


def criar_derivada(texto):
    # Lê e valida o texto
    expressao = ler_expressao(texto)

    # Calcula a derivada em relação a x
    derivada = sympy.diff(expressao, x)

    # Transforma a derivada em uma função que recebe um número
    df = sympy.lambdify(x, derivada, "math")
    return df


def converter_numero(texto, nome):
    # Remove espaços e troca vírgula por ponto (2,5 vira 2.5)
    texto = texto.strip()
    texto = texto.replace(",", ".")

    # Campo vazio é erro
    if texto == "":
        raise ValueError("O campo '" + nome + "' não pode ficar vazio.")

    # Tenta converter o texto para número
    try:
        valor = float(texto)
    except ValueError:
        raise ValueError("O campo '" + nome + "' deve ser um número. Você digitou: " + texto)

    # float aceita as palavras "nan" e "inf", que não servem
    if math.isnan(valor) or math.isinf(valor):
        raise ValueError("O campo '" + nome + "' deve ser um número válido.")

    return valor


def converter_inteiro(texto, nome):
    # Primeiro converte para número
    valor = converter_numero(texto, nome)

    # Depois confere se não tem parte decimal (ex.: 2.5 não vale)
    if valor != int(valor):
        raise ValueError("O campo '" + nome + "' deve ser um número inteiro.")

    return int(valor)


def converter_lista(texto, nome):
    # Aceita separação por espaço ou ponto e vírgula (2,5 vira 2.5)
    texto = texto.replace(";", " ")
    texto = texto.replace(",", ".")
    partes = texto.split()

    # Lista vazia é erro
    if len(partes) == 0:
        raise ValueError("O campo '" + nome + "' não pode ficar vazio.")

    # Converte cada pedaço para número
    numeros = []
    for parte in partes:
        numeros.append(converter_numero(parte, nome))

    return numeros