import sqlite3 as sql

def db_initialization():
    with sql.connect("i_t_aggregator_db") as connect:
        connect.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                name TEXT,
                notification_time TIME
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

def add_user(id, name):
    with sql.connect("i_t_aggregator_db") as connect:
        connect.execute("""
        
        """)
    pass

def get_companies_list(id):
    return []

def add_company(id, ticker):
    return "ok"

def delete_company(id, ticker):
    return "ok"

def set_notification_time(time):
    return "ok"
