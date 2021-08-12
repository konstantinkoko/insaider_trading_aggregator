import requests
from bs4 import BeautifulSoup

def ticker_check(ticker):
    response = requests.get(f"https://iss.moex.com/iss/securities/{ticker}.json")  # https://iss.moex.com/iss/reference/
    company_info = response.json()
    right_check = False
    if len(company_info["description"]["data"]) > 0:
        currency = company_info["description"]["data"][7][2]
        ticker = company_info["description"]["data"][0][2]
        company_name = company_info["description"]["data"][1][2]
        if currency != "SUR":
            status = "не в рублях"
        else:
            status = "ok"
            right_check = True
    else:
        status = "тикер не найден"
    return [ticker, right_check, status, company_name]


def make_event_info(event_info_url, date, time):

    info_dict = {'date': date, 'time': time, 'event_info_url': event_info_url}
    r = requests.get(event_info_url)

    soup = BeautifulSoup(r.text, 'html.parser')
    info = soup.find("div", style="word-break: break-word; word-wrap: break-word;")
    for br in info.find_all('br'):
        text = br.next_sibling
        if str(text)[:4] =='2.1.':
            info_dict['name'] = ' '.join(text.strip('.').split()[-3:])
        if str(text)[:4] =='2.2.':
            info_dict['post'] = ' '.join(text.strip('.').split()[14:])
        if str(text)[:4] == '2.4.':
            info_dict['before'] = []
            for i in text.split():
                if '%' in i:
                    info_dict['before'].append(i.strip('–.'))
        if str(text)[:4] == '2.5.':
            info_dict['after'] = []
            for i in text.split():
                if '%' in i:
                    info_dict['after'].append(i.strip('–.'))
    return info_dict


def event_list(company_id, year):
    r = requests.get('https://e-disclosure.ru/Event/Page?companyId=' + str(company_id) + '&year=' + str(year))

    soup = BeautifulSoup(r.text, 'html.parser')

    info = []
    for i in soup.find_all("tr")[1:]:
        columns = i.find_all("td")
        if 'Изменение размера доли участия' in columns[2].text:
            date = columns[1].text.split()[0]
            time = columns[1].text.split()[1]
            event_info_url = columns[2].a['href']
            #try:
            #    info.append(make_event_info(event_info_url, date, time))
            #except:
            #    info.append('no data')
            info.append(f"date: {date}\ntime: {time}\nevent_url: {event_info_url}\n\n")
    info.reverse()
    return info


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


def show_trading_info(ticker, period):
    ticker_info = ticker_check(ticker)  # [ticker_format, right_check, status, company_name]
    ticker = ticker_info[0]
    status = ticker_info[2]
    company_name = ticker_info[3]
    if ticker_info[1]:
        company_id = get_company_id(ticker, company_name)
        info = event_list(company_id, year=2020)
    else:
        info = status
    return info
