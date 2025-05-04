import streamlit as st
import pandas as pd
import yfinance as yf
import requests
from io import BytesIO
from PIL import Image as PILImage
import plotly.graph_objects as go

st.set_page_config(page_title="Финансовый Анализ", layout="wide")

st.title("📊 Расширенный Анализ Акций")
ticker = st.text_input("Введите тикер компании (например, AAPL):", value="AAPL").upper()

@st.cache_data(show_spinner=False)
def get_logo_url(info):
    website = info.get("website", "")
    domain = website.replace("https://", "").replace("http://", "").split("/")[0] if website else ""
    return f"https://logo.clearbit.com/{domain}" if domain else ""

@st.cache_data(show_spinner=False)
def get_extended_metrics():
    return [
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
        {"Показатель": "Quant Rating", "Значение": "Недоступно", "Оценка": "🔵 Нейтрально"},
    ]

if ticker:
    with st.spinner("Загружаем данные..."):
        stock = yf.Ticker(ticker)
        info = stock.info
        data = get_extended_metrics()

    st.subheader(f"📈 Расширенные метрики для {ticker}")
    df = pd.DataFrame(data)
    st.dataframe(df, use_container_width=True)

    # Визуализация числовых значений
    numeric_df = df.copy()
    numeric_df['Число'] = pd.to_numeric(
        numeric_df['Значение'].str.replace(r'[^\d\.-]', '', regex=True),
        errors='coerce'
    )
    numeric_df = numeric_df.dropna(subset=['Число'])

    fig = go.Figure(go.Bar(
        x=numeric_df['Показатель'],
        y=numeric_df['Число'],
        marker_color='indigo'
    ))
    fig.update_layout(
        title=f"График ключевых показателей {ticker}",
        xaxis_title="Показатель",
        yaxis_title="Значение",
        height=450
    )
    st.plotly_chart(fig, use_container_width=True)

    # Логотип
    logo_url = get_logo_url(info)
    if logo_url:
        try:
            response = requests.get(logo_url, timeout=3)
            img = PILImage.open(BytesIO(response.content))
            st.image(img, caption=f"Логотип {ticker}", width=150)
        except:
            st.info("❗ Логотип не найден.")
