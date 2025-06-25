# stocks/selenium_scraper.py

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
from .models import Stock

def scrape_nse_with_selenium():
    options = Options()
    options.add_argument('--headless')  # Run in background
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    service = Service(executable_path="C:/path/to/chromedriver.exe")  # UPDATE THIS PATH
    driver = webdriver.Chrome(service=service, options=options)

    try:
        driver.get("https://www.nse.co.ke/market-data/equities-securities.html")
        time.sleep(5)  # wait for page to load

        # You might need to inspect and adjust table class/id
        table = driver.find_element(By.TAG_NAME, "table")
        rows = table.find_elements(By.TAG_NAME, "tr")[1:]  # skip header

        for row in rows:
            cols = row.find_elements(By.TAG_NAME, "td")
            if len(cols) >= 3:
                symbol = cols[0].text.strip()
                name = cols[1].text.strip()
                try:
                    price = float(cols[2].text.strip().replace(",", ""))
                except ValueError:
                    price = 0.0

                Stock.objects.update_or_create(
                    symbol=symbol,
                    defaults={
                        "name": name,
                        "price": price,
                    }
                )

        print("✅ NSE stock data scraped with Selenium and saved.")
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        driver.quit()
