import numpy as np
import sympy as sp
import pandas as pd

# Definição das variáveis simbólicas
theta1, theta2 = sp.symbols('theta1 theta2')

# Definição dos parâmetros constantes
P = 100  # N (peso)
L = 1    # m (comprimento)
k = 1000  # Nm/rad (constante de proporcionalidade, pode ser ajustada)

# Definição do sistema de equações não lineares
f1 = k*theta1 - (3*P*L/2) * sp.cos(theta1) - k * (theta2 - theta1)
f2 = k*(theta2 - theta1) - (P*L/2) * sp.cos(theta2)

# Criando a matriz de funções e calculando a Jacobiana simbolicamente
F = sp.Matrix([f1, f2])
J = F.jacobian([theta1, theta2])

# Convertendo para funções numéricas
F_lambdified = sp.lambdify((theta1, theta2), F, 'numpy')
J_lambdified = sp.lambdify((theta1, theta2), J, 'numpy')

# Chute inicial
X_k = np.array([0.5, 0.5], dtype=float)

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
colunas = ["Iteração", "theta1", "theta2", "Erro_theta1", "Erro_theta2", "Maior Erro"]
df_resultados = pd.DataFrame(resultados, columns=colunas)

# Exportando para Excel
df_resultados.to_excel("resultados_newton.xlsx", index=False)

print("Arquivo 'resultados_newton.xlsx' gerado com sucesso!")
