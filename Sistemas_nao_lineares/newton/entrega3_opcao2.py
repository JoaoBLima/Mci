import numpy as np
import sympy as sp
import pandas as pd

# Definição das variáveis
theta1, theta2, theta3 = sp.symbols('theta1 theta2 theta3')

# Parâmetros fornecidos no problema
P = 10  # N
L = 1    # m

# Lista dos valores de k a serem testados
valores_k = [1000, 100, 10]

# Lista para armazenar resultados
resultados = []

# Iteração para cada valor de k
for k in valores_k:
    # Definição do sistema de equações
    f1 = k * theta1 - (5 * P * L / 2) * sp.cos(theta1) - k * (theta2 - theta1)
    f2 = k * (theta2 - theta1) - (3 * P * L / 2) * sp.cos(theta2) - k * (theta3 - theta2)
    f3 = k * (theta3 - theta2) - (P * L / 2) * sp.cos(theta3)

    # Criando a matriz de funções e a Jacobiana simbolicamente
    F = sp.Matrix([f1, f2, f3])
    J = F.jacobian([theta1, theta2, theta3])

    # Convertendo para funções numéricas
    F_lambdified = sp.lambdify((theta1, theta2, theta3), F, 'numpy')
    J_lambdified = sp.lambdify((theta1, theta2, theta3), J, 'numpy')

    # Chute inicial
    X_k = np.array([0.1, 0.1, 0.1], dtype=float)

    # Critério de parada
    tol = 1e-4
    max_iter = 20

    print(f"\nResolvendo para k = {k}")
    
    # Método de Newton
    for i in range(max_iter):
        # Calcula F(X_k) e J(X_k)
        F_val = np.array(F_lambdified(*X_k), dtype=float).flatten()
        J_val = np.array(J_lambdified(*X_k), dtype=float)

        # Resolve o sistema linear J(X_k) * ΔX = -F(X_k)
        delta_X = np.linalg.solve(J_val, -F_val)

        # Atualiza a solução
        X_k1 = X_k + delta_X

        # Calcula o erro
        erro = np.max(np.abs(delta_X))
        print(f"Iteração {i+1}: Erro = {erro:.6f}")

        # Verifica a convergência
        if erro < tol:
            break

        # Atualiza X_k para a próxima iteração
        X_k = X_k1

    # Salva os resultados
    resultados.append([k, round(X_k[0], 4), round(X_k[1], 4), round(X_k[2], 4)])

# Criando DataFrame para exibição
df_resultados = pd.DataFrame(resultados, columns=["k (Nm/rad)", "θ1 (rad)", "θ2 (rad)", "θ3 (rad)"])
print("\nResultados finais:")
print(df_resultados)
