from database_operations import db_add_user, db_get_companies_list, db_add_company, db_delete_company, \
    db_set_notification_time, db_get_company_id
from parcer import event_list, ticker_check


def add_user(user_id, name):
    db_add_user(user_id, name)


def get_companies_list(user_id):
    content = db_get_companies_list(user_id)
    return content


def add_company(user_id, ticker):
    ticker_info = ticker_check(ticker)
    ticker = ticker_info[0]
    status = ticker_info[2]
    if ticker_info[1]:
        db_add_company(user_id, ticker)
    return status


def delete_company(user_id, ticker):
    status = db_delete_company(user_id, ticker)
    return status


def set_notification_time(user_id, time):
    status = db_set_notification_time(user_id, time)
    return status


def show_trading_info(ticker, period):
    ticker_info = ticker_check(ticker)  # [ticker_format, right_check, status, company_name]
    ticker = ticker_info[0]
    status = ticker_info[2]
    company_name = company_name_format(ticker_info[3])
    if ticker_info[1]:
        company_id = db_get_company_id(ticker, company_name)
        info = event_list(company_id, year=2020)
    else:
        info = status
    return info


def company_name_format(company_name):
    exception_list = ['ао', 'ao', 'оао', 'oao', 'зао', 'пао', 'ооо', 'ooo', 'нк', '"', "«", "»", '']
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
    return company_name.strip(' -')
