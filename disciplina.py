def listar_disciplina(conn):
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT id_disciplina, nome FROM Disciplina ORDER BY id_disciplina")
            return cursor.fetchall()
    except Exception as e:
        print("Erro ao listar disciplinas:", e)
        conn.rollback()
        return []
    
def listar_turma_disciplina(conn):
    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT td.id_turma, t.nome_turma,
                    td.id_disciplina, d.nome,
                    td.id_professor, p.nome_professor
                FROM Turma_Disciplina td
                JOIN Turma t ON td.id_turma = t.id_turma
                JOIN Disciplina d ON td.id_disciplina = d.id_disciplina
                JOIN Professor p ON td.id_professor = p.id_professor
                ORDER BY t.nome_turma, d.nome;
            """)
            return cur.fetchall()
    except Exception as e:
        print("Erro ao listar disciplinas por turma:", e)
        conn.rollback()
        raise
    
def listar_disciplinas_com_associacoes(conn):
    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT 
                    d.id_disciplina,
                    d.nome,
                    CONCAT(t.ano, ' Ano ', t.nome) AS turma_ano,
                    p.nome
                FROM Disciplina d
                JOIN Turma_Disciplina td ON d.id_disciplina = td.id_disciplina
                JOIN Turma t ON td.id_turma = t.id_turma
                JOIN Professor p ON td.id_professor = p.id_professor
                ORDER BY d.id_disciplina;
            """)
            return cur.fetchall()
    except Exception as e:
        print("Erro ao listar disciplinas com associações:", e)
        conn.rollback()
        raise
    
def associar_turma_disciplina_professor(conn, id_turma, id_disciplina, id_professor):
    try:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO Turma_Disciplina (id_turma, id_disciplina, id_professor)
                VALUES (%s, %s, %s)
                ON CONFLICT (id_turma, id_disciplina) DO UPDATE SET id_professor = EXCLUDED.id_professor;
            """, (id_turma, id_disciplina, id_professor))
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e

def inserir_disciplina(conn, nome):
    try:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO Disciplina (nome) VALUES (%s) RETURNING id_disciplina;",
                (nome,)
            )
            id_disciplina = cur.fetchone()[0]  # Pega o ID retornado
        conn.commit()
        return id_disciplina
    except Exception as e:
        conn.rollback()
        raise e

def buscar_disciplina_por_id(conn, id_disciplina):
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT 
                    d.id_disciplina,
                    d.nome,
                    CONCAT(t.ano, ' Ano ', t.nome) AS turma_ano,
                    p.nome
                FROM Disciplina d
                JOIN Turma_Disciplina td ON d.id_disciplina = td.id_disciplina
                JOIN Turma t ON td.id_turma = t.id_turma
                JOIN Professor p ON td.id_professor = p.id_professor
                WHERE d.id_disciplina = %s
                LIMIT 1;
            """, (id_disciplina,))
            return cursor.fetchone()
    except Exception as e:
        print("Erro ao buscar disciplina:", e)
        conn.rollback()
        return None

def atualizar_disciplina(conn, id_disciplina, novo_nome):
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "UPDATE Disciplina SET nome = %s WHERE id_disciplina = %s",
                (novo_nome, id_disciplina)
            )
        conn.commit()
        print("Disciplina atualizada com sucesso.")
    except Exception as e:
        print("Erro ao atualizar disciplina:", e)
        conn.rollback()

def deletar_disciplina(conn, id_disciplina):
    try:
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM Disciplina WHERE id_disciplina = %s", (id_disciplina,))
        conn.commit()
        print("Disciplina deletada com sucesso.")
    except Exception as e:
        print("Erro ao deletar disciplina:", e)
        conn.rollback()
        raise e

def deletar_turma_disciplina(conn, id_turma, id_disciplina):
    try:
        with conn.cursor() as cur:
            cur.execute("""
                DELETE FROM Turma_Disciplina
                WHERE id_turma = %s AND id_disciplina = %s;
            """, (id_turma, id_disciplina))
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e