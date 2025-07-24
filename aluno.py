def listar_alunos(conn):
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT id_aluno, nome, data_nascimento FROM Aluno ORDER BY id_aluno")
            return cursor.fetchall()
    except Exception as e:
        print("Erro ao listar alunos:", e)
        conn.rollback()
        return []

def inserir_aluno(conn, nome, data_nascimento):
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO Aluno (nome, data_nascimento) VALUES (%s, %s)",
                (nome, data_nascimento)
            )
        conn.commit()
        print("Aluno inserido com sucesso.")
    except Exception as e:
        print("Erro ao inserir aluno:", e)
        conn.rollback()

def buscar_aluno_por_id(conn, id_aluno):
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT id_aluno, nome, data_nascimento FROM Aluno WHERE id_aluno = %s", (id_aluno,))
            return cursor.fetchone()
    except Exception as e:
        print("Erro ao buscar aluno:", e)
        conn.rollback()
        return None

def atualizar_aluno(conn, id_aluno, novo_nome, nova_data):
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "UPDATE Aluno SET nome = %s, data_nascimento = %s WHERE id_aluno = %s",
                (novo_nome, nova_data, id_aluno)
            )
        conn.commit()
        print("Aluno atualizado com sucesso.")
    except Exception as e:
        print("Erro ao atualizar aluno:", e)
        conn.rollback()

def deletar_alunoID(conn, id_aluno):
    try:
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM Aluno WHERE id_aluno = %s", (id_aluno,))
        conn.commit()
        print("Aluno deletado com sucesso.")
    except Exception as e:
        print("Erro ao deletar aluno:", e)
        conn.rollback()
