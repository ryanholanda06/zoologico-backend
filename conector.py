import psycopg2
from psycopg2.extras import RealDictCursor

class Database:
    def __init__(self):
        self.host = "127.0.0.1"
        self.port = "5432"
        self.database = "tutorial"
        self.user = "postgres"
        self.password = "Js182@09"

    def get_connection(self):
        return psycopg2.connect(
            host=self.host,
            port=self.port,
            database=self.database,
            user=self.user,
            password=self.password
        )

    def execute_select(self, query, params=None):
        conn = self.get_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute(query, params or ())
        res = cursor.fetchall()
        cursor.close()
        conn.close()
        return res

    def execute_statement(self, query, params=None):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(query, params or ())
        conn.commit()
        cursor.close()
        conn.close()