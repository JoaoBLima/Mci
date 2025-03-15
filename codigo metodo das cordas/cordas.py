import numpy as np
import pandas as pd
from prettytable import PrettyTable  # Para formatar a saída como tabela

def metodo_secante(f, x0, x1, tol=1e-30, max_iter=100):
    """
    Implementação do método da secante para encontrar a raiz de uma função.
    Também gera uma planilha Excel com os resultados de cada iteração.
    """
    # Lista para armazenar os resultados
    resultados = []
    tabela = PrettyTable(["Iteração", "x0", "x1", "x2", "f(x2)"])

    for i in range(max_iter):
        f_x0 = f(x0)
        f_x1 = f(x1)
        if f_x1 - f_x0 == 0:
            raise ValueError("Divisão por zero no cálculo do método da secante.")

        x2 = x1 - (f_x1 * (x1 - x0)) / (f_x1 - f_x0)
        f_x2 = f(x2)
        
        # Armazena os resultados
        resultados.append([i + 1, x0, x1, x2, f_x2])
        tabela.add_row([i + 1, f"{x0:.20f}", f"{x1:.20f}", f"{x2:.20f}", f"{f_x2:.20f}"])
        
        if abs(x2 - x1) < tol:
            break
        x0, x1 = x1, x2

    # Exibir a tabela no console
    print(tabela)

    # Criar DataFrame e salvar como Excel
    df = pd.DataFrame(resultados, columns=["Iteração", "x0", "x1", "x2", "f(x2)"])
    df.to_excel("secante_resultados.xlsx", index=False)
    print("\nResultados salvos em 'secante_resultados.xlsx'\n")
    
    return round(x2, 6), len(resultados)

if __name__ == "__main__":
    # Definição da função (exemplo: f(x) = exp(-x) - cos(x))
    f = lambda t:75 * np.exp(-1.5 * t) + 20 * np.exp(-0.075 * t) - 15

    try:
        x0 = float(input("Digite a primeira estimativa inicial (x0): "))
        x1 = float(input("Digite a segunda estimativa inicial (x1): "))
        tol = float(input("Digite a tolerância desejada (ex.: 1e-6): "))

        raiz, num_iteracoes = metodo_secante(f, x0, x1, tol)
        print(f"Aproximação da raiz: {raiz}")
        print(f"Número de iterações: {num_iteracoes}")
    except ValueError as e:
        print(e)
