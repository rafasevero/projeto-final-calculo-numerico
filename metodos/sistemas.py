from utils import converter_numero


# ---------- Leitura dos dados (texto -> números) ----------

def ler_matriz(texto):
    # Cada linha do texto é uma linha da matriz; números separados por espaço
    linhas_do_texto = []
    for linha in texto.strip().splitlines():
        if linha.strip() != "":
            linhas_do_texto.append(linha)

    if len(linhas_do_texto) == 0:
        raise ValueError("Informe a matriz dos coeficientes.")

    matriz = []
    for numero_linha in range(len(linhas_do_texto)):
        linha_de_numeros = []
        for valor in linhas_do_texto[numero_linha].replace(";", " ").split():
            nome_do_campo = "A (linha " + str(numero_linha + 1) + ")"
            linha_de_numeros.append(converter_numero(valor, nome_do_campo))
        matriz.append(linha_de_numeros)

    tamanho = len(matriz)
    for numero_linha in range(tamanho):
        if len(matriz[numero_linha]) != tamanho:
            raise ValueError("A matriz deve ser quadrada: " + str(tamanho) + " linhas exigem "
                             + str(tamanho) + " colunas (a linha " + str(numero_linha + 1)
                             + " tem " + str(len(matriz[numero_linha])) + ").")
    return matriz


def ler_vetor(texto, tamanho_esperado, nome):
    vetor = []
    for valor in texto.replace(";", " ").split():
        vetor.append(converter_numero(valor, nome))

    if len(vetor) != tamanho_esperado:
        raise ValueError("O vetor '" + nome + "' deve ter " + str(tamanho_esperado)
                         + " elementos (você informou " + str(len(vetor)) + ").")
    return vetor


# ---------- Substituições (resolvem sistemas triangulares) ----------

def substituicao_regressiva(matriz_triangular, termos_independentes):
    # Resolve o sistema triangular SUPERIOR de baixo para cima
    tamanho = len(termos_independentes)
    solucao = [0.0] * tamanho

    for linha in range(tamanho - 1, -1, -1):
        soma_conhecida = 0.0
        for coluna in range(linha + 1, tamanho):
            soma_conhecida = soma_conhecida + matriz_triangular[linha][coluna] * solucao[coluna]

        solucao[linha] = (termos_independentes[linha] - soma_conhecida) / matriz_triangular[linha][linha]

    return solucao


def substituicao_progressiva(matriz_triangular_inferior, termos_independentes):
    # Resolve o sistema triangular INFERIOR de cima para baixo
    tamanho = len(termos_independentes)
    solucao = [0.0] * tamanho

    for linha in range(tamanho):
        soma_conhecida = 0.0
        for coluna in range(linha):
            soma_conhecida = soma_conhecida + matriz_triangular_inferior[linha][coluna] * solucao[coluna]

        solucao[linha] = (termos_independentes[linha] - soma_conhecida) / matriz_triangular_inferior[linha][linha]

    return solucao


# ---------- Eliminação de Gauss ----------

def eliminacao_gauss(matriz_coeficientes, vetor_termos, pivoteamento=True):
    tamanho = len(matriz_coeficientes)

    # Matriz aumentada: cada linha da matriz com o termo independente colado no final
    matriz_aumentada = []
    for linha in range(tamanho):
        matriz_aumentada.append(matriz_coeficientes[linha][:] + [vetor_termos[linha]])

    # Cada volta é um estágio: zera a coluna "estagio" nas linhas abaixo do pivô
    for estagio in range(tamanho - 1):

        # Pivoteamento: procura a linha com o maior valor (em módulo) nesta coluna
        if pivoteamento:
            linha_do_maior = estagio
            for linha in range(estagio + 1, tamanho):
                if abs(matriz_aumentada[linha][estagio]) > abs(matriz_aumentada[linha_do_maior][estagio]):
                    linha_do_maior = linha

            if linha_do_maior != estagio:
                # Troca as duas linhas de lugar
                linha_temporaria = matriz_aumentada[estagio]
                matriz_aumentada[estagio] = matriz_aumentada[linha_do_maior]
                matriz_aumentada[linha_do_maior] = linha_temporaria

        pivo = matriz_aumentada[estagio][estagio]
        if abs(pivo) < 0.000000001:
            raise ValueError("Pivô nulo no estágio " + str(estagio + 1) +
                             ". O sistema não tem solução única (ou ative o pivoteamento).")

        # Para cada linha abaixo do pivô: linha = linha - multiplicador * linha_do_pivo
        for linha in range(estagio + 1, tamanho):
            multiplicador = matriz_aumentada[linha][estagio] / pivo

            for coluna in range(estagio, tamanho + 1):
                matriz_aumentada[linha][coluna] = (matriz_aumentada[linha][coluna]
                                                   - multiplicador * matriz_aumentada[estagio][coluna])

    # Confere o último pivô (o laço acima não chegou nele)
    if abs(matriz_aumentada[tamanho - 1][tamanho - 1]) < 0.000000001:
        raise ValueError("Pivô nulo no último estágio. O sistema não tem solução única.")

    # Separa a matriz triangular dos termos independentes
    matriz_triangular = []
    termos_independentes = []
    for linha in range(tamanho):
        matriz_triangular.append(matriz_aumentada[linha][:tamanho])
        termos_independentes.append(matriz_aumentada[linha][tamanho])

    return substituicao_regressiva(matriz_triangular, termos_independentes)


# ---------- Fatoração LU ----------

def fatoracao_lu(matriz_coeficientes, vetor_termos):
    tamanho = len(matriz_coeficientes)

    # L começa como matriz identidade (1 na diagonal, 0 no resto)
    matriz_L = []
    for linha in range(tamanho):
        nova_linha = []
        for coluna in range(tamanho):
            if linha == coluna:
                nova_linha.append(1.0)
            else:
                nova_linha.append(0.0)
        matriz_L.append(nova_linha)

    # U começa como uma cópia de A (e vai virar triangular)
    matriz_U = []
    for linha in range(tamanho):
        matriz_U.append(matriz_coeficientes[linha][:])

    # Mesma eliminação do Gauss
    for estagio in range(tamanho - 1):
        pivo = matriz_U[estagio][estagio]
        if abs(pivo) < 0.000000001:
            raise ValueError("Pivô nulo no estágio " + str(estagio + 1) +
                             ". Não é possível fatorar sem trocar linhas.")

        for linha in range(estagio + 1, tamanho):
            multiplicador = matriz_U[linha][estagio] / pivo

            # A diferença para o Gauss: guardamos o multiplicador em L
            matriz_L[linha][estagio] = multiplicador

            # Esta posição vira zero por definição (evita resto de arredondamento)
            matriz_U[linha][estagio] = 0.0

            for coluna in range(estagio + 1, tamanho):
                matriz_U[linha][coluna] = matriz_U[linha][coluna] - multiplicador * matriz_U[estagio][coluna]

    if abs(matriz_U[tamanho - 1][tamanho - 1]) < 0.000000001:
        raise ValueError("Pivô nulo no último estágio. O sistema não tem solução única.")

    # Resolve L·y = b e depois U·x = y
    y = substituicao_progressiva(matriz_L, vetor_termos)
    solucao = substituicao_regressiva(matriz_U, y)

    return solucao, matriz_L, matriz_U, y


# ---------- Gauss-Seidel (método iterativo) ----------

def criterio_linhas(matriz_coeficientes):
    # Para cada linha: soma dos módulos fora da diagonal / módulo da diagonal.
    # O critério vale se o MAIOR desses valores for menor que 1.
    tamanho = len(matriz_coeficientes)
    maior_razao = 0.0

    for linha in range(tamanho):
        soma_fora_da_diagonal = 0.0
        for coluna in range(tamanho):
            if coluna != linha:
                soma_fora_da_diagonal = soma_fora_da_diagonal + abs(matriz_coeficientes[linha][coluna])

        razao = soma_fora_da_diagonal / abs(matriz_coeficientes[linha][linha])
        if razao > maior_razao:
            maior_razao = razao

    return maior_razao


def criterio_sassenfeld(matriz_coeficientes):
    # Parecido com o das linhas, mas usa os betas já calculados nas linhas de cima
    tamanho = len(matriz_coeficientes)
    betas = []

    for linha in range(tamanho):
        soma = 0.0
        for coluna in range(linha):
            soma = soma + betas[coluna] * abs(matriz_coeficientes[linha][coluna])
        for coluna in range(linha + 1, tamanho):
            soma = soma + abs(matriz_coeficientes[linha][coluna])

        betas.append(soma / abs(matriz_coeficientes[linha][linha]))

    return max(betas)


def gauss_seidel(matriz_coeficientes, vetor_termos, chute_inicial, tolerancia, max_iteracoes=100):
    tamanho = len(matriz_coeficientes)

    for linha in range(tamanho):
        if abs(matriz_coeficientes[linha][linha]) < 0.000000001:
            raise ValueError("Há zero na diagonal (linha " + str(linha + 1) +
                             "). Troque a ordem das equações antes de usar Gauss-Seidel.")

    solucao = chute_inicial[:]
    iteracoes = []

    for rodada in range(1, max_iteracoes + 1):
        solucao_anterior = solucao[:]

        # Calcula cada incógnita usando os valores mais recentes
        for linha in range(tamanho):
            soma_outros_termos = 0.0
            for coluna in range(tamanho):
                if coluna != linha:
                    soma_outros_termos = soma_outros_termos + matriz_coeficientes[linha][coluna] * solucao[coluna]

            solucao[linha] = (vetor_termos[linha] - soma_outros_termos) / matriz_coeficientes[linha][linha]

        # Erro relativo: maior mudança / maior valor de x
        maior_mudanca = 0.0
        maior_valor = 0.0
        for posicao in range(tamanho):
            mudanca = abs(solucao[posicao] - solucao_anterior[posicao])
            if mudanca > maior_mudanca:
                maior_mudanca = mudanca
            if abs(solucao[posicao]) > maior_valor:
                maior_valor = abs(solucao[posicao])

        if maior_valor == 0:
            erro = maior_mudanca
        else:
            erro = maior_mudanca / maior_valor

        iteracoes.append((rodada, solucao[:], erro))

        if erro < tolerancia:
            return solucao, iteracoes

    raise ValueError("Não convergiu em " + str(max_iteracoes) + " iterações. "
                     "O sistema pode não satisfazer os critérios de convergência.")