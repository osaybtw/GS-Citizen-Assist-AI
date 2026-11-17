"""main.py - Citizen Assist AI: assistente de energia para comércios pequenos.

Execute com:  python main.py
"""

import os

from base_conhecimento import BaseConhecimento
from assistente import Assistente, ler

PASTA = os.path.dirname(os.path.abspath(__file__))
PASTA_DADOS = os.path.join(PASTA, "data")


def menu():
    print("\n=== Citizen Assist AI ===")
    print("Orientações sobre energia elétrica para comércios pequenos")
    print("1. Perguntar (texto livre)")
    print("2. Navegar por categorias")
    print("3. Ver indicadores")
    print("4. Exportar atendimentos para CSV")
    print("0. Sair")


def main():
    base = BaseConhecimento(os.path.join(PASTA_DADOS, "base_conhecimento.json"))
    carregou = base.carregar()          # lê o JSON e cria os objetos Orientacao
    assistente = Assistente("Citizen Assist AI", base, PASTA_DADOS)

    print(f"Olá! Eu sou o {assistente.nome}.")
    print("Não peça nem digite CPF, telefone ou e-mail. Este assistente NÃO é um canal oficial.")
    if not carregou:
        print("Aviso: a base de conhecimento não foi carregada. "
              "Verifique data/base_conhecimento.json.")

    while True:
        menu()
        opcao = ler("Escolha uma opção: ")
        if opcao == "1":
            if carregou:
                assistente.perguntar()
            else:
                print("Base de conhecimento indisponível.")
        elif opcao == "2":
            if carregou:
                assistente.navegar()
            else:
                print("Base de conhecimento indisponível.")
        elif opcao == "3":
            assistente.indicadores()
        elif opcao == "4":
            assistente.exportar_csv()
        elif opcao == "0":
            assistente.pedir_nota()
            print("Até logo!")
            break
        else:
            print("Opção inválida. Digite 1, 2, 3, 4 ou 0.")


if __name__ == "__main__":
    main()
