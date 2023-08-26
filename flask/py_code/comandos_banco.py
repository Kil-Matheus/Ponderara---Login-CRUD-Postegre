import psycopg2

class Banco():
    def __init__(self):
        self.db_conn = psycopg2.connect(
            dbname="postgres",
            user="postgres",
            password="senha",
            host="db",
            port="5432"
        )
        self.valores = None
    
    
    def create(self, nome_tabela):
        try:
            with self.db_conn.cursor() as cursor:
                cursor.execute(f'CREATE TABLE IF NOT EXISTS {nome_tabela} (nome TEXT, idade INTEGER)')
                self.db_conn.commit()
        except psycopg2.Error as e:
            raise Exception(f'Erro ao criar tabela: {e}')
    
    def select(self):
        try:
            with self.db_conn.cursor() as cursor:
                cursor.execute('SELECT * FROM bloco')
                valores = cursor.fetchall()
                return valores
        except psycopg2.Error as e:
            raise Exception(f'Erro ao selecionar: {e}')
    
    def delete(self, valor):
        try:
            with self.db_conn.cursor() as cursor:
                cursor.execute('DELETE FROM bloco WHERE title = %s', (valor,))
                self.db_conn.commit()
                valores = self.select()
                return valores
        except psycopg2.Error as e:
            raise Exception(f'Erro ao deletar: {e}')
    
    def update(self, title, new_title, new_contents):
        try:
            with self.db_conn.cursor() as cursor:
                cursor.execute('UPDATE bloco SET title = %s, contents = %s WHERE title = %s', (new_title, new_contents, title))
                self.db_conn.commit()
                valores = self.select()
                return valores
        except psycopg2.Error as e:
            raise Exception(f'Erro ao atualizar: {e}')
    
    def insert(self, nome, valor):
        try:
            with self.db_conn.cursor() as cursor:
                cursor.execute('INSERT INTO bloco VALUES (%s, %s)', (nome, valor))
                self.db_conn.commit()
                valores = self.select()
                return valores
        except psycopg2.Error as e:
            raise Exception(f'Erro ao inserir: {e}')
