def create_sql_index_code(start_year: int, current_year: int) -> str:
    year = start_year
    sql_code = ""

    while year <= current_year:
        sql_index_code = f"CREATE INDEX \"index-{year}\" ON \"data_{year}\" (id);"
        sql_code = sql_code + sql_index_code + "\n"
        year += 1

    return sql_code


def create_sql_index_drop_code(start_year: int, current_year: int) -> str:
    year = start_year
    sql_code = ""

    while year <= current_year:
        sql_index_code = f"DROP INDEX \"index-{year}\";"
        sql_code = sql_code + sql_index_code + "\n"
        year += 1

    return sql_code


def create_sql_partition_code(start_year: int, current_year: int) -> str:
    year = start_year
    sql_code = ""

    while year <= current_year:
        sql_partition_code = f"""
            CREATE TABLE data_{year} (
                id TEXT NOT NULL,
                date DATE NOT NULL,
                element TEXT NOT NULL,
                data_value NUMERIC,
                m_flag CHAR,
                q_flag CHAR,
                s_flag CHAR,
                obs_time TEXT
            ) PARTITION BY RANGE (date);
        
            CREATE TABLE data_{year}_01 PARTITION OF data_{year}
                FOR VALUES FROM ('{year}-01-01') TO ('{year}-02-01');
                
            CREATE TABLE data_{year}_02 PARTITION OF data_{year}
                FOR VALUES FROM ('{year}-02-01') TO ('{year}-03-01');
                
            CREATE TABLE data_{year}_03 PARTITION OF data_{year}
                FOR VALUES FROM ('{year}-03-01') TO ('{year}-04-01');
                
            CREATE TABLE data_{year}_04 PARTITION OF data_{year}
                FOR VALUES FROM ('{year}-04-01') TO ('{year}-05-01');
                
            CREATE TABLE data_{year}_05 PARTITION OF data_{year}
                FOR VALUES FROM ('{year}-05-01') TO ('{year}-06-01');
                
            CREATE TABLE data_{year}_06 PARTITION OF data_{year}
                FOR VALUES FROM ('{year}-06-01') TO ('{year}-07-01');
                
            CREATE TABLE data_{year}_07 PARTITION OF data_{year}
                FOR VALUES FROM ('{year}-07-01') TO ('{year}-08-01');
                
            CREATE TABLE data_{year}_08 PARTITION OF data_{year}
                FOR VALUES FROM ('{year}-08-01') TO ('{year}-09-01');
                
            CREATE TABLE data_{year}_09 PARTITION OF data_{year}
                FOR VALUES FROM ('{year}-09-01') TO ('{year}-10-01');
                
            CREATE TABLE data_{year}_10 PARTITION OF data_{year}
                FOR VALUES FROM ('{year}-10-01') TO ('{year}-11-01');
                
            CREATE TABLE data_{year}_11 PARTITION OF data_{year}
                FOR VALUES FROM ('{year}-11-01') TO ('{year}-12-01');
                
            CREATE TABLE data_{year}_12 PARTITION OF data_{year}
                FOR VALUES FROM ('{year}-12-01') TO ('{year+1}-01-01');
            
            INSERT INTO data_{year} (id, date, element, data_value, m_flag, q_flag, s_flag, obs_time)
            SELECT id, date, element, data_value, m_flag, q_flag, s_flag, obs_time FROM \"{year}\";
            
            DROP TABLE  \"{year}\";
        """
        sql_code = sql_code + sql_partition_code + "\n"
        year += 1

    return sql_code


print(create_sql_index_code(1763, 2025))
