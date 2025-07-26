# matricula.py
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
    
def listar_matriculas_ordenadas(conn, coluna='ID', ordem='ASC'):
    # Dicionário para mapear os nomes amigáveis para as colunas reais
    colunas_validas = {
        'ID': 'm.id_matricula',
        'Aluno': 'a.nome',
        'Turma': 't.nome',
        'Ano': 't.ano',
        'Data': 'm.data_matricula'
    }

    coluna_sql = colunas_validas.get(coluna, 'm.id_matricula')
    ordem = ordem.upper()
    if ordem not in ['ASC', 'DESC']:
        ordem = 'ASC'

    query = f"""
        SELECT m.id_matricula, a.id_aluno, a.nome, t.id_turma, t.nome, m.data_matricula, t.ano
        FROM Matricula m
        JOIN Aluno a ON m.id_aluno = a.id_aluno
        JOIN Turma t ON m.id_turma = t.id_turma
        ORDER BY {coluna_sql} {ordem};
    """

    with conn.cursor() as cur:
        cur.execute(query)
        return cur.fetchall()

def listar_matriculas(conn):
    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT 
                    m.id_matricula, 
                    a.id_aluno, 
                    a.nome, 
                    t.id_turma, 
                    t.nome, 
                    m.data_matricula,
                    t.ano
                FROM Matricula m
                JOIN Aluno a ON m.id_aluno = a.id_aluno
                JOIN Turma t ON m.id_turma = t.id_turma
                ORDER BY m.id_matricula;
            """)
            return cur.fetchall()
    except Exception as e:
        raise e

def inserir_matricula(conn, id_aluno, id_turma, data_matricula):
    try:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO Matricula (id_aluno, id_turma, data_matricula)
                VALUES (%s, %s, %s);
            """, (id_aluno, id_turma, data_matricula))
        conn.commit()
    except Exception as e:
        conn.rollback()
        print("Erro ao inserir matrícula:", e)
        raise e

def listar_matriculas_por_aluno(conn, id_aluno):
    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT t.id_turma, t.nome, m.data_matricula
                FROM Matricula m
                JOIN Turma t ON m.id_turma = t.id_turma
                WHERE m.id_aluno = %s;
            """, (id_aluno,))
            return cur.fetchall()
    except Exception as e:
        print("Erro ao listar matrículas por aluno:", e)
        raise e

def deletar_matricula(conn, id_matricula):
    try:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM Matricula WHERE id_matricula = %s;", (id_matricula,))
        conn.commit()
    except Exception as e:
        conn.rollback()
        print("Erro ao deletar matrícula:", e)
        raise e

def inserir_matricula_em_lote(conn, lista_id_aluno, id_turma, data_matricula):
    try:
        with conn.cursor() as cur:
            for id_aluno in lista_id_aluno:
                cur.execute("""
                    INSERT INTO Matricula (id_aluno, id_turma, data_matricula)
                    VALUES (%s, %s, %s);
                """, (id_aluno, id_turma, data_matricula))
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e