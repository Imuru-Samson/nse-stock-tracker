#!C:\Users\imuru samson\Desktop\NSE_STOCK_TRACKER\venv\Scripts\python.exe

# === Python Standard Libraries ===
import os
import socket
import django

# === Selenium Libraries for Web Automation ===
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options

# === Django Setup to Access ORM ===
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'stock_site.settings')
django.setup()

# === Import the Stock model from your Django app ===
from stocks.models import Stock

# === Path to your ChromeDriver (Update if needed) ===
CHROME_DRIVER_PATH = r"C:\Users\Administrator\Downloads\chromedriver-win64\chromedriver-win64\chromedriver.exe"

# === Utility Function: Check Internet Connectivity ===
def is_connected(host="8.8.8.8", port=53, timeout=3):
    """
    Checks if the system is connected to the internet.
    Default host is Google's public DNS.
    """
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except Exception:
        return False

# === Main Function to Fetch and Scrape NSE Data ===
def fetch_data():
    print("🌐 Checking internet connection...")
    if not is_connected():
        print("❌ No internet connection.")
        return

    print("🚀 Launching headless Chrome browser...")
    # Configure Chrome options to run in headless mode (without GUI)
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")  # Updated headless mode
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")

    # Initialize Chrome WebDriver with your ChromeDriver path
    driver = webdriver.Chrome(service=Service(CHROME_DRIVER_PATH), options=chrome_options)

    try:
        # Target site: Kwayisi NSE stocks listing (uses static table)
        url = "https://afx.kwayisi.org/nse/"
        driver.get(url)

        # Optional: Screenshot for debugging purposes
        print("📸 Capturing screenshot of loaded page...")
        driver.save_screenshot("kwayisi_debug.png")
        print("✅ Screenshot saved")

        # Wait for the table to fully load (up to 20 seconds)
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "table tbody tr"))
        )

        # Extract all rows of the table
        rows = driver.find_elements(By.CSS_SELECTOR, "table tbody tr")
        if not rows:
            print("⚠️ No stock rows found.")
            return

        data = []  # To store extracted stocks

        # Loop through each row and extract relevant stock data
        for row in rows:
            cells = row.find_elements(By.TAG_NAME, "td")
            if len(cells) < 4:
                print("⚠️ Skipping row with insufficient columns")
                continue

            # Extract symbol, name, and price
            symbol = cells[0].text.strip()
            name = cells[1].text.strip()
            price_text = cells[3].text.strip().replace(",", "")  # Remove commas in price

            try:
                price = float(price_text)
            except ValueError:
                print(f"⚠️ Skipping {symbol} — invalid price format: {price_text}")
                continue

            data.append({"symbol": symbol, "name": name, "price": price})

        print(f"✅ Scraped {len(data)} stocks. Saving to database...")
        save_to_db(data)

    except TimeoutException:
        print("❌ Timeout waiting for stock table to load.")

    finally:
        # Always close the browser
        driver.quit()

# === Save the Extracted Data to Django Database ===
def save_to_db(data):
    """
    Clears existing Stock entries and saves new ones.
    """
    # Remove old stock data (optional: use update_or_create instead)
    Stock.objects.all().delete()

    # Add new data
    for item in data:
        Stock.objects.create(**item)

    print("✅ Stock data saved to database.")

# === Entry Point ===
if __name__ == "__main__":
    fetch_data()
