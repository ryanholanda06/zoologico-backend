import psycopg2
from psycopg2.extras import RealDictCursor

class Database:
    def __init__(self):
        # Altere para a sua senha do Postgres
        self.conn = psycopg2.connect(
            host="127.0.0.1",
            port="5432",
            database="tutorial",
            user="postgres",
            password="SUA_SENHA_AQUI"
        )

    def get_cursor(self):
        # O RealDictCursor faz o banco retornar os dados como dicionário/JSON
        return self.conn.cursor(cursor_factory=RealDictCursor)
