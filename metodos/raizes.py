from utils import criar_funcao, criar_derivada

def bissecao(f, a, b, tol, max_iter=100):
    fa = f(a)
    fb = f(b)

    if fa * fb > 0:
        raise ValueError("f(a) e f(b) têm o mesmo sinal. Escolha outro intervalo.")

    iteracoes = []

    for k in range(1, max_iter + 1):
        c = (a + b) / 2
        fc = f(c)

        erro = b - a
        iteracoes.append((k, a, b, c, fc, erro))

        if abs(fc) < tol:
            return c, iteracoes

        if erro < tol:
            return c, iteracoes

        if fa * fc < 0:
            b = c
            fb = fc
        else:
            a = c
            fa = fc

    raise ValueError("Não convergiu no número máximo de iterações.")

def falsa_posicao(f, a, b, tol, max_iter=100):
    fa = f(a)
    fb = f(b)

    if fa * fb > 0:
        raise ValueError("f(a) e f(b) têm o mesmo sinal. Escolha outro intervalo.")

    iteracoes = []

    c_anterior = None

    for k in range(1, max_iter + 1):

        denominador = fb - fa
        if abs(denominador) < 0.000000001:
            raise ValueError("f(a) e f(b) são iguais. Escolha outro intervalo.")

        c = (a * fb - b * fa) / denominador
        fc = f(c)

        if c_anterior is None:
            erro = abs(b - a)
        else:
            erro = abs(c - c_anterior)

        iteracoes.append((k, a, b, c, fc, erro))

        if abs(fc) < tol:
            return c, iteracoes

        if erro < tol:
            return c, iteracoes

        if fa * fc < 0:
            b = c
            fb = fc
        else:
            a = c
            fa = fc

        c_anterior = c

    raise ValueError("Não convergiu no número máximo de iterações.")

def newton(f, df, x0, tol, max_iter=100):
    iteracoes = []
    x = x0

    for k in range(1, max_iter + 1):
        fx = f(x)
        dfx = df(x)

        if abs(dfx) < 0.000000001:
            raise ValueError("Derivada igual a zero em x = " + str(x) + ". Escolha outro x0.")

        x_novo = x - fx / dfx
        erro = abs(x_novo - x)

        iteracoes.append((k, x, fx, dfx, x_novo, erro))

        if erro < tol:
            return x_novo, iteracoes

        if abs(f(x_novo)) < tol:
            return x_novo, iteracoes

        x = x_novo

    raise ValueError("Não convergiu no número máximo de iterações.")

def secante(f, x0, x1, tol, max_iter=100):
    iteracoes = []

    for k in range(1, max_iter + 1):

        f0 = f(x0)
        f1 = f(x1)

        denominador = f1 - f0
        if abs(denominador) < 0.000000001:
            raise ValueError("f(x0) e f(x1) são iguais. Escolha outras aproximações iniciais.")

        x2 = x1 - f1 * (x1 - x0) / denominador
        f2 = f(x2)

        erro = abs(x2 - x1)

        iteracoes.append((k, x0, x1, x2, f2, erro))

        if erro < tol:
            return x2, iteracoes

        if abs(f2) < tol:
            return x2, iteracoes

        x0 = x1
        x1 = x2

    raise ValueError("Não convergiu no número máximo de iterações.")
