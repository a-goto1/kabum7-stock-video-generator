"""
Step 2: 各銘柄の株価サマリーをコメント文にし、PDFと日本語音声(mp3)を作成する。
(旧 test2.py)
"""
import pytz
import yfinance as yf
from gtts import gTTS
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph, SimpleDocTemplate

from config import BASE_DIR, DATE_FORMAT, FONT_PATH, SYMBOLS, TIMEZONE
from utils import ensure_folder, get_last_trading_day, get_market_window


def fetch_stock_data(symbol, start_date, end_date, interval="1h"):
    stock = yf.Ticker(symbol)
    return stock.history(start=start_date, end=end_date, interval=interval)


def generate_comment(data, start_date, title):
    if data.empty:
        return "No data found for the selected date range."

    start_price = "${:.2f}".format(data["Close"].iloc[0])
    end_price = "${:.2f}".format(data["Close"].iloc[-1])

    comment = (
        f"【{title} {start_date.strftime('%m月%d日')}の株価】\n\n"
        f"始まり値段: {start_price}\n"
        f"終わり値段: {end_price}\n"
    )
    return comment


def write_to_pdf(comment, filename):
    doc = SimpleDocTemplate(str(filename), pagesize=letter)
    getSampleStyleSheet()  # スタイル初期化のため呼び出し（reportlab仕様）

    pdfmetrics.registerFont(TTFont("IPAG", FONT_PATH))
    style = ParagraphStyle(name="IPAG", fontName="IPAG", fontSize=12, leading=14)

    paragraphs = [Paragraph(comment.replace("\n", "<br />"), style)]
    doc.build(paragraphs)


def generate_audio(comment, audio_filename):
    tts = gTTS(comment, lang="ja")
    tts.save(str(audio_filename))


def run():
    jst = pytz.timezone(TIMEZONE)
    last_trading_day_jst = get_last_trading_day()
    start_jst, end_jst = get_market_window(last_trading_day_jst)
    start_utc = start_jst.astimezone(pytz.UTC)
    end_utc = end_jst.astimezone(pytz.UTC)

    folder_name = ensure_folder(BASE_DIR / last_trading_day_jst.strftime(DATE_FORMAT))

    for symbol, title in SYMBOLS.items():
        data = fetch_stock_data(symbol, start_utc, end_utc)
        comment = generate_comment(data, start_jst, title)

        pdf_filename = folder_name / f"{title} {start_jst.strftime(DATE_FORMAT)}_stock_prices.pdf"
        audio_filename = folder_name / f"{title} {start_jst.strftime(DATE_FORMAT)}.mp3"

        write_to_pdf(comment, pdf_filename)
        generate_audio(comment, audio_filename)

        print(f"PDF '{pdf_filename}' and audio file '{audio_filename}' created for {title}.")


if __name__ == "__main__":
    run()
