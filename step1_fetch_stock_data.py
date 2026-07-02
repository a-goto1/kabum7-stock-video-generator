"""
Step 1: 各銘柄の株価データを取得し、PDF（一覧）とJPG（グラフ）を作成する。
(旧 test1.py)
"""
from datetime import timedelta

import matplotlib.font_manager as fm
import matplotlib.pyplot as plt
import pytz
import yfinance as yf
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

from config import BASE_DIR, DATE_FORMAT, FONT_PATH, SYMBOLS, TIMEZONE
from utils import ensure_folder, get_last_trading_day, get_market_window


def fetch_stock_data(symbol, start_date, end_date, interval="1h"):
    stock = yf.Ticker(symbol)
    return stock.history(start=start_date, end=end_date, interval=interval)


def fetch_previous_day_close(symbol, date, interval="1d"):
    stock = yf.Ticker(symbol)
    previous_day = date - timedelta(days=1)
    data = stock.history(start=previous_day, end=date, interval=interval)
    if not data.empty:
        return data["Close"].iloc[-1]
    return "N/A"


def write_to_pdf(data, filename, start_date, end_date, previous_close, title):
    try:
        c = canvas.Canvas(str(filename), pagesize=letter)
        width, height = letter
        pdfmetrics.registerFont(TTFont("IPAG", FONT_PATH))
        c.setFont("IPAG", 12)

        jst = pytz.timezone(TIMEZONE)
        start_date_jst = start_date.astimezone(jst)
        end_date_jst = end_date.astimezone(jst)
        c.drawString(
            100,
            height - 50,
            f"{title} 株価 {start_date_jst.strftime('%Y年%m月%d日 %H時%M分%S秒 %Z')} "
            f"から {end_date_jst.strftime('%Y年%m月%d日 %H時%M分%S秒 %Z')} JSTまで",
        )

        start_price = data["Close"].iloc[0] if not data.empty else "N/A"
        end_price = data["Close"].iloc[-1] if not data.empty else "N/A"
        c.drawString(
            100, height - 70,
            f"始値: {start_price:.2f}ドル" if isinstance(start_price, (float, int)) else f"始値: {start_price}",
        )
        c.drawString(
            100, height - 90,
            f"終値: {end_price:.2f}ドル" if isinstance(end_price, (float, int)) else f"終値: {end_price}",
        )

        if isinstance(previous_close, (float, int)):
            c.drawString(100, height - 110, f"前日終値: {previous_close:.2f}ドル")
        else:
            c.drawString(100, height - 110, f"前日終値: {previous_close}")

        y_position = height - 130
        for index, row in data.iterrows():
            jst_time = index.tz_convert(jst)
            date_str = jst_time.strftime("%Y年%m月%d日 %H時%M分%S秒")
            price = row["Close"]
            c.drawString(
                100, y_position,
                f"{date_str}: {price:.2f}ドル" if isinstance(price, (float, int)) else f"{date_str}: {price}",
            )
            y_position -= 20
            if y_position < 50:
                c.showPage()
                c.setFont("IPAG", 12)
                y_position = height - 50

        c.save()
        print(f"PDF '{filename}' が正常に作成されました。")
    except Exception as e:
        print(f"PDF作成中にエラーが発生しました: {e}")


def create_jpg(data, filename, previous_close, title):
    try:
        jst = pytz.timezone(TIMEZONE)
        data = data.copy()
        data.index = data.index.tz_convert(jst)
        font_prop = fm.FontProperties(fname=FONT_PATH, size=38)
        plt.rcParams["font.size"] = 14

        fig, ax = plt.subplots(figsize=(9, 16))
        ax.plot(data.index, data["Close"], label="終値", color="blue", marker="o")
        ax.set_title(f"{title} 株価 (日本時間)", fontsize=14, fontproperties=font_prop)
        ax.set_xlabel("時間", fontsize=14, fontproperties=font_prop)
        ax.set_ylabel("価格 (USD)", fontsize=14, fontproperties=font_prop)
        ax.legend()

        if not data.empty:
            start_price = data["Close"].iloc[0]
            end_price = data["Close"].iloc[-1]
            max_price = data["Close"].max()
            min_price = data["Close"].min()
            ax.text(0.02, 0.95, f"始値: {start_price:.2f} USD", transform=ax.transAxes,
                     fontsize=36, fontproperties=font_prop, color="green", verticalalignment="top")
            ax.text(0.02, 0.90, f"終値: {end_price:.2f} USD", transform=ax.transAxes,
                     fontsize=36, fontproperties=font_prop, color="red", verticalalignment="top")
            ax.text(0.02, 0.85, f"最高値: {max_price:.2f} USD", transform=ax.transAxes,
                     fontsize=28, fontproperties=font_prop, color="blue", verticalalignment="top")
            ax.text(0.02, 0.80, f"最安値: {min_price:.2f} USD", transform=ax.transAxes,
                     fontsize=28, fontproperties=font_prop, color="purple", verticalalignment="top")

            if isinstance(previous_close, (float, int)):
                ax.text(0.02, 0.75, f"前日終値: {previous_close:.2f} USD", transform=ax.transAxes,
                         fontsize=20, fontproperties=font_prop, color="orange", verticalalignment="top")

        plt.subplots_adjust(left=0.2, bottom=0.2)
        plt.savefig(filename, format="jpg")
        plt.close()
        print(f"JPG '{filename}' が正常に作成されました。")
    except Exception as e:
        print(f"JPG作成中にエラーが発生しました: {e}")


def run():
    jst = pytz.timezone(TIMEZONE)
    last_trading_day_jst = get_last_trading_day()
    start_date, end_date = get_market_window(last_trading_day_jst)
    previous_close_date = start_date - timedelta(days=1)

    folder_name = ensure_folder(BASE_DIR / start_date.astimezone(jst).strftime(DATE_FORMAT))

    for symbol, title in SYMBOLS.items():
        previous_close = fetch_previous_day_close(symbol, previous_close_date)
        data = fetch_stock_data(symbol, start_date, end_date)

        pdf_filename = folder_name / f"{title} {start_date.strftime('%m月%d日')}.pdf"
        jpg_filename = folder_name / f"{title} {start_date.strftime(DATE_FORMAT)}.jpg"

        write_to_pdf(data, pdf_filename, start_date, end_date, previous_close, title)
        create_jpg(data, jpg_filename, previous_close, title)


if __name__ == "__main__":
    run()
