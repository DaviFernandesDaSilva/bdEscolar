def inserir_responsavel(conn, nome, telefone, cpf):
    try:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO responsavel (nome, telefone, cpf)
                VALUES (%s, %s, %s);
            """, (nome, telefone, cpf))
        conn.commit()
        print("Responsável inserido com sucesso.")
    except Exception as e:
        print(f"Erro ao inserir responsável: {e}")
        conn.rollback()
        raise

def listar_responsaveis(conn, coluna="id_responsavel", ordem="ASC"):
    colunas_validas = {
        "id_responsavel": "id_responsavel",
        "Nome": "nome",
    }
    ordem = ordem.upper()
    if coluna not in colunas_validas:
        coluna = "id_responsavel"
    if ordem not in ["ASC", "DESC"]:
        ordem = "ASC"
    
    query = f"""
        SELECT id_responsavel, nome, telefone, cpf
        FROM responsavel
        ORDER BY {colunas_validas[coluna]} {ordem}
    """
    try:
        with conn.cursor() as cur:
            cur.execute(query)
            return cur.fetchall()
    except Exception as e:
        print(f"Erro ao listar responsáveis: {e}")
        conn.rollback()
        return []

def buscar_responsavel_por_id(conn, id_responsavel):
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT id_responsavel, nome, telefone, cpf FROM responsavel WHERE id_responsavel = %s;", (id_responsavel,))
            return cur.fetchone()
    except Exception as e:
        print(f"Erro ao buscar responsável por ID: {e}")
        conn.rollback()
        raise

def buscar_responsavel_por_cpf(conn, cpf):
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT id_responsavel, nome, telefone, cpf FROM responsavel WHERE cpf = %s;", (cpf,))
            return cur.fetchone()
    except Exception as e:
        print(f"Erro ao buscar responsável por CPF: {e}")
        conn.rollback()
        raise

def atualizar_responsavel(conn, id_responsavel, nome, telefone, cpf):
    try:
        with conn.cursor() as cur:
            cur.execute("""
                UPDATE responsavel
                SET nome = %s, telefone = %s, cpf = %s
                WHERE id_responsavel = %s;
            """, (nome, telefone, cpf, id_responsavel))
        conn.commit()
        print("Responsável atualizado com sucesso.")
    except Exception as e:
        print(f"Erro ao atualizar responsável: {e}")
        conn.rollback()
        raise

def deletar_responsavel(conn, id_responsavel):
    try:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM responsavel WHERE id_responsavel = %s;", (id_responsavel,))
        conn.commit()
        print("Responsável deletado com sucesso.")
    except Exception as e:
        print(f"Erro ao deletar responsável: {e}")
        conn.rollback()
        raise

def listar_responsaveis_do_aluno(conn, id_aluno):
    with conn.cursor() as cur:
        cur.execute("""
            SELECT r.id_responsavel, r.nome, r.telefone, r.cpf
            FROM responsavel r
            INNER JOIN Aluno_Responsavel ar ON r.id_responsavel = ar.id_responsavel
            WHERE ar.id_aluno = %s;
        """, (id_aluno,))
        return cur.fetchall()

def desassociar_todos_responsaveis(conn, id_aluno):
    with conn.cursor() as cur:
        cur.execute("DELETE FROM Aluno_Responsavel WHERE id_aluno = %s;", (id_aluno,))
    conn.commit()

def associar_aluno_responsavel(conn, id_aluno, lista_responsaveis):
    try:
        with conn.cursor() as cur:
            # Primeiro, apaga todas associações antigas do aluno para não duplicar
            cur.execute("DELETE FROM aluno_responsavel WHERE id_aluno = %s;", (id_aluno,))
            
            # Agora, insere as associações selecionadas
            for id_resp in lista_responsaveis:
                cur.execute(
                    "INSERT INTO aluno_responsavel (id_aluno, id_responsavel) VALUES (%s, %s);",
                    (id_aluno, id_resp)
                )
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
