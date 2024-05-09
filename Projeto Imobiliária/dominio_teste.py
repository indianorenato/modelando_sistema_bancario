import pandas as pd
import mysql.connector

# Ler a planilha do Excel
caminho_do_arquivo = 'C:\\Users\\Renato Moreira\\dominio.xlsx'
dados = pd.read_excel(caminho_do_arquivo)

# Conectar-se ao banco de dados MySQL
conexao = mysql.connector.connect(
    host='DESKTOP-O2UL14C',
    user='root',
    password='Rekymite1.',
    database='analisededados'
)
cursor = conexao.cursor()

# Inserir os dados na tabela correspondente
for indice, linha in dados.iterrows():
    # Supondo que você tenha uma tabela chamada "sua_tabela" e que as colunas correspondam
    # às colunas na sua planilha do Excel
    cursor.execute("INSERT INTO sua_tabela (coluna1, coluna2, ...) VALUES (%s, %s, ...)", tuple(linha))

# Confirmar as alterações
conexao.commit()

# Fechar a conexão
cursor.close()
conexao.close()

