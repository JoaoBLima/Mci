#entrega 1- chutes:1,1,1

import numpy as np
import sympy as sp
import pandas as pd

# Definição das variáveis simbólicas
x, y, z = sp.symbols('x y z')

# Definição do sistema de equações não lineares
f1 = 2*x - sp.cos(x) - y
f2 = -x + 2*y - sp.cos(y) - z
f3 = -y + z - sp.cos(z)

# Criando a matriz de funções e calculando a Jacobiana simbolicamente
F = sp.Matrix([f1, f2, f3])
J = F.jacobian([x, y, z])

# Convertendo para funções numéricas
F_lambdified = sp.lambdify((x, y, z), F, 'numpy')
J_lambdified = sp.lambdify((x, y, z), J, 'numpy')

# Chute inicial
X_k = np.array([-2.0, -3.0, -4.0], dtype=float)

# Critério de parada
tol = 1e-4  # Precisão desejada
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
    resultados.append([i, *X_k.round(4), *erro.round(4), round(np.max(erro), 4)])
    
    # Verifica convergência
    if np.max(erro) < tol:
        break
    
    # Atualiza X_k para a próxima iteração
    X_k = X_k1

# Criando DataFrame para exibição
colunas = ["Iteração", "x", "y", "z", "Erro_x", "Erro_y", "Erro_z", "Maior Erro"]
df_resultados = pd.DataFrame(resultados, columns=colunas)

# Exibindo a tabela final
print(df_resultados)
