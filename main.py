import bs4
import requests
import numpy as np
import pandas as pd
import sys

from operator import itemgetter
from IPython.display import display
pd.set_option('display.max_rows', 500)

url = sys.argv[1]


def get_portfolio_data():
    html = requests.get(url)
    parsed_html = bs4.BeautifulSoup(html.content, 'html.parser')

    portfolio = []
    total = 0
    for tr in parsed_html.find_all('tbody')[0].find_all('tr'):
        name = tr.find_all('td', {'class': 'FormData'})
        value = tr.find_all('td', {'class': 'FormDataR'})
        if len(name) == 0 or len(value) == 0:
            continue

        name, title = name[0].text, name[1].text
        value = value[0].text.replace(',', '')

        portfolio.append({
            'name': name,
            'title': title,
            'value': int(value)
        })
        total += int(value)
    for data in portfolio:
        data['per'] = f"{str(round(100 * float(data['value']) / float(total),2))}%"

    return sorted(portfolio, key=itemgetter('value'), reverse=True)


def get_total_percentage(data):
    total = 0
    for d in data:
        total += float(d['per'].replace('%', ''))
    return round(total, 2)


def get_dataframe(data):
    df = pd.DataFrame(data)
    df.index += 1
    return df


if __name__ == "__main__":
    portfolio = get_portfolio_data()
    portfolio15 = portfolio[:15]
    df = get_dataframe(portfolio15)

    print(f"\n{df}")
    print(f"\ntotal percentage: {get_total_percentage(portfolio15)}\n")
