import yfinance as yf
import pandas as pd

import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt

tesla=yf.Ticker('TSLA')
tesla_data=tesla.history(period='max').reset_index()
# print(tesla_data.head(5))

url='https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/revenue.htm'
html_data=requests.get(url)
if html_data.status_code==200:
    soup=BeautifulSoup(html_data.text,'html.parser')
    tables=soup.find_all('table')[1]
    rows=tables.find_all('tr')


    data=[]  # get the content of column and append them to later convert them to data frame

    for row in rows:
        col=row.find_all('td')
        if len(col)==2:
            date_=col[0].text.strip()
            revenue_=col[1].text.strip()

            data.append([date_,revenue_])

    tesla_revenue=pd.DataFrame(data,columns=['Date','Revenue'])

    tesla_revenue.dropna(inplace=True)
    tesla_revenue['Revenue'] = tesla_revenue['Revenue'].str.replace(',', '',regex=False).str.replace('$', '',regex=False)
    tesla_revenue = tesla_revenue[tesla_revenue['Revenue'] != ""]
    
    tesla_revenue['Date'] = pd.to_datetime(tesla_revenue['Date'])
    tesla_revenue['Revenue'] = pd.to_numeric(tesla_revenue['Revenue'])
    
    def make_graph(stock_data, revenue_data, stock):
        stock_data_specific = stock_data[stock_data.Date <= '2021-06-14']
        revenue_data_specific = revenue_data[revenue_data.Date <= '2021-04-30']

        fig, axes = plt.subplots(2, 1, figsize=(12, 8), sharex=True)

        # Stock price
        axes[0].plot(pd.to_datetime(stock_data_specific.Date), stock_data_specific.Close, label="Share Price", color="blue")
        axes[0].set_ylabel("Price ($US)")
        axes[0].set_title(f"{stock} - Historical Share Price")

        # Revenue
        axes[1].plot(pd.to_datetime(revenue_data_specific.Date), revenue_data_specific.Revenue, label="Revenue", color="green")
        axes[1].set_ylabel("Revenue ($US Millions)")
        axes[1].set_xlabel("Date")
        axes[1].set_title(f"{stock} - Historical Revenue")

        plt.tight_layout()
        plt.savefig("graph.png") #Savves image
        plt.show()
    make_graph(tesla_data,tesla_revenue,'Tesla')
