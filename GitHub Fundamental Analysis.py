import streamlit as st
import pandas as pd
import yfinance as yf

from PIL import Image
from io import BytesIO

st.set_page_config(page_title="Анализ акций", layout="wide")

def safe_get(info, key, multiplier=1, suffix="", percent=False):
    value = info.get(key)
    if value is None:
        return "Н/Д", "🔴 Плохо"
    try:
        val = round(value * multiplier, 2) if isinstance(value, (int, float)) else value
        if percent:
            val = f"{val:.2f}%"
        return f"{val}{suffix}", "🟢 Хорошо"
    except:
        return "Н/Д", "🔴 Плохо"

def get_data(ticker):
    try:
        stock = yf.Ticker(ticker)
        info = stock.info

        if not isinstance(info, dict) or not info:
            st.error("Не удалось получить данные по тикеру.")
            return []

        data = []

        def add(label, key, multiplier=1, suffix="", percent=False):
            value, rating = safe_get(info, key, multiplier, suffix, percent)
            data.append({"Показатель": label, "Значение": value, "Оценка": rating})

        # Добавление доступных показателей
        add("P/E (TTM)", "trailingPE")
        add("Forward P/E", "forwardPE")
        add("P/B", "priceToBook")
        add("P/S", "priceToSalesTrailing12Months")
        data.append({"Показатель": "P/FCF", "Значение": "Н/Д (отриц. FCF)", "Оценка": "🔴 Плохо"})
        add("D/E", "debtToEquity")
        add("PEG Ratio", "pegRatio")
        add("Enterprise Value", "enterpriseValue", 1e-6, " млн")
        data.append({"Показатель": "Peter Lynch Price (PLP)", "Значение": "Недоступен", "Оценка": "🔵 Нейтрально"})
        data.append({"Показатель": "Piotroski F-Score", "Значение": "Недоступно", "Оценка": "🔵 Нейтрально"})
        data.append({"Показатель": "Altman Z-Score", "Значение": "Недоступно", "Оценка": "🔵 Нейтрально"})
        data.append({"Показатель": "Beneish M-Score", "Значение": "Недоступно", "Оценка": "🔵 Нейтрально"})
        add("Dividend Yield (%)", "dividendYield", percent=True)
        add("Payout Ratio", "payoutRatio", percent=True)
        data.append({"Показатель": "Dividend Growth 5Y", "Значение": "Недоступно", "Оценка": "🔵 Нейтрально"})
        add("Quick Ratio", "quickRatio")
        add("Current Ratio", "currentRatio")
        add("Revenue (TTM)", "totalRevenue", 1e-6, " млн")
        data.append({"Показатель": "Revenue в кризисы", "Значение": "Недоступно", "Оценка": "🔵 Нейтрально"})
        add("Operating Margin %", "operatingMargins", percent=True)
        add("Net Margin %", "profitMargins", percent=True)
        add("Net Income", "netIncomeToCommon", 1e-6, " млн")
        add("Total Debt", "totalDebt", 1e-6, " млн")
        add("Total Assets", "totalAssets", 1e-6, " млн")
        add("Total Liabilities", "totalLiab", 1e-6, " млн")
        add("Stockholders' Equity", "totalStockholderEquity", 1e-6, " млн")
        add("EPS Estimate (Next Year)", "earningsGrowth")
        add("ROE (TTM)", "returnOnEquity", percent=True)
        data.append({"Показатель": "Buyback (5Y)", "Значение": "Недоступно", "Оценка": "🔵 Нейтрально"})
        data.append({"Показатель": "ROIC", "Значение": "Недоступно", "Оценка": "🔵 Нейтрально"})
        add("Operating CF", "operatingCashflow", 1e-6, " млн")
        add("Free CF", "freeCashflow", 1e-6, " млн")
        add("Short Float", "shortPercentOfFloat", percent=True)
        add("Institutional Ownership", "heldPercentInstitutions", percent=True)
        add("Employees", "fullTimeEmployees")
        data.append({"Показатель": "Retail Stores", "Значение": "Недоступно", "Оценка": "🔵 Нейтрально"})
        data.append({"Показатель": "OpenInsiders", "Значение": "Недоступно", "Оценка": "🔵 Нейтрально"})
        data.append({"Показатель": "Quant Rating", "Значение": "Недоступно", "Оценка": "🔵 Нейтрально"})

        return data
    except Exception as e:
        st.error(f"Ошибка при загрузке данных: {e}")
        return []


def get_stock_factors(ticker):
    stock = yf.Ticker(ticker)
    info = stock.info

    value = 5 - min((info.get("forwardPE") or 30) / 10, 5)
    growth = min((info.get("revenueGrowth") or 0.2) * 25, 5)
    profitability = min((info.get("profitMargins") or 0.2) * 25, 5)
    momentum = min((info.get("52WeekChange") or 0.2) * 25, 5)
    eps_revisions = min((info.get("earningsQuarterlyGrowth") or 0.2) * 25, 5)

    return value, growth, profitability, momentum, eps_revisions

def get_rating_label(quant_rating):
    if 4.5 <= quant_rating <= 5.0:
        return "Strong Buy", "darkgreen"
    elif 3.5 <= quant_rating < 4.5:
        return "Buy", "green"
    elif 2.5 <= quant_rating < 3.5:
        return "Hold", "orange"
    elif 1.5 <= quant_rating < 2.5:
        return "Sell", "red"
    else:
        return "Strong Sell", "darkred"

def calculate_quant_rating(ticker):
    try:
        value, growth, profitability, momentum, eps_revisions = get_stock_factors(ticker)
        quant_rating = round((value + growth + profitability + momentum + eps_revisions) / 5, 2)
        label, color = get_rating_label(quant_rating)
        return quant_rating, label, color
    except Exception as e:
        return 0, f"Ошибка: {e}", "black"

# Интерфейс
st.title("📊 Анализ акций и Quant Rating")

ticker = st.text_input("Введите тикер:", "").upper()

if st.button("Анализировать"):
    if ticker:
        with st.spinner("Загружаем данные..."):
            data = get_data(ticker)
            quant_value, quant_label, quant_color = calculate_quant_rating(ticker)

            if data:
                st.subheader("📄 Финансовые показатели")
                df = pd.DataFrame(data)
                st.dataframe(df, use_container_width=True)

                st.subheader("📈 Quant Rating")
                st.markdown(
                    f'<h4>Рейтинг: <span style="color:{quant_color}">{quant_label} ({quant_value:.2f})</span></h4>',
                    unsafe_allow_html=True
                )
    else:
        st.warning("Пожалуйста, введите тикер.")
