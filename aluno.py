def listar_alunos(conn, coluna="id_aluno", ordem="ASC"):
    colunas_validas = {
        "id_aluno": "id_aluno",
        "nome": "nome",
        "data_nascimento": "data_nascimento"
    }
    ordem = ordem.upper()
    if coluna not in colunas_validas:
        coluna = "id_aluno"
    if ordem not in ["ASC", "DESC"]:
        ordem = "ASC"
    
    query = f"""
        SELECT id_aluno, nome, data_nascimento
        FROM Aluno
        ORDER BY {colunas_validas[coluna]} {ordem}
    """
    try:
        with conn.cursor() as cur:
            cur.execute(query)
            return cur.fetchall()
    except Exception as e:
        print(f"Erro ao listar alunos: {e}")
        return []

    
def listar_alunos_sem_matricula(conn):
    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT id_aluno, nome 
                FROM Aluno 
                WHERE id_aluno NOT IN (SELECT id_aluno FROM Matricula);
            """)
            return cur.fetchall()
    except Exception as e:
        raise e

def inserir_aluno(conn, nome, data_nascimento):
    try:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO aluno (nome, data_nascimento)
                VALUES (%s, %s)
                RETURNING id_aluno;
            """, (nome, data_nascimento))
            id_aluno = cur.fetchone()[0]
        conn.commit()
        print("Aluno inserido com sucesso.")
        return id_aluno
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
        raise

def listar_responsaveis_do_aluno(conn, id_aluno):
    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT r.id_responsavel, r.nome, r.telefone, r.cpf
                FROM responsavel r
                JOIN aluno_responsavel ar ON r.id_responsavel = ar.id_responsavel
                WHERE ar.id_aluno = %s
                ORDER BY r.nome;
            """, (id_aluno,))
            return cur.fetchall()
    except Exception as e:
        print(f"Erro ao listar responsáveis do aluno: {e}")
        return []