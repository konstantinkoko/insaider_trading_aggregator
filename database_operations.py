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


def db_add_user(user_id, name):
    with sql.connect("i_t_aggregator_db") as connect:
        connect.execute("""
            INSERT OR IGNORE INTO users (user_id, name, notification_time)
            VALUES(?,?,?)
            """, (user_id, name, "08:00"))


def db_get_companies_list(user_id):
    with sql.connect("i_t_aggregator_db") as connect:
        cursor = connect.execute("""
                SELECT * FROM users_companies
                WHERE user_id = ?;
                """, (user_id,))
        data = cursor.fetchall()
        content = [company[1] for company in data]
    return content


def db_add_company(user_id, ticker):
    with sql.connect("i_t_aggregator_db") as connect:
        connect.execute("""
            INSERT OR IGNORE INTO users_companies (user_id, ticker)
            VALUES(?,?)
        """, (user_id, ticker))


def db_delete_company(user_id, ticker):
    with sql.connect("i_t_aggregator_db") as connect:
        connect.execute("""
            DELETE FROM users_companies
            WHERE user_id = ? AND ticker = ?;
        """, (user_id, ticker))
        status = "ok"
    return status


def db_set_notification_time(user_id, time):
    with sql.connect("i_t_aggregator_db") as connect:
        connect.execute("""
            UPDATE users
            SET notification_time = ?
            WHERE user_id = ?
        """, (time, user_id))
        status = "ok"
    return status


def db_get_company_id(ticker, company_name):
    with sql.connect("i_t_aggregator_db") as connect:
        cursor = connect.execute("""
                SELECT company_id FROM companies
                WHERE company_name = ?;
                """, (company_name,))
        data = cursor.fetchall()
    company_id = data[0][0]
    return company_id


'''
def notifications():
    with sql.connect("i_t_aggregator_db") as connect:
        cursor = connect.execute("""
                SELECT * FROM users;
                """)
        data = cursor.fetchall()

    for user_info in data:
        user_id = user_info[0]
        notification_time = user_info[2]
        companies_list = [db_get_companies_list(user_id)[i][1] for i in range(len(data))]
        content = []
        for ticker in companies_list:
            content.append(show_trading_info(ticker, "day"))
    return content
'''
