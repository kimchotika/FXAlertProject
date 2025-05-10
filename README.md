# 💸 FX Alert – Should You Buy USD With THB Today?

**FX Tracker** is a lightweight web app that helps individuals and small businesses decide **when to buy USD with Thai Baht (THB)**. It analyzes live THB/USD exchange rate trends using statistical thresholds and visual zones — no guesswork, just data.

This project was inspired by:

> “I exchange THB to USD monthly — I wanted a tool that tells me when it’s the right time to convert.”

---

## 🔍 What It Does

- 📈 Visualizes the THB/USD rate over the past 30, 90, or 365 days
- 📊 Categorizes today’s rate into 5 meaningful zones:
  - 🔥 Best Deal — THB is historically strongest
  - 💸 Good Deal
  - ✅ Fair Rate
  - 🤝 Market Rate
  - ⚠️ Expensive — THB is weak
- 📍 Shows today's rate as a red dot with clear recommendation
- 📐 Adds 7-day and 30-day moving average lines for trend spotting
- 🟦 Uses a free public API — no signup, no CSV, just live data

---

## 🧠 Skills & Tools Demonstrated

### 💻 Technical Stack
- **Python** – data scripting and analysis
- **Streamlit** – interactive app interface
- **Pandas & NumPy** – statistical trend analysis
- **Matplotlib** – visualizing exchange rate bands and trends
- **Frankfurter API** – live exchange rate data (no API key)

### 🚀 Highlights
- Real-world decision modeling for foreign exchange
- Applies `mean ± std` logic to define "good" vs "bad" FX timing
- Clean UI and logic that non-technical users can understand
- Deployable on [Streamlit Cloud](https://streamlit.io/cloud)

---

## 📁 Project Structure

FXAlertProject/
- ├── app.py # Streamlit app (runs everything)
- ├── requirements.txt # Python dependencies
- └── README.md # You're reading this



---

## ⚙️ How to Run Locally

```bash
git clone https://github.com/kimchotika/FXAlertProject.git
cd FXAlertProject
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
