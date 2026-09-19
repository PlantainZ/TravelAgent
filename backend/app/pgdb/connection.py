import psycopg2

# 改成你自己的数据库连接信息
DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "dbname": "your_database",
    "user": "your_user",
    "password": "your_password",
}

def get_one_row():
    """连接数据库，取一行数据"""
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    cur.execute("SELECT * FROM your_table LIMIT 1")  # 改成你的表名
    row = cur.fetchone()
    columns = [desc[0] for desc in cur.description]  # 拿到列名
    cur.close()
    conn.close()
    # 把 (col1, col2, ...) 转成 {col1: val1, col2: val2, ...}
    if row:
        return dict(zip(columns, [str(v) for v in row]))
    return None