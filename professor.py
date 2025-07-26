def listar_professor(conn, coluna="id_professor", ordem="ASC"):
    try:
        with conn.cursor() as cur:
            query = f"""
                SELECT 
                    p.id_professor, 
                    p.nome,
                    STRING_AGG(d.nome || ' (' || t.nome || ' - ' || t.ano::text || ')', ', ') AS disciplinas_turmas
                FROM Professor p
                LEFT JOIN Turma_Disciplina td ON td.id_professor = p.id_professor
                LEFT JOIN Disciplina d ON d.id_disciplina = td.id_disciplina
                LEFT JOIN Turma t ON t.id_turma = td.id_turma
                GROUP BY p.id_professor, p.nome
                ORDER BY {coluna} {ordem}
            """
            cur.execute(query)
            return cur.fetchall()
    except Exception as e:
        print(f"Erro ao listar professores: {e}")
        conn.rollback()
        return []

def inserir_professor(conn, nome):
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO Professor (nome) VALUES (%s)",
                (nome,)
            )
        conn.commit()
        print("Professor inserido com sucesso.")
    except Exception as e:
        print("Erro ao inserir professor:", e)
        conn.rollback()

def buscar_professor_por_id(conn, id_professor):
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT id_professor, nome FROM Professor WHERE id_professor = %s", (id_professor,))
            return cursor.fetchone()
    except Exception as e:
        print("Erro ao buscar professor:", e)
        conn.rollback()
        return None

def atualizar_professor(conn, id_professor, novo_nome):
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "UPDATE Professor SET nome = %s WHERE id_professor = %s",
                (novo_nome, id_professor)
            )
        conn.commit()
        print("Professor atualizado com sucesso.")
    except Exception as e:
        print("Erro ao atualizar professor:", e)
        conn.rollback()

def deletar_professorID(conn, id_professor):
    try:
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM Professor WHERE id_professor = %s", (id_professor,))
        conn.commit()
        print("Professor deletado com sucesso.")
    except Exception as e:
        print("Erro ao deletar professor:", e)
        conn.rollback()
