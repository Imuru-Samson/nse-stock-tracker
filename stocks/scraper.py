# stocks/scraper.py

import requests
from bs4 import BeautifulSoup
from .models import Stock

def scrape_nse_stocks():
    url = "https://live.mystocks.co.ke/markets/securities"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print("❌ Failed to fetch stock data")
        return

    soup = BeautifulSoup(response.text, "html.parser")
    table = soup.find("table", class_="securities-table")

    if not table:
        print("❌ Could not find the stock table on mystocks.co.ke")
        return

    rows = table.find("tbody").find_all("tr")

    for row in rows:
        cols = row.find_all("td")
        if len(cols) >= 5:
            symbol = cols[0].text.strip()
            name = cols[1].text.strip()
            try:
                price = float(cols[4].text.strip().replace(",", ""))
            except ValueError:
                price = 0.0

            Stock.objects.update_or_create(
                symbol=symbol,
                defaults={
                    "name": name,
                    "price": price,
                }
            )
    
    print("✅ Stock data scraped and saved.")
