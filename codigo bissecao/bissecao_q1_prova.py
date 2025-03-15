# MÉTODO DA BISSECÇÃO
import numpy as np
import pandas as pd
import math
from prettytable import PrettyTable

def metodo_bissecao(f, a, b, erro):
    """
    Implementação do método da bissecção com cálculo de erro absoluto e relativo.
    Agora exporta os resultados para uma planilha Excel.

    Parâmetros:
    - f: função (lambda ou def) para a qual queremos encontrar a raiz.
    - a: limite inferior do intervalo inicial.
    - b: limite superior do intervalo inicial.
    - erro: erro tolerado para a aproximação da raiz.

    Retorna:
    - Uma tabela com os resultados de cada iteração e a raiz aproximada.
    - Um arquivo Excel com os resultados.
    """

    if f(a) * f(b) >= 0:
        raise ValueError("Intervalo inválido! f(a) e f(b) devem ter sinais opostos.")

    iteracoes = 0
    tabela = PrettyTable(["Iteração", "a", "b", "c", "Erro Absoluto", "Erro Relativo"])
    c_anterior = None
    dados = []

    while True:
        iteracoes += 1
        c = (a + b) / 2
        
        erro_absoluto = abs(b - a)
        erro_relativo = abs((c - c_anterior) / c) if c_anterior is not None and c != 0 else float('inf')
        
        tabela.add_row([iteracoes, round(a, 6), round(b, 6), round(c, 6), round(erro_absoluto, 6), round(erro_relativo, 6)])
        dados.append([iteracoes, round(a, 6), round(b, 6), round(c, 6), round(erro_absoluto, 6), round(erro_relativo, 6)])
        
        if f(c) == 0:
            break
        elif f(a) * f(c) < 0:
            b = c
        else:
            a = c

        c_anterior = c

        if erro_absoluto < erro:
            break

    print(tabela)
    
    df = pd.DataFrame(dados, columns=["Iteração", "a", "b", "c", "Erro Absoluto", "Erro Relativo"])
    df.to_excel("bissecao_resultados.xlsx", index=False)
    print("\nOs resultados foram salvos no arquivo 'bissecao_resultados.xlsx'.")
    
    return c, iteracoes

if __name__ == "__main__":
    f = lambda x: x + 2 + math.sin(x)

    try:
        a = float(input("Digite o limite inferior do intervalo (a): "))
        b = float(input("Digite o limite superior do intervalo (b): "))
        erro = 0.0001

        raiz, num_iteracoes = metodo_bissecao(f, a, b, erro)
        print(f"Aproximação da raiz: {raiz}")
        print(f"Número de iterações: {num_iteracoes}")
    except ValueError as e:
        print(e)
