def listar_turmas_com_disciplinas(conn, coluna="id_turma", ordem="ASC"):
    try:
        colunas_validas = {
            "ID": "t.id_turma",
            "Nome": "t.nome",
            "Ano": "t.ano",
        }

        coluna_sql = colunas_validas.get(coluna, "t.id_turma")
        ordem_sql = "ASC" if ordem.upper() == "ASC" else "DESC"

        with conn.cursor() as cursor:
            cursor.execute(f"""
                SELECT 
                    t.id_turma, t.nome, t.ano,
                    STRING_AGG(d.nome || ' (Prof. ' || p.nome || ')', ', ') AS disciplinas
                FROM Turma t
                LEFT JOIN Turma_Disciplina td ON td.id_turma = t.id_turma
                LEFT JOIN Disciplina d ON d.id_disciplina = td.id_disciplina
                LEFT JOIN Professor p ON p.id_professor = td.id_professor
                GROUP BY t.id_turma, t.nome, t.ano
                ORDER BY {coluna_sql} {ordem_sql}
            """)
            return cursor.fetchall()

    except Exception as e:
        print("Erro ao listar turmas:", e)
        conn.rollback()
        return []

def listar_turmas(conn):
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT id_turma, nome, ano FROM Turma ORDER BY id_turma")
            return cursor.fetchall()
    except Exception as e:
        print("Erro ao listar turmas:", e)
        conn.rollback()
        return []

def inserir_turma(conn, nome, ano):
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO Turma (nome, ano) VALUES (%s, %s)",
                (nome, ano)
            )
        conn.commit()
        print("Turma inserida com sucesso.")
    except Exception as e:
        print("Erro ao inserir turma:", e)
        conn.rollback()

def buscar_turma_por_id(conn, id_turma):
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT id_turma, nome, ano FROM Turma WHERE id_turma = %s", (id_turma,))
            return cursor.fetchone()
    except Exception as e:
        print("Erro ao buscar turma:", e)
        conn.rollback()
        return None

def atualizar_turma(conn, id_turma, novo_nome, novo_ano):
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "UPDATE Turma SET nome = %s, ano = %s WHERE id_turma = %s",
                (novo_nome, novo_ano, id_turma)
            )
        conn.commit()
        print("Turma atualizada com sucesso.")
    except Exception as e:
        print("Erro ao atualizar turma:", e)
        conn.rollback()

def deletar_turma(conn, id_turma):
    try:
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM Turma WHERE id_turma = %s", (id_turma,))
        conn.commit()
        print("Turma deletada com sucesso.")
    except Exception as e:
        print("Erro ao deletar turma:", e)
        conn.rollback()
        raise e 
