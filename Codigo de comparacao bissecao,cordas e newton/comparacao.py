#comparacao entre bissecao,cordas e newton
import numpy as np
import math
from prettytable import PrettyTable  # Para formatar a saída como tabela

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

        if f(c) == 0:
            break
        elif f(a) * f(c) < 0:
            b = c
        else:
            a = c

        c_anterior = c
        if erro_absoluto < erro:
            break

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

#------------------------------------------------------------------------------#
# FUNÇÃO PRINCIPAL PARA COMPARAÇÃO DOS MÉTODOS
if __name__ == "__main__":
    # Definindo a função f(x) = x * ln(x) - 1 e sua derivada f'(x) = ln(x) + 1
    f = lambda x: x + 2 + math.sin(x)
    df = lambda x: 1 + math.cos(x)

    try:
        # Entrada do usuário para Bissecção
        print("=== MÉTODO DA BISSECÇÃO ===")
        a = float(input("Digite o limite inferior do intervalo (a): "))
        b = float(input("Digite o limite superior do intervalo (b): "))
        erro_bissecao = float(input("Digite o erro tolerado: "))
        tabela_bissecao, raiz_bissecao, iteracoes_bissecao = metodo_bissecao(f, a, b, erro_bissecao)

        # Entrada do usuário para Secante
        print("\n=== MÉTODO DA SECANTE ===")
        x0_secante = float(input("Digite a primeira estimativa inicial (x0): "))
        x1_secante = float(input("Digite a segunda estimativa inicial (x1): "))
        tol_secante = float(input("Digite a tolerância: "))
        tabela_secante, raiz_secante, iteracoes_secante = metodo_secante(f, x0_secante, x1_secante, tol_secante)

        # Entrada do usuário para Newton-Raphson
        print("\n=== MÉTODO DE NEWTON-RAPHSON ===")
        x0_newton = float(input("Digite a estimativa inicial (x0): "))
        tol_newton = float(input("Digite a tolerância: "))
        tabela_newton, raiz_newton, iteracoes_newton = metodo_newton(f, df, x0_newton, tol_newton)

        # Exibe os resultados
        print("\n=== RESULTADOS DO MÉTODO DA BISSECÇÃO ===")
        print(tabela_bissecao)
        print(f"Aproximação da raiz: {raiz_bissecao}")
        print(f"Número de iterações: {iteracoes_bissecao}\n")

        print("=== RESULTADOS DO MÉTODO DA SECANTE ===")
        print(tabela_secante)
        print(f"Aproximação da raiz: {raiz_secante}")
        print(f"Número de iterações: {iteracoes_secante}\n")

        print("=== RESULTADOS DO MÉTODO DE NEWTON-RAPHSON ===")
        print(tabela_newton)
        print(f"Aproximação da raiz: {raiz_newton}")
        print(f"Número de iterações: {iteracoes_newton}\n")

        # Comparação final
        print("=== COMPARAÇÃO FINAL ===")
        print(f"Método da Bissecção     - Raiz: {raiz_bissecao}, Iterações: {iteracoes_bissecao}")
        print(f"Método da Secante       - Raiz: {raiz_secante}, Iterações: {iteracoes_secante}")
        print(f"Método de Newton-Raphson - Raiz: {raiz_newton}, Iterações: {iteracoes_newton}")

    except ValueError as e:
        print(e)
