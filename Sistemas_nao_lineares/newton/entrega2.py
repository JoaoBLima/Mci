import numpy as np
import sympy as sp
import pandas as pd

# Definição das variáveis
theta1, theta2 = sp.symbols('theta1 theta2')

# Parâmetros fornecidos no problema
P = 100  # N
L = 1    # m

# Lista dos valores de k a serem testados
valores_k = [1000, 500, 100, 10]

# Lista para armazenar resultados
resultados = []

# Iteração para cada valor de k
for k in valores_k:
    # Definição do sistema de equações
    f1 = k * theta1 - (3 * P * L / 2) * sp.cos(theta1) - k * (theta2 - theta1)
    f2 = k * (theta2 - theta1) - (P * L / 2) * sp.cos(theta2)

    # Criando a matriz de funções e a Jacobiana simbolicamente
    F = sp.Matrix([f1, f2])
    J = F.jacobian([theta1, theta2])

    # Convertendo para funções numéricas
    F_lambdified = sp.lambdify((theta1, theta2), F, 'numpy')
    J_lambdified = sp.lambdify((theta1, theta2), J, 'numpy')

    # Chute inicial
    X_k = np.array([0.1, 0.1], dtype=float)

    # Critério de parada
    tol = 1e-4
    max_iter = 20

    # Método de Newton
    for _ in range(max_iter):
        # Calcula F(X_k) e J(X_k)
        F_val = np.array(F_lambdified(*X_k), dtype=float).flatten()
        J_val = np.array(J_lambdified(*X_k), dtype=float)

        # Resolve o sistema linear J(X_k) * ΔX = -F(X_k)
        delta_X = np.linalg.solve(J_val, -F_val)

        # Atualiza a solução
        X_k1 = X_k + delta_X

        # Verifica a convergência
        if np.max(np.abs(X_k1 - X_k)) < tol:
            break

        # Atualiza X_k para a próxima iteração
        X_k = X_k1

    # Salva os resultados
    resultados.append([k, round(X_k[0], 4), round(X_k[1], 4)])

# Criando DataFrame para exibição
df_resultados = pd.DataFrame(resultados, columns=["k (Nm/rad)", "θ1 (rad)", "θ2 (rad)"])
print(df_resultados)
