# 📈 NSE Stock Tracker — Django + Selenium

This is a web application that scrapes live stock data from the **Nairobi Securities Exchange (NSE)** using **Selenium**, stores it in a **database**, and displays it in a responsive dashboard built with **Django** and **Tailwind CSS**.

---

## 💡 Features

- ✅ Real-time web scraping using Selenium
- ✅ Headless Chrome for automation
- ✅ Data stored in SQLite/MSSQL via Django ORM
- ✅ Tailwind CSS styled dashboard
- ✅ Live chart updates with Chart.js
- ✅ Dark mode toggle
- ✅ Searchable, responsive table layout
- ✅ Stock detail modal with real-time chart

---

## 🚀 Technologies Used

| Tech           | Description                                |
|----------------|--------------------------------------------|
| Python 3.13     | Backend logic                              |
| Django 5.2.1    | Web framework                              |
| Selenium        | Web scraping automation                    |
| ChromeDriver    | Headless browser control                   |
| Chart.js        | Live data charting                         |
| Tailwind CSS    | Modern frontend design                     |
| SQLite / MSSQL  | Database storage (configured via Django)   |
| Git & GitHub    | Version control & source code hosting      |
| VS Code         | Code editing with Python & Django plugins  |

---

## 🛠 Setup Instructions

```bash
# Clone this repository
git clone https://github.com/Imuru-Samson/nse-stock-tracker.git

# Create and activate virtual environment
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt  # If created

# Run database migrations
python manage.py migrate

# Run the Selenium scraper
python nse_selenium_loader.py

# Start the development server
python manage.py runserver
