import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import pandas as pd
import yfinance as yf
from PIL import Image, ImageTk
import requests
from io import BytesIO
import streamlit as st

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
        messagebox.showerror("Ошибка", f"Не удалось получить данные для тикера {ticker}. Ошибка: {str(e)}")
        return None

# Функция для получения оценки на основе значения
def get_rating(value):
    try:
        if value == "Н/Д":
            return "🔵 Нейтрально"
        if isinstance(value, (int, float)):
            if value < 10:
                return "🟢 Хорошо"
            elif value < 20:
                return "🟡 Нейтрально"
            else:
                return "🔴 Плохо"
        return "🔵 Нейтрально"
    except:
        return "🔵 Нейтрально"

# Quant Rating функции
def get_stock_factors(ticker):
    stock = yf.Ticker(ticker)
    info = stock.info

    value = 5 - min((info.get("forwardPE") or 30) / 10, 5)
    growth = min((info.get("revenueGrowth") or 0.2) * 25, 5)
    profitability = min((info.get("profitMargins") or 0.2) * 25, 5)
    momentum = min((info.get("52WeekChange") or 0.2) * 25, 5)
    eps_revisions = min((info.get("earningsQuarterlyGrowth") or 0.2) * 25, 5)

    website = info.get("website", "")
    domain = website.replace("https://", "").replace("http://", "").split("/")[0] if website else ""
    logo_url = f"https://logo.clearbit.com/{domain}" if domain else ""

    return value, growth, profitability, momentum, eps_revisions, logo_url

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
        value, growth, profitability, momentum, eps_revisions, logo_url = get_stock_factors(ticker)

        quant_rating = round(
            (value + growth + profitability + momentum + eps_revisions) / 5, 2
        )
        label, color = get_rating_label(quant_rating)
        return quant_rating, label, color, logo_url
    except Exception as e:
        return 0, f"Ошибка: {e}", "black", ""

# UI-функции
def show_results(data, quant_rating_data):
    win = tk.Toplevel(root)
    win.title("Результаты анализа")
    win.geometry("950x650")

    tree = ttk.Treeview(win, columns=("Показатель", "Значение", "Оценка"), show="headings", selectmode="browse")
    tree.heading("Показатель", text="Показатель")
    tree.heading("Значение", text="Значение")
    tree.heading("Оценка", text="Оценка")
    tree.column("Показатель", width=300)
    tree.column("Значение", width=200)
    tree.column("Оценка", width=150)
    tree.pack(fill=tk.BOTH, expand=True)

    tree.tag_configure("good", background="lightgreen")
    tree.tag_configure("neutral_yellow", background="lightyellow")
    tree.tag_configure("neutral_blue", background="lightblue")
    tree.tag_configure("bad", background="lightcoral")

    def get_tag(grade):
        if "Плохо" in grade:
            return "bad"
        elif "Нейтрально" in grade:
            if grade.startswith("🟡"):
                return "neutral_yellow"
            elif grade.startswith("🔵"):
                return "neutral_blue"
            else:
                return "neutral_yellow"
        elif "Хорошо" in grade:
            return "good"
        else:
            return ""

    for item in data:
        tag = get_tag(item["Оценка"])
        tree.insert("", tk.END, values=(item["Показатель"], item["Значение"], item["Оценка"]), tags=(tag,))

    quant_label = ttk.Label(win, text=f"Quant Rating: {quant_rating_data[1]} ({quant_rating_data[0]:.2f})", font=("Helvetica", 14), foreground=quant_rating_data[2])
    quant_label.pack(pady=10)

    if quant_rating_data[3]:
        try:
            response = requests.get(quant_rating_data[3])
            img = Image.open(BytesIO(response.content)).resize((100, 100), Image.Resampling.LANCZOS)
            logo_img = ImageTk.PhotoImage(img)
            logo_label = ttk.Label(win, image=logo_img)
            logo_label.image = logo_img
            logo_label.pack(pady=5)
        except:
            pass

    def save_to_excel():
        df = pd.DataFrame(data)
        file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])
        if file_path:
            try:
                df.to_excel(file_path, index=False)
                messagebox.showinfo("Успех", f"Сохранено: {file_path}")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Ошибка при сохранении: {str(e)}")

    ttk.Button(win, text="Сохранить в Excel", command=save_to_excel).pack(pady=10)

# Основной интерфейс
root = tk.Tk()
root.title("Анализ акций и Quant Rating")

frame = ttk.Frame(root, padding=10)
frame.grid(row=0, column=0, padx=10, pady=10)

ttk.Label(frame, text="Введите тикер:").grid(row=0, column=0, sticky="w")
ticker_entry = ttk.Entry(frame, width=20)
ticker_entry.grid(row=0, column=1, padx=10)

def on_analyze_click():
    ticker = ticker_entry.get().strip().upper()
    if not ticker:
        messagebox.showwarning("Внимание", "Введите тикер!")
        return
    data = get_data(ticker)
    quant_data = calculate_quant_rating(ticker)
    if data:
        show_results(data, quant_data)

ttk.Button(frame, text="Анализировать", command=on_analyze_click).grid(row=1, column=0, columnspan=2, pady=10)

root.mainloop()
