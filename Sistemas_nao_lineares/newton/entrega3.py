import numpy as np
import sympy as sp
import pandas as pd

# Definição das variáveis simbólicas
theta1, theta2, theta3, k = sp.symbols('theta1 theta2 theta3 k')

# Definição dos parâmetros constantes
P = 10   # N (peso)
L = 1    # m (comprimento)

# Definição do sistema de equações não lineares com base nas condições de equilíbrio
f1 = k * theta1 - (5 * P * L / 2) * sp.cos(theta1) - k * (theta2 - theta1)
f2 = k * (theta2 - theta1) - (3 * P * L / 2) * sp.cos(theta2) - k * (theta3 - theta2)
f3 = k * (theta3 - theta2) - (P * L / 2) * sp.cos(theta3)

# Criando a matriz de funções e calculando a Jacobiana simbolicamente
F = sp.Matrix([f1, f2, f3])
J = F.jacobian([theta1, theta2, theta3])

# Lista de valores de k a serem testados
valores_k = [1000, 100, 10]

for k_val in valores_k:
    print(f"\nResolvendo para k = {k_val} Nm/rad")
    
    # Converter as funções para uso numérico
    F_lambdified = sp.lambdify((theta1, theta2, theta3), F.subs(k, k_val), 'numpy')
    J_lambdified = sp.lambdify((theta1, theta2, theta3), J.subs(k, k_val), 'numpy')
    
    # Chute inicial
    X_k = np.array([0.5, 0.5, 0.5], dtype=float)  # Chute inicial para theta1, theta2 e theta3
    
    # Critério de parada
    tol = 1e-10  # Precisão desejada
    max_iter = 20  # Número máximo de iterações
    
    # Lista para armazenar resultados
    resultados = []
    
    for i in range(max_iter):
        # Calcula F(X_k) e J(X_k)
        F_val = np.array(F_lambdified(*X_k), dtype=float).flatten()
        J_val = np.array(J_lambdified(*X_k), dtype=float)
        
        # Resolve o sistema linear J(X_k) * ΔX = -F(X_k) para ΔX
        delta_X = np.linalg.solve(J_val, -F_val)
        
        # Atualiza a solução
        X_k1 = X_k + delta_X
        
        # Calcula erro absoluto |X_k1 - X_k|
        erro = np.abs(X_k1 - X_k)
        
        # Registra os resultados com 4 casas decimais
        resultados.append([i, *X_k.round(10), *erro.round(10), round(np.max(erro), 10)])
        
        # Verifica convergência
        if np.max(erro) < tol:
            break
        
        # Atualiza X_k para a próxima iteração
        X_k = X_k1
    
    # Criando DataFrame para exibição
    colunas = ["Iteração", "theta1", "theta2", "theta3", "Erro_theta1", "Erro_theta2", "Erro_theta3", "Maior Erro"]
    df_resultados = pd.DataFrame(resultados, columns=colunas)
    
    # Exibindo a tabela final
    print(df_resultados)
