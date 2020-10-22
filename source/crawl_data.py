from bs4 import BeautifulSoup
import requests
import pandas as pd
import csv

file_path = "D:\Yeat3_Ser1\BigData\KT_Giuaky\ex1"

#function
def get_page_content(url):
  page = requests.get(url, headers={"Accept-Language":"en-US"})
  return BeautifulSoup(page.text, "lxml")

def export_table_and_print(data):
  table = pd.DataFrame(data, columns=['Date', 'Open', 'High', 'Low', 'Close', 'Volume','Market Cap']);
  table.index = table.index + 1
  table.to_csv(file_path + "\crawl_result.csv", sep=',', encoding='utf-8', index=False)

def get_element_arrtributes(day):
  date = day.find('td', class_='cmc-table__cell cmc-table__cell--sticky cmc-table__cell--left').find('div').text
  opens = day.findAll('td', class_='cmc-table__cell cmc-table__cell--right')[0].get_text()
  high = day.findAll('td', class_='cmc-table__cell cmc-table__cell--right')[1].get_text()
  low = day.findAll('td', class_='cmc-table__cell cmc-table__cell--right')[2].get_text()
  close = day.findAll('td', class_='cmc-table__cell cmc-table__cell--right')[3].get_text()
  volume = day.findAll('td', class_='cmc-table__cell cmc-table__cell--right')[4].get_text()
  market_cap = day.findAll('td', class_='cmc-table__cell cmc-table__cell--right')[5].get_text()

  data['Date'].append(date if date else '')
  data['Open'].append(opens if  opens else '')
  data['High'].append(high if high else '')
  data['Low'].append(low if low else '')
  data['Close'].append(close if close else '')
  data['Volume'].append(volume if volume else '')
  data['Market Cap'].append(market_cap if market_cap else '')

def parse_page(url):
  soup = get_page_content(url)

  allday_data = soup.findAll('tr', class_='cmc-table-row')

  for day in allday_data:
    get_element_arrtributes(day)

  export_table_and_print(data)
#global
url = 'https://coinmarketcap.com/currencies/bitcoin/historical-data/?start=20190925&end=20200925'

data = {
  'Date' : [],
  'Open' : [],
  'High' : [],
  'Low' : [],
  'Close' : [],
  'Volume' : [],
  'Market Cap' : []
}

parse_page(url)