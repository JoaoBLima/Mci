import numpy as np
import math
from prettytable import PrettyTable  # Para formatar a saída como tabela

# Definição da função f(x) = x + 2 + sin(x) e sua derivada f'(x) = 1 + cos(x)
f = lambda x: x + 2 + np.sin(x)
df = lambda x: 1 + np.cos(x)

#------------------------------------------------------------------------------#
# MÉTODO DA BISSECÇÃO
def metodo_bissecao(f, a, b, erro):
    if f(a) * f(b) >= 0:
        raise ValueError("O intervalo [a, b] não satisfaz o Teorema de Bolzano.")

    iteracoes = 0
    tabela = PrettyTable(["Iteração", "a", "f(a)", "b", "f(b)", "c", "f(c)", "Erro Absoluto", "Erro Relativo"])
    c_anterior = None

    while True:
        iteracoes += 1
        c = (a + b) / 2
        fa = f(a)
        fb = f(b)
        fc = f(c)
        erro_absoluto = abs((b - a))
        erro_relativo = abs((c - c_anterior) / c) if c_anterior is not None and c != 0 else float('inf')

        tabela.add_row([
            iteracoes, round(a, 4), round(fa, 6), round(b, 4), round(fb, 6), 
            round(c, 4), round(fc, 6), round(erro_absoluto, 6), round(erro_relativo, 6)
        ])

        if f(c) == 0 or erro_absoluto < erro:
            break
        elif f(a) * f(c) < 0:
            b = c
        else:
            a = c

        c_anterior = c

    return tabela, round(c, 6), iteracoes

#------------------------------------------------------------------------------#
# MÉTODO DA SECANTE
def metodo_secante(f, x0, x1, tol=1e-6, max_iter=100):
    tabela = PrettyTable(["Iteração", "x0", "f(x0)", "x1", "f(x1)", "x2", "f(x2)", "Erro Absoluto", "Erro Relativo"])

    for i in range(max_iter):
        f_x0 = f(x0)
        f_x1 = f(x1)
        if f_x1 - f_x0 == 0:
            raise ValueError("Divisão por zero no método da secante.")

        x2 = x1 - (f_x1 * (x1 - x0)) / (f_x1 - f_x0)
        f_x2 = f(x2)
        erro_absoluto = abs(x2 - x1)
        erro_relativo = abs((x2 - x1) / x2) if x2 != 0 else float('inf')
        tabela.add_row([i+1, round(x0, 6), round(f_x0, 6), round(x1, 6), round(f_x1, 6), round(x2, 6), round(f_x2, 6), round(erro_absoluto, 6), round(erro_relativo, 6)])

        if erro_absoluto < tol:
            return tabela, round(x2, 6), i + 1

        x0, x1 = x1, x2

    raise Exception("O método da secante não convergiu após o número máximo de iterações.")

#------------------------------------------------------------------------------#
# MÉTODO DE NEWTON-RAPHSON
def metodo_newton(f, df, x0, tol, max_iter=100):
    iteracoes = 0
    tabela = PrettyTable(["Iteração", "x_n", "f(x_n)", "f'(x_n)", "Erro Absoluto", "Erro Relativo"])

    while iteracoes < max_iter:
        iteracoes += 1
        fx = f(x0)
        dfx = df(x0)

        if dfx == 0:
            raise ValueError("Derivada zero encontrada. O método falhou.")

        x1 = x0 - fx / dfx
        erro_absoluto = abs(x1 - x0)
        erro_relativo = abs((x1 - x0) / x1) if x1 != 0 else float('inf')

        tabela.add_row([iteracoes, round(x0, 6), round(fx, 6), round(dfx, 6), round(erro_absoluto, 6), round(erro_relativo, 6)])

        if erro_absoluto < tol:
            return tabela, round(x1, 6), iteracoes

        x0 = x1

    raise Exception("O método de Newton-Raphson não convergiu após o número máximo de iterações.")
