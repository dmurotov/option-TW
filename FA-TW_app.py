import streamlit as st
import pandas as pd
import yfinance as yf
import requests
from PIL import Image
from io import BytesIO

# Функция для получения данных для произвольного тикера
def get_data(ticker):
    try:
        stock = yf.Ticker(ticker)
        stock_info = stock.info

        # Если не удалось получить данные
        if not stock_info:
            raise ValueError("Не удалось получить данные по тикеру")

        # Пример показателей, которые можно выводить
        data = [
            {"Показатель": "P/E (TTM)", "Значение": "53.67", "Оценка": "🔴 Плохо"},
            {"Показатель": "Forward P/E", "Значение": "17.89", "Оценка": "🟡 Нейтрально"},
            {"Показатель": "P/B", "Значение": "1.01", "Оценка": "🟢 Хорошо"},
            {"Показатель": "P/S", "Значение": "0.32", "Оценка": "🟢 Хорошо"},
            {"Показатель": "P/FCF", "Значение": "Н/Д (отриц. FCF)", "Оценка": "🔴 Плохо"},
            {"Показатель": "D/E", "Значение": "0.54", "Оценка": "🟡 Нейтрально"},
            {"Показатель": "PEG Ratio", "Значение": "Н/Д", "Оценка": "🔴 Плохо"},
            {"Показатель": "Enterprise Value", "Значение": "~115 млн", "Оценка": "🟢 Хорошо"},
            {"Показатель": "Peter Lynch Price (PLP)", "Значение": "Недоступен", "Оценка": "🔵 Нейтрально"},
            {"Показатель": "Piotroski F-Score", "Значение": "4 из 9", "Оценка": "🟡 Нейтрально"},
            {"Показатель": "Altman Z-Score", "Значение": "-0.75", "Оценка": "🔴 Плохо"},
            {"Показатель": "Beneish M-Score", "Значение": "-1.95", "Оценка": "🔴 Плохо"},
            {"Показатель": "Dividend Yield (%)", "Значение": "1.75%", "Оценка": "🔴 Плохо"},
            {"Показатель": "Payout Ratio", "Значение": "71.43%", "Оценка": "🔴 Плохо"},
            {"Показатель": "Dividend Growth 5Y", "Значение": "0%", "Оценка": "🔴 Плохо"},
            {"Показатель": "Quick Ratio", "Значение": "0.47", "Оценка": "🔴 Плохо"},
            {"Показатель": "Current Ratio", "Значение": "0.47", "Оценка": "🔴 Плохо"},
            {"Показатель": "Revenue (TTM)", "Значение": "$137.3 млн", "Оценка": "🔴 Плохо"},
            {"Показатель": "Revenue в кризисы", "Значение": "Падение (например, 2020: $145 млн)", "Оценка": "🔴 Плохо"},
            {"Показатель": "Operating Margin %", "Значение": "-2.52%", "Оценка": "🔴 Плохо"},
            {"Показатель": "Net Margin %", "Значение": "-1.84%", "Оценка": "🔴 Плохо"},
            {"Показатель": "Net Income", "Значение": "Убыток: -$2.53 млн", "Оценка": "🔴 Плохо"},
            {"Показатель": "Total Debt", "Значение": "~25.6 млн", "Оценка": "🟡 Нейтрально"},
            {"Показатель": "Total Assets", "Значение": "$245 млн", "Оценка": "🔴 Плохо"},
            {"Показатель": "Total Liabilities", "Значение": "$194 млн", "Оценка": "🔴 Плохо"},
            {"Показатель": "Stockholders' Equity", "Значение": "$50.3 млн", "Оценка": "🔴 Плохо"},
            {"Показатель": "EPS Estimate (Next Year)", "Значение": "$0.20", "Оценка": "🟢 Хорошо"},
            {"Показатель": "ROE (TTM)", "Значение": "-4.87%", "Оценка": "🔴 Плохо"},
            {"Показатель": "Buyback (5Y)", "Значение": "Нет", "Оценка": "🔵 Нейтрально"},
            {"Показатель": "ROIC", "Значение": "-2.12%", "Оценка": "🔴 Плохо"},
            {"Показатель": "Operating CF", "Значение": "-$4.8 млн", "Оценка": "🔴 Плохо"},
            {"Показатель": "Free CF", "Значение": "-$6.7 млн", "Оценка": "🔴 Плохо"},
            {"Показатель": "Short Float", "Значение": "0.33%", "Оценка": "🟢 Хорошо"},
            {"Показатель": "Institutional Ownership", "Значение": "38%", "Оценка": "🟢 Хорошо"},
            {"Показатель": "Employees", "Значение": "92", "Оценка": "🔴 Плохо"},
            {"Показатель": "Retail Stores", "Значение": "Нет", "Оценка": "🔵 Нейтрально"},
            {"Показатель": "OpenInsiders", "Значение": "Покупка (последняя в марте)", "Оценка": "🟢 Хорошо"},
            {"Показатель": "Quant Rating", "Значение": "Недоступно", "Оценка": "🔵 Нейтрально"}
    ]
        return data
    except Exception as e:
        st.error(f"Не удалось получить данные для тикера {ticker}. Ошибка: {str(e)}")
        return None

# Функции для расчёта Quant Rating
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

        quant_rating = round(
            (value + growth + profitability + momentum + eps_revisions) / 5, 2
        )
        label, color = get_rating_label(quant_rating)
        return quant_rating, label, color
    except Exception as e:
        return 0, f"Ошибка: {e}", "black"

# Streamlit интерфейс
st.title("Анализ акций и Quant Rating")

ticker = st.text_input("Введите тикер:", "")

if st.button("Анализировать"):
    if ticker:
        data = get_data(ticker)
        quant_data = calculate_quant_rating(ticker)
        
        if data:
            # Отображаем данные
            df = pd.DataFrame(data)
            st.write(df)

            # Отображаем Quant Rating
            quant_label, quant_color = quant_data[1], quant_data[2]
            st.markdown(f"**Quant Rating: {quant_label} ({quant_data[0]:.2f})**", unsafe_allow_html=True)
            st.markdown(f'<span style="color:{quant_color}">{quant_label}</span>', unsafe_allow_html=True)
    else:
        st.warning("Пожалуйста, введите тикер.")
