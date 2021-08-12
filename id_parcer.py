import requests
from bs4 import BeautifulSoup
import sqlite3 as sql


def company_name_format(company_name):
    exception_list = ['ао', 'ao', 'оао', 'oao', 'зао', 'пао', 'ооо', 'ooo', '"', "«", "»", '']
    separator_list = ['"', "«", "»"]
    _company_name = [i.strip('«»"().,').strip('«»"().,') for i in company_name.lower().split()]
    company_name = ' '.join(_company_name)
    for symbol in separator_list:
        _company_name = company_name.split(symbol)
        company_name = ' '.join(_company_name)

    _company_name = company_name.split()
    company_name = ' '
    for i in _company_name:
        if i not in exception_list:
            if company_name[-1] != '-' and i[0] != '-':
                company_name += " " + i
            else:
                company_name += i
    return company_name.strip()


flag = True
id = 1
#38312

while id < 38312:
    r = requests.get('https://e-disclosure.ru/portal/company.aspx?id=' + str(id))

    soup = BeautifulSoup(r.text, 'html.parser')
    name = soup.find("h2").text

    if 'Запрошенная страница не существует.' not in name:
        _name = company_name_format(name)
        print(f'"{_name}" : "{id}",')
        with sql.connect('i_t_aggregator_db') as connect:
            connect.execute("""
                INSERT OR REPLACE INTO companies (company_id, company_name, ticker)
                VALUES(?,?,?);
            """, (id, _name, None))
    id += 1