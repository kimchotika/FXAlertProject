import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import requests
from datetime import datetime, timedelta

# Fetch historical USD/THB rates
def fetch_historical_rates(days=90):
    end_date = datetime.today()
    start_date = (end_date - timedelta(days=days)).strftime("%Y-%m-%d")
    end_date_str = end_date.strftime("%Y-%m-%d")
    url = f"https://api.frankfurter.app/{start_date}..{end_date_str}?from=USD&to=THB"

    try:
        response = requests.get(url)
        data = response.json()
        rates = [(date, rate["THB"]) for date, rate in data["rates"].items()]
        rates.sort()
        return pd.DataFrame(rates, columns=["date", "rate"])
    except Exception as e:
        print("❌ Error fetching historical rates:", e)
        return pd.DataFrame()

# Main analysis and plot
def analyze_fx(days=90):
    df = fetch_historical_rates(days)

    if df.empty or df['rate'].isnull().all():
        return None, "⚠️ Could not fetch exchange rate data. Please try again later.", None

    df['date'] = pd.to_datetime(df['date'])
    df['ma_7'] = df['rate'].rolling(window=7).mean()
    df['ma_30'] = df['rate'].rolling(window=30).mean()
    latest = df.iloc[-1]

    mean = df['rate'].mean()
    std = df['rate'].std()

    best_top = mean - 1.5 * std
    good_top = mean - 1.0 * std
    fair_top = mean - 0.25 * std
    market_top = mean + 0.25 * std
    expensive_top = df['rate'].max() + 0.5
    y_min = df['rate'].min() - 0.5

    rate = latest['rate']
    if rate < best_top:
        recommendation = "🔥 Best Deal — extremely favorable to exchange!"
    elif rate < good_top:
        recommendation = "💸 Good Deal — strong opportunity."
    elif rate < fair_top:
        recommendation = "✅ Fair Rate — reasonable time to exchange."
    elif rate < market_top:
        recommendation = "🤝 Market Rate — normal, no urgency."
    else:
        recommendation = "⚠️ Expensive — above average, best to wait."

    fig, ax = plt.subplots(figsize=(12, 6))

    ax.plot(df['date'], df['ma_7'], label='7-day MA', color='teal', linestyle='--')
    ax.plot(df['date'], df['ma_30'], label='30-day MA', color='tomato', linestyle=':')
    ax.fill_between(df['date'], y_min, best_top, color='#fdecea', alpha=0.6)
    ax.fill_between(df['date'], best_top, good_top, color='#f3e5f5', alpha=0.6)
    ax.fill_between(df['date'], good_top, fair_top, color='#e8f5e9', alpha=0.6)
    ax.fill_between(df['date'], fair_top, market_top, color='#e3f2fd', alpha=0.6)
    ax.fill_between(df['date'], market_top, expensive_top, color='#fff8e1', alpha=0.6)

    ax.plot(df['date'], df['rate'], color='violet', linewidth=2, label='USD/THB')
    ax.scatter(latest['date'], latest['rate'], color='red', zorder=5)
    ax.text(latest['date'], latest['rate'] + 0.1, f"{latest['rate']:.2f}", color='red', fontsize=10, ha='center')

    # Add labels for zones
    x_pos = df['date'].iloc[0]
    ax.text(x_pos, (y_min + best_top)/2, "Best Deal", color='red', fontsize=9, va='center')
    ax.text(x_pos, (best_top + good_top)/2, "Good Deal", color='purple', fontsize=9, va='center')
    ax.text(x_pos, (good_top + fair_top)/2, "Fair Rate", color='green', fontsize=9, va='center')
    ax.text(x_pos, (fair_top + market_top)/2, "Market", color='gray', fontsize=9, va='center')
    ax.text(x_pos, (market_top + expensive_top)/2, "Expensive", color='orange', fontsize=9, va='center')

    # Format x-axis date labels
    ax.set_title(f'THB/USD Exchange Rate Trend (Last {days} Days)')
    ax.set_ylabel('USD per 1 THB')
    ax.set_yticks(np.arange(round(y_min, 1), round(expensive_top, 1), 0.5))
    ax.xaxis.set_major_locator(mdates.AutoDateLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))
    plt.xticks(rotation=45)
    ax.set_facecolor('white')
    ax.legend()
    ax.grid(False)

    return fig, recommendation, latest['rate']

# Streamlit app layout
st.set_page_config(page_title="FX Alert", layout="wide")
st.title("💸 FX Alert – Should You Buy USD With THB Today?")
days = st.selectbox("📅 Select trend window:", [30, 90, 365])

fig, recommendation, today_rate = analyze_fx(days)

if fig:
    st.pyplot(fig)
    st.markdown(f"### 📌 Today’s Rate: **{today_rate:.2f} THB/USD**")
    st.success(recommendation)
else:
    st.error(recommendation)