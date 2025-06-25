import requests
import time
import socket
import django
import os

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'stock_site.settings')
django.setup()

from stocks.models import Stock

# Your RapidAPI key
API_KEY = "728e9bf5c6msh29fdb9bf2d25bafp1ebf5ajsnb19c9a59aed8"
url = "https://nairobi-stock-exchange-nse.p.rapidapi.com/stocks"
headers = {
    "x-rapidapi-host": "nairobi-stock-exchange-nse.p.rapidapi.com",
    "x-rapidapi-key": API_KEY
}

def is_connected(host="8.8.8.8", port=53, timeout=3):
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except Exception:
        return False

def fetch_data():
    print("🌐 Checking internet connection...")
    if not is_connected():
        print("❌ No internet connection. Please connect and try again.")
        return

    print("\n⏳ Fetching data from NSE API...")
    for attempt in range(1, 4):
        try:
            response = requests.get(url, headers=headers, timeout=30)
            if response.status_code == 200:
                print(f"✅ Data fetched successfully on attempt {attempt}.")
                data = response.json()

                if not isinstance(data, list):
                    print("⚠️ Unexpected data format:", data)
                    return

                print(f"✅ Total records received: {len(data)}")
                save_to_db(data)
                return
            else:
                print(f"❌ Attempt {attempt}: Failed to fetch data (Status code: {response.status_code})")
        except requests.exceptions.Timeout:
            print(f"❌ Attempt {attempt}: Request timed out.")
        except Exception as e:
            print(f"❌ Attempt {attempt}: Error occurred - {e}")

        if attempt < 3:
            print("🔁 Retrying in 5 seconds...")
            time.sleep(5)

    print("❌ All attempts failed. Please check your internet connection and API key.")

def save_to_db(data):
    Stock.objects.all().delete()
    for item in data:
        raw_price = item.get("price", "0.0")
        try:
            # Remove commas before converting to float
            clean_price = float(str(raw_price).replace(",", ""))
        except ValueError:
            print(f"⚠️ Skipping stock with invalid price: {raw_price}")
            continue

        Stock.objects.create(
            symbol=item.get("symbol", "N/A"),
            name=item.get("name", "Unknown"),
            price=clean_price
        )
    print("✅ Stock data saved to database.")

if __name__ == "__main__":
    fetch_data()
