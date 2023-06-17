import pandas
import pandas as pd
import openpyxl

def encontra_nome(email, planilha):
    tabela = pd.read_excel(planilha)

    # Colunas de Interesse
    c1 = ''
    if planilha == 'alunos.xlsx':
        c1 = 'E-mail academico'
    elif planilha == 'professores.xlsx':
        c1 = 'E-mail'
    c2 = 'Nome'

    email_conhecido = email

    nomes_coluna2 = tabela.loc[tabela[c1] == email_conhecido, c2].tolist()

    return nomes_coluna2[0]


