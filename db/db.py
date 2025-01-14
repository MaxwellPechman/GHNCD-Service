from psycopg_pool import ConnectionPool


class PostgresInterface:
    def __init__(self,
                 db_name: str,
                 db_user: str,
                 db_password: str,
                 db_host: str,
                 db_port: int,
                 min_size: int = 1,
                 max_size: int = 50):
        self.pool = ConnectionPool(
            conninfo=f"dbname={db_name} user={db_user} password={db_password} host={db_host} port={db_port}",
            min_size=min_size,
            max_size=max_size,
        )

    def execute(self, sql: str, params: tuple = None):
        with self.pool.connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(sql, params)


    def dispose(self):
        self.pool.close()