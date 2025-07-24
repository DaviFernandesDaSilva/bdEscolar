import os

def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')

def menu_principal():
    limpar_tela()
    print("=== Sistema de Gestão Escolar ===")
    print("1. Listar Alunos")
    print("2. Inserir Aluno")
    print("3. Buscar Aluno por ID")
    print("4. Atualizar Aluno")
    print("5. Deletar Aluno por ID")
    print("0. Sair")
    return input("Escolha uma opção: ")

def exibir_alunos(alunos):
    if not alunos:
        print("Nenhum aluno encontrado.")
    else:
        for a in alunos:
            print(f"ID: {a[0]} | Nome: {a[1]} | Nascimento: {a[2]}")
