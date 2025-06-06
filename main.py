# Criando um programa que ajuda os motoqueiros a monitorar os gastos de gasolina/km
# main.py o arquivo principal que roda o programa
# Esse é o programa que o usuário vai interagir no terminal. É como o menu

from models import Moto

def menu():
    print("\n=== MONITOR DE GASTOS DA MOTO ===")
    print("1 - Adicionar abastecimento")
    print("2 - Registrar troca de óleo")
    print("3 - Ver relatório de consumo")
    print("0 - Sair")

def main():
    moto = Moto()

    while True:
        menu()
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            try:
                data = input("Data do abastecimento (dd/mm/aaaa): ")
                litros = float(input("Quantidade de litros abastecidos: "))
                valor = float(input("Valor total pago: R$ "))
                km_atual = int(input("KM atual: "))
                moto.adicionar_abastecimento(data, litros, valor, km_atual)
            except ValueError:
                print("Erro nos dados inseridos. Tente novamente.")
        
        elif opcao == "2":
            moto.troca_oleo()

        elif opcao == "3":
            moto.relatorio()

        elif opcao == "0":
            print("Saindo... Até mais!")
            break
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    main()
