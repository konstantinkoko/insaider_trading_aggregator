import requests
from bs4 import BeautifulSoup
import sqlite3 as sql

flag = True
id = 4524
#38312

while id < 38312:
    r = requests.get('https://e-disclosure.ru/portal/company.aspx?id=' + str(id))

    soup = BeautifulSoup(r.text, 'html.parser')
    name = soup.find("h2").text

    if 'Запрошенная страница не существует.' not in name:
        print(f'"{name}" : "{id}",')
        with sql.connect('i_t_aggregator_db') as connect:
            connect.execute("""
                INSERT OR REPLACE INTO companies (company_id, company_name, ticker)
                VALUES(?,?,?);
            """, (id, name, None))
    id += 1