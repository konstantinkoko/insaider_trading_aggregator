import sqlite3 as sql

def db_initialization():
    with sql.connect("i_t_aggregator_db") as connect:
        connect.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                name TEXT,
                notification_time TEXT
                );
            """)
        connect.execute("""
            CREATE TABLE IF NOT EXISTS companies (
                company_id INTEGER PRIMARY KEY,
                company_name TEXT,
                ticker TEXT
                );
            """)
        connect.execute("""
            CREATE TABLE IF NOT EXISTS users_companies (
                user_id INTEGER,
                ticker TEXT,
                CONSTRAINT p_key PRIMARY KEY (user_id, ticker)
                );
            """)

def add_user(user_id, name):
    with sql.connect("i_t_aggregator_db") as connect:
        connect.execute("""
            INSERT OR IGNORE INTO users (user_id, name, notification_time)
            VALUES(?,?,?)
            """, (user_id, name, "08:00"))

def get_companies_list(user_id):
    with sql.connect("i_t_aggregator_db") as connect:
        cursor = connect.execute("""
                SELECT * FROM users_companies
                WHERE user_id = ?;
                """, (user_id,))
        data = cursor.fetchall()
    return str(data)

def add_company(user_id, ticker):
    with sql.connect("i_t_aggregator_db") as connect:
        connect.execute("""
            INSERT OR IGNORE INTO users_companies (user_id, ticker)
            VALUES(?,?)
        """, (user_id, ticker))
    return "ok"

def delete_company(user_id, ticker):
    with sql.connect("i_t_aggregator_db") as connect:
        connect.execute("""
            DELETE FROM users_companies
            WHERE user_id = ? AND ticker = ?;
        """, (user_id, ticker))
    return "ok"

def set_notification_time(user_id, time):
    with sql.connect("i_t_aggregator_db") as connect:
        connect.execute("""
            UPDATE users
            SET notification_time = ?
            WHERE user_id = ?
        """, (time, user_id))
    return "ok"

