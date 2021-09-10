import requests
from datetime import datetime, timedelta
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


def make_event_info(event_info_url):

    info_dict = {}
    r = requests.get(event_info_url)

    soup = BeautifulSoup(r.text, 'html.parser')
    info = soup.find("div", style="word-break: break-word; word-wrap: break-word;")
    text_list = []
    for br in info.find_all('br'):
        text_list.append(str(br.next_sibling))
    #print(text_list)
    for i, string in enumerate(text_list):
        if string[:4] == '2.1.':
            info_dict['name'] = text_list[i+1].strip('.')
        if string[:4] == '2.2.':
            info_dict['post'] = text_list[i+1].strip('.')
        if string[:4] == '2.5.':
            before = text_list[i+1].strip('.').split()[0].split('/')[0].strip('%')
        if string[:4] == '2.6.':
            after = text_list[i+1].strip('.').split()[0].split('/')[0].strip('%')
    #print(before, float(before))
    #print(after, float(after))
    #print(after - before)
    info_dict['delta'] = 'ololo'
    return info_dict


def event_list(company_id, year, period):
    r = requests.get('https://e-disclosure.ru/Event/Page?companyId=' + str(company_id) + '&year=' + str(year))

    soup = BeautifulSoup(r.text, 'html.parser')

    info = []
    for i in soup.find_all("tr")[1:]:
        columns = i.find_all("td")
        if 'Изменение размера доли участия' in columns[2].text:
            date = columns[1].text.split()[0]
            time = columns[1].text.split()[1]
            event_info_url = columns[2].a['href']

            period_check = True
            time_delta = timedelta(days=1)
            if period == "day" and\
                    datetime.strptime(date + " " + time, "%d.%m.%Y %H:%M") + time_delta < datetime.today():
                period_check = False

            if period_check is True:
                try:
                    info_dict = make_event_info(event_info_url)
                except:
                    info_dict = {'name': '-------', 'post': '-------', 'delta': '-------'}
                info.append(f"date: {date}\ntime: {time}\nname: {info_dict['name']}\npost: {info_dict['post']}\n"
                            f"delta: {info_dict['delta']}\nevent_url: {event_info_url}\n\n")
    info.reverse()
    return info
