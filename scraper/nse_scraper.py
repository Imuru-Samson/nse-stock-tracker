import requests
from bs4 import BeautifulSoup
from datetime import datetime

# For now we’ll just print the scraped data

def fetch_nse_stocks():
    url = 'https://www.nse.co.ke/market-statistics/equity-market.html'
    headers = {
        'User-Agent': 'Mozilla/5.0'
    }

    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        print(f"Failed to fetch page. Status code: {response.status_code}")
        return

    soup = BeautifulSoup(response.text, 'html.parser')

    # Example: This will need to be customized based on the actual HTML structure
    rows = soup.select('table.table tbody tr')

    stocks = []

    for row in rows:
        cols = row.find_all('td')
        if len(cols) < 5:
            continue
        
        try:
            ticker = cols[0].text.strip()
            name = cols[1].text.strip()
            price = float(cols[2].text.strip().replace(',', ''))
            volume = int(cols[4].text.strip().replace(',', ''))
            
            stocks.append({
                'ticker': ticker,
                'name': name,
                'price': price,
                'volume': volume,
                'date_fetched': datetime.now()
            })
        except Exception as e:
            print("Error parsing row:", e)

    return stocks


if __name__ == '__main__':
    stock_data = fetch_nse_stocks()
    for stock in stock_data:
        print(stock)
