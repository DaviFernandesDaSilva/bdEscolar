import psycopg2

def conectar():
    return psycopg2.connect(
        dbname="Studee",
        user="postgres",
        password="davi123",
        host="localhost",
        port="5432"
    )
