from datetime import datetime

class Transacao:
    def __init__(self, valor, tipo):
        self.valor = valor
        self.tipo = tipo
        self.data_hora = datetime.now()

class Extrato:
    def __init__(self):
        self.transacoes = []

    def adicionar_transacao(self, transacao):
        self.transacoes.append(transacao)

class ContaBancaria:
    def __init__(self, agencia, numero_conta, saldo=3500):
        self.agencia = agencia
        self.numero_conta = numero_conta
        self.saldo = saldo
        self.saques_realizados = Extrato()
        self.depositos_realizados = Extrato()

    def depositar(self, valor):
        self.saldo += valor
        transacao = Transacao(valor, "Depósito")
        self.depositos_realizados.adicionar_transacao(transacao)

    def sacar(self, valor):
        if self.saldo >= valor:
            self.saldo -= valor
            transacao = Transacao(valor, "Saque")
            self.saques_realizados.adicionar_transacao(transacao)

    def extrato(self):
        return {
            'saldo': self.saldo,
            'saques_realizados': self.saques_realizados.transacoes,
            'depositos_realizados': self.depositos_realizados.transacoes
        }


class Usuario:
    def __init__(self, nome, data_nascimento, cpf, endereco):
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf
        self.endereco = endereco
        self.contas = []

    def cadastrar_conta(self, conta):
        self.contas.append(conta)


usuarios = []
contas = []
prox_numero_conta = 1


def cadastrar_usuario(nome, data_nascimento, cpf, endereco):
    for usuario in usuarios:
        if usuario.cpf == cpf:
            print("CPF já cadastrado.")
            return
    usuarios.append(Usuario(nome, data_nascimento, cpf, endereco))
    print("Usuário cadastrado com sucesso.")


def cadastrar_conta(usuario):
    global prox_numero_conta
    conta = ContaBancaria(agencia="0001", numero_conta=f"{prox_numero_conta:04}")
    prox_numero_conta += 1
    usuario.cadastrar_conta(conta)
    contas.append({'usuario': usuario, 'conta': conta})
    print("Conta cadastrada com sucesso.")


def saque(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
    if len(extrato['saques_realizados']) >= limite_saques:
        print('Você já atingiu o limite diário de saques.')
        return saldo, extrato
    if valor > limite:
        print('O valor máximo por saque é excedido.')
        return saldo, extrato
    if saldo < valor:
        print('Saldo insuficiente para realizar o saque.')
        return saldo, extrato

    saldo -= valor
    transacao = Transacao(valor, "Saque")
    extrato['saques_realizados'].append(transacao)
    print(f'Saque de R${valor:.2f} realizado com sucesso.')
    return saldo, extrato


def deposito(saldo, valor, extrato):
    saldo += valor
    transacao = Transacao(valor, "Depósito")
    extrato['depositos_realizados'].append(transacao)
    print(f'Depósito de R${valor:.2f} realizado com sucesso.')
    return saldo, extrato


def extrato(saldo, *, extrato):
    print('\n=== Extrato ===')
    print(f'Saldo atual: R${saldo:.2f}\n')
    print('Saques realizados:')
    for transacao in extrato['saques_realizados']:
        print(f'- {transacao.tipo} de R${transacao.valor:.2f} em {transacao.data_hora}')
    print('\nDepósitos realizados:')
    for transacao in extrato['depositos_realizados']:
        print(f'- {transacao.tipo} de R${transacao.valor:.2f} em {transacao.data_hora}')
    print('\n===============')


def listar_contas(usuario):
    print('\n--- Contas do Usuário ---')
    for item in contas:
        if item['usuario'] == usuario:
            print(f"Agência: {item['conta'].agencia} - Número da Conta: {item['conta'].numero_conta}")


def main():
    print("SEJA BEM-VINDO!")
    print('========================= MENU =========================')
    while True:
        print("\nEscolha uma operação:")
        print("1 - Cadastrar Usuário")
        print("2 - Cadastrar Conta Bancária")
        print("3 - Depositar")
        print("4 - Sacar")
        print("5 - Visualizar Extrato")
        print("6 - Listar Contas de um Usuário")
        print("7 - Sair")

        opcao = input("Digite o número da operação desejada: ")

        if opcao == "1":
            nome = input("Digite seu nome completo: ")
            data_nascimento = input("Digite sua data de nascimento (DD/MM/AAAA): ")
            cpf = input("Digite seu CPF: ")
            endereco = input("Digite seu endereço: ")
            cadastrar_usuario(nome, data_nascimento, cpf, endereco)
        elif opcao == "2":
            cpf = input("Digite o CPF do usuário: ")
            usuario = next((u for u in usuarios if u.cpf == cpf), None)
            if usuario:
                cadastrar_conta(usuario)
            else:
                print("Usuário não encontrado.")
        elif opcao == "3":
            cpf = input("Digite o CPF do usuário: ")
            usuario = next((u for u in usuarios if u.cpf == cpf), None)
            if usuario:
                valor = float(input("Digite o valor a ser depositado: "))
                conta = next((c['conta'] for c in contas if c['usuario'] == usuario), None)
                if conta:
                    conta['conta'].saldo, _ = deposito(conta['conta'].saldo, valor, conta['conta'].extrato())
                else:
                    print("Conta não encontrada.")
            else:
                print("Usuário não encontrado.")
        elif opcao == "4":
            cpf = input("Digite o CPF do usuário: ")
            usuario = next((u for u in usuarios if u.cpf == cpf), None)
            if usuario:
                valor = float(input("Digite o valor a ser sacado: "))
                conta = next((c['conta'] for c in contas if c['usuario'] == usuario), None)
                if conta:
                    conta['conta'].saldo, _ = saque(saldo=conta['conta'].saldo, valor=valor,
                                                     extrato=conta['conta'].extrato(), limite=500, numero_saques=3,
                                                     limite_saques=3)
                else:
                    print("Conta não encontrada.")
            else:
                print("Usuário não encontrado.")
        elif opcao == "5":
            cpf = input("Digite o CPF do usuário: ")
            usuario = next((u for u in usuarios if u.cpf == cpf), None)
            if usuario:
                conta = next((c['conta'] for c in contas if c['usuario'] == usuario), None)
                if conta:
                    extrato(conta['conta'].saldo, extrato=conta['conta'].extrato())
                else:
                    print("Conta não encontrada.")
            else:
                print("Usuário não encontrado.")
        elif opcao == "6":
            cpf = input("Digite o CPF do usuário: ")
            usuario = next((u for u in usuarios if u.cpf == cpf), None)
            if usuario:
                listar_contas(usuario)
            else:
                print("Usuário não encontrado.")
        elif opcao == "7":
            print("Saindo...")
            break
        else:
            print("Opção inválida. Por favor, escolha uma opção válida.")


if __name__ == "__main__":
    main()

