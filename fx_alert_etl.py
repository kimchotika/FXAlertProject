import requests
import pandas as pd
from datetime import datetime

def fetch_latest_rate():
    url = "https://api.exchangerate.host/latest?base=USD&symbols=THB"
    response = requests.get(url)
    data = response.json()
    print(data)  # 👈 Add this line
    rate = data["rates"]["THB"]
    return rate

if __name__ == "__main__":
    df = fetch_latest_rate()
    print(df)