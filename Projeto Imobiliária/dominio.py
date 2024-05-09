import pandas as pd
from datetime import datetime, timedelta

# Função para verificar atrasos no pagamento de aluguel
def verificar_atrasos(dados):
    hoje = datetime.today()
    atrasos = dados[(dados['Data de Vencimento'] < hoje) & (dados['Status'] != 'Pago')]
    if not atrasos.empty:
        print('=' * 100)
        print('')
        print("Alerta: Atrasos no pagamento de aluguel!")
        print('')
        print(atrasos[['Inquilino', 'Data de Vencimento', 'Cobrado', 'Status']])
    print('=' * 100)
    print('')


# Função para verificar vencimento de contrato e reajustes anuais
def verificar_vencimento_contrato(dados):
    hoje = datetime.today()
    proximos_meses = hoje + timedelta(days=30 * 3)  # Próximos 3 meses

    # Converter a coluna 'Fim Contrato' para datetime
    dados['Fim Contrato'] = pd.to_datetime(dados['Fim Contrato'])
    dados['Mês Reajuste'] = pd.to_datetime(dados['Mês Reajuste'], format='%B')

    # Ordenar o DataFrame pela coluna 'Fim Contrato'
    dados = dados.sort_values(by='Fim Contrato')

    # Filtrar os contratos vencendo em breve e com reajuste no mês atual e no próximo mês
    contratos_vencendo = dados[
        (dados['Fim Contrato'] > hoje) & 
        (dados['Fim Contrato'] < proximos_meses) & 
        ((dados['Mês Reajuste'].dt.month == hoje.month) | (dados['Mês Reajuste'].dt.month == (hoje.month % 12) + 1))
    ]

    print('=' * 100)
    print('')

    if not contratos_vencendo.empty:
        print("Alerta: Contratos vencendo em breve com reajuste no mês atual e no próximo mês!")
        print('')
        print(contratos_vencendo[['Inquilino', 'Fim Contrato', 'Mês Reajuste']])
    print('=' * 100)
    print('')

# Função principal
def main():
    # Ler a planilha do Excel
    caminho_do_arquivo = 'C:\\Users\\Renato Moreira\\dominio.xlsx'
    dados = pd.read_excel(caminho_do_arquivo)

    # Verificar atrasos no pagamento de aluguel
    verificar_atrasos(dados)

    # Verificar vencimento de contrato e reajustes anuais
    verificar_vencimento_contrato(dados)


if __name__ == "__main__":
    main()
