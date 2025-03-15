import numpy as np
import math
from prettytable import PrettyTable  # Para formatar a saída como tabela

def metodo_newton(f, df, x0, tol):
    """
    Método de Newton-Raphson para encontrar a raiz de uma função.

    Parâmetros:
    - f: função para a qual queremos encontrar a raiz.
    - df: derivada da função f.
    - x0: estimativa inicial.
    - tol: erro tolerado para a aproximação da raiz.

    Retorna:
    - Aproximação da raiz e o número de iterações realizadas.
    """
    iteracoes = 0
    tabela = PrettyTable(["Iteração", "x_n", "f(x_n)", "f'(x_n)", "Erro Absoluto"])

    while True:
        iteracoes += 1
        fx = f(x0)
        dfx = df(x0)

        if dfx == 0:
            raise ValueError("Derivada zero encontrada. O método falhou.")

        x1 = x0 - fx / dfx
        erro_absoluto = abs(x1 - x0)

        # Adiciona a linha na tabela
        tabela.add_row([iteracoes, round(x0, 6), round(fx, 6), round(dfx, 6), round(erro_absoluto, 6)])

        if erro_absoluto <= tol:
            print(tabela)
            return x1, iteracoes

        x0 = x1

# Definindo a função f(x) = x + 2 + sin(x) e sua derivada
f = lambda x: x + 2 + math.sin(x)
df = lambda x: 1 + math.cos(x)

# Exemplo de uso
if __name__ == "__main__":
    try:
        x0 = float(input("Digite a estimativa inicial (x0): "))
        tol = float(input("Digite o erro tolerado (ex.: 0.001): "))

        raiz, num_iteracoes = metodo_newton(f, df, x0, tol)
        print(f"Aproximação da raiz: {raiz}")
        print(f"Número de iterações: {num_iteracoes}")
    except ValueError as e:
        print(e)
