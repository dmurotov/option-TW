import pandas as pd
import yfinance as yf
import requests
from io import BytesIO
from PIL import Image as PILImage
from IPython.display import display, clear_output
import ipywidgets as widgets
import plotly.graph_objects as go
import matplotlib.pyplot as plt

# Получение данных (заглушка)
def get_data(ticker):
    try:
        stock = yf.Ticker(ticker)
        _ = stock.info  # проверка существования тикера

        # Демоданные (можно заменить на реальный парсинг)
        data = [
            {"Показатель": "P/E (TTM)", "Значение": "53.67", "Оценка": "🔴 Плохо"},
            {"Показатель": "Forward P/E", "Значение": "17.89", "Оценка": "🟡 Нейтрально"},
            {"Показатель": "P/B", "Значение": "1.01", "Оценка": "🟢 Хорошо"},
            {"Показатель": "Quant Rating", "Значение": "Недоступно", "Оценка": "🔵 Нейтрально"},
        ]
        return data
    except Exception as e:
        print(f"Ошибка при получении данных: {str(e)}")
        return None

# Отображение таблицы
def display_data(data):
    df = pd.DataFrame(data)
    display(df)
    return df

# Обработчик при вводе тикера
def on_ticker_entered(change):
    clear_output(wait=True)
    display(ticker_input)

    ticker = change['new'].upper()
    data = get_data(ticker)

    if data:
        print(f"\n📊 Финансовые показатели для {ticker}:\n")
        df = display_data(data)

        # Преобразование числовых значений
        numeric_df = df.copy()
        numeric_df['Число'] = pd.to_numeric(
            numeric_df['Значение'].str.replace(r'[^\d\.\-]', '', regex=True),
            errors='coerce'
        )
        numeric_df = numeric_df.dropna(subset=['Число'])

        if not numeric_df.empty:
            fig = go.Figure(go.Bar(
                x=numeric_df['Показатель'],
                y=numeric_df['Число'],
                marker_color='teal'
            ))
            fig.update_layout(
                title=f"График числовых показателей для {ticker}",
                xaxis_title="Показатель",
                yaxis_title="Значение",
                height=500
            )
            fig.show()
        else:
            print("📉 Нет числовых данных для построения графика.")

        # Заглушка Quant Rating
        quant_rating_data = (4.2, "Buy", "green", f"https://logo.clearbit.com/{ticker.lower()}.com")
        print(f"\n📈 Quant Rating: {quant_rating_data[1]} ({quant_rating_data[0]:.2f})")

        # Попытка загрузить логотип
        try:
            response = requests.get(quant_rating_data[3], timeout=3)
            img = PILImage.open(BytesIO(response.content))
            plt.imshow(img)
            plt.axis('off')
            plt.show()
        except Exception as e:
            print("❗ Не удалось загрузить логотип:", str(e))
    else:
        print(f"❌ Не удалось получить данные для тикера {ticker}")

# Виджет ввода тикера
ticker_input = widgets.Text(
    value='AAPL',
    placeholder='Введите тикер',
    description='Тикер:',
    disabled=False
)
display(ticker_input)

# Привязка обработчика
ticker_input.observe(on_ticker_entered, names='value')
