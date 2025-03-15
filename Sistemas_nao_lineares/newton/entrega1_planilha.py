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

# Definição dos quatro chutes iniciais
chutes_iniciais = [
    np.array([1.0, 1.0, 1.0], dtype=float),  # Caso a
    np.array([-0.5, -2.0, -3.0], dtype=float),  # Caso b
    np.array([-2.0, -3.0, -4.0], dtype=float),  # Caso c
    np.array([0.0, 0.0, 0.0], dtype=float)   # Caso d
]

# Critério de parada
tol = 1e-5  # Precisão desejada
max_iter = 30  # Número máximo de iterações

# Lista para armazenar os resultados gerais
todos_resultados = []

# Itera sobre cada chute inicial
for idx, X_k in enumerate(chutes_iniciais):
    resultados = []  # Lista para armazenar os resultados desse caso

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
        resultados.append([chr(97 + idx), i, *X_k.round(5), *erro.round(5), round(np.max(erro), 5)])
        
        # Verifica convergência
        if np.max(erro) < tol:
            break
        
        # Atualiza X_k para a próxima iteração
        X_k = X_k1

    # Adiciona uma separação entre os casos na tabela
    if todos_resultados:
        todos_resultados.append(["-", "-", "-", "-", "-", "-", "-", "-", "-"])
    
    # Adiciona os resultados do caso à lista geral
    todos_resultados.extend(resultados)

# Criando DataFrame para exibição e salvamento
colunas = ["Caso", "Iteração", "x", "y", "z", "Erro_x", "Erro_y", "Erro_z", "Maior Erro"]
df_resultados = pd.DataFrame(todos_resultados, columns=colunas)

# Salvando os resultados em uma planilha Excel
df_resultados.to_excel("resultados_sistema_nao_linear.xlsx", index=False)

# Exibindo mensagem de conclusão
print("Planilha 'resultados_sistema_nao_linear.xlsx' gerada com sucesso!")
