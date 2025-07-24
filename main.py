from db import conectar
from aluno import *
from ui import *

def main():
    conn = conectar()
    try:
        while True:
            opcao = menu_principal()

            if opcao == '1':
                limpar_tela()
                try:
                    alunos = listar_alunos(conn)
                    exibir_alunos(alunos)
                except Exception as e:
                    print(f"Ocorreu um erro ao listar os alunos: {e}")
                input("\nPressione Enter para voltar ao menu...")

            elif opcao == '2':
                limpar_tela()
                try:
                    nome = input("Digite o nome do aluno: ")
                    data_nasc = input("Digite a data de nascimento (YYYY-MM-DD): ")
                    inserir_aluno(conn, nome, data_nasc)
                except Exception as e:
                    print(f"Ocorreu um erro ao inserir o aluno: {e}")
                input("\nPressione Enter para voltar ao menu...")
                
            elif opcao == '3':
                limpar_tela()
                try:
                    id_aluno = input("Digite o ID do aluno: ")
                    aluno = buscar_aluno_por_id(conn, id_aluno)
                    if aluno:
                        print(f"ID: {aluno[0]} | Nome: {aluno[1]} | Nascimento: {aluno[2]}")
                    else:
                        print("Aluno não encontrado.")
                except Exception as e:
                    print(f"Ocorreu um erro ao buscar o aluno: {e}")
                input("\nPressione Enter para voltar ao menu...")

            elif opcao == '4':
                limpar_tela()
                id_aluno = input("Digite o ID do aluno a ser atualizado: ")
                try:
                    aluno = buscar_aluno_por_id(conn, id_aluno)
                    if aluno:
                        print(f"Aluno atual: {aluno[1]}, Nascimento: {aluno[2]}")
                        novo_nome = input("Novo nome: ")
                        nova_data = input("Nova data de nascimento (YYYY-MM-DD): ")
                        atualizar_aluno(conn, id_aluno, novo_nome, nova_data)
                    else:
                        print("Aluno não encontrado.")
                except Exception as e:
                    print(f"Ocorreu um erro ao atualizar o aluno: {e}")
                input("\nPressione Enter para voltar ao menu...")

            elif opcao == '5':
                limpar_tela()
                id_aluno = input("Digite o ID do aluno a ser deletado: ")
                try:
                    aluno = buscar_aluno_por_id(conn, id_aluno)
                    if aluno:
                        confirm = input(f"Tem certeza que deseja deletar o aluno {aluno[1]}? (s/n): ").lower()
                        if confirm == 's':
                            deletar_alunoID(conn, id_aluno)

                        else:
                            print("Operação cancelada.")
                    else:
                        print("Aluno não encontrado.")
                except Exception as e:
                    print(f"Ocorreu um erro ao deletar o aluno: {e}")
                input("\nPressione Enter para voltar ao menu...")


            elif opcao == '0':
                print("Saindo...")
                break

            else:
                print("Opção inválida, tente novamente.")
                input("\nPressione Enter para continuar...")

    except Exception as e:
        print(f"Ocorreu um erro: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    main()
