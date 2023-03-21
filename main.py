from bs4 import BeautifulSoup
import requests
import numpy as np
import pandas as pd

def main():
    html_text = requests.get('https://www.iexindia.com/marketdata/market_snapshot.aspx').text
    soup = BeautifulSoup(html_text, 'lxml')

    data = soup.find_all('td')

    df = []
    for i in range(96, 887):
        df.append(data[i].text)

    df = list(filter(lambda x: len(x) > 2, df))

    df = [[df[i] for i in range(j, j+7)] for j in range(0, len(df), 7)]
    headers = ["Time Block", "Purchase Bid (MW)", "Sell Bid (MW)", "MCV (MW)", "Final Scheduled Volume (MW)", "MCP (Rs/kWh)*", "Weighted MCP (Rs/MWh)"]

    df = pd.DataFrame(np.vstack(df), columns = headers)
    df = df.loc[:, ["Time Block", "MCP (Rs/kWh)*"]]
    
    # Orginally, the data retrieved has its MCP in Rs/MWh, which needs to be converted to Rs/kWh 
    # by dividing by 1000
    df["MCP (Rs/kWh)*"] = df["MCP (Rs/kWh)*"]/1000

    with open("data.csv",'w') as data_file:
        data_file.write(df.to_csv(index=False))

if __name__ == "__main__":
    main()
