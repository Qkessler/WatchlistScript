import os
import yfinance
import re
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from send_email import send_email
from collections import namedtuple
import logbook
from datetime import datetime, timedelta

Company = namedtuple('Company', 'ticker price buyprice')
app_log = logbook.Logger('App')

MAIL_TO_ADDRESS = os.environ['MAIL_TO_ADDRESS']
MAIL_SERVER = os.environ['MAIL_SERVER']
MAIL_FROM_ADDRESS = os.environ['MAIL_FROM_ADDRESS']
MAIL_FROM_PASSWORD = os.environ['MAIL_FROM_PASSWORD']
CLIENT_SECRET = os.environ['CLIENT_SECRET']


def main():
    print(CLIENT_SECRET)
    # sheet = init_spreadsheet()
    # tickers = get_tickers(sheet)
    # prices = get_prices(tickers)
    # buyprices = get_buyprices(sheet)
    # companies = construct_companies(tickers, prices, buyprices)
    # print(sheet, tickers, prices, buyprices, companies)
    # email_buyprice(companies)


def init_spreadsheet():
    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name(
        , scope)
    client = gspread.authorize(creds)
    sheet = client.open('WATCHLIST').sheet1
    return sheet


def get_tickers(sheet):
    tickers = sheet.col_values(1)[2:]
    return tickers


def get_buyprices(sheet):
    buyprices = sheet.col_values(2)[2:]
    return buyprices


def get_prices(list_tickers):
    prices = []
    if len(list_tickers) > 1:
        data = yfinance.download(tickers=list_tickers, period='1d')
        for name in list_tickers:
            ticker_price = data['Adj Close'][name][0]
            prices.append(round(ticker_price, 2))
    else:
        ticker_data = yfinance.Ticker(list_tickers[0])
        price = ticker_data.history(period='1d')['Close'][0]
        prices.append(price)
    return prices


def construct_companies(tickers, prices, buyprices):
    companies = []
    companies_length = len(tickers)
    for _ in range(companies_length):
        companies.append(Company(tickers[_], prices[_], float(buyprices[_])))
    return companies


def email_buyprice(companies):
    week = timedelta(days=7)
    for company in companies:
        last_company = None
        with open('/home/qkessler/Documents/watchlist_script/watchlist.log',
                  'r') as f:
            for line in f.readlines():
                if company.ticker in line:
                    last_company = line
        if last_company:
            pat = re.compile(r'\d+-\d+-\d+')
            date_str = pat.findall(last_company)
            date = datetime.strptime(date_str[0], '%Y-%m-%d').date()
        if not last_company or date <= datetime.date(datetime.today()) - week:
            if company.price <= company.buyprice:
                body = f'Hey Quique, \nThe company {company.ticker} '
                body += f'is under its buyprice, You should check it out!'
                body += f'\nThe current price is {company.price}'
                body += f'\nBye,\n Quique.'
                subject = f'Company {company.ticker} is on sale!'
                app_log.trace(f'Email was sent on company "{company.ticker}"')
                send_email(body, subject)
