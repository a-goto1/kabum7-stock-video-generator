"""
kabum7 共通設定ファイル

環境依存の値（保存先フォルダなど）はここか環境変数でまとめて管理します。
個人PCの絶対パスをコードに直書きしないためのモジュールです。
"""
import os
from pathlib import Path

# ---------------------------------------------------------------------------
# 保存先フォルダ
# ---------------------------------------------------------------------------
# 環境変数 KABUM7_BASE_DIR が設定されていればそれを使用し、
# なければこのファイルと同じ場所に output フォルダを作成します。
# Windowsで使う場合は例えば以下のように設定してください:
#   set KABUM7_BASE_DIR=C:\Users\YourName\Documents\kabum7\output
BASE_DIR = Path(os.environ.get("KABUM7_BASE_DIR", Path(__file__).parent / "output"))
BASE_DIR.mkdir(parents=True, exist_ok=True)

# フォントファイル（日本語表示用）
FONT_PATH = str(Path(__file__).parent / "assets" / "ipag.ttf")

# ---------------------------------------------------------------------------
# 対象銘柄
# ---------------------------------------------------------------------------
SYMBOLS = {
    "NVDA": "NVIDIA",
    "AAPL": "Apple",
    "TSLA": "Tesla",
    "MSFT": "Microsoft",
    "AMZN": "Amazon",
    "META": "Meta",
    "GOOGL": "Alphabet",
}

# 動画連結時の並び順（数字が小さいほど先頭）
CUSTOM_ORDER = {
    "NVIDIA": 1,
    "Apple": 2,
    "Tesla": 3,
    "Microsoft": 4,
    "Amazon": 5,
    "Meta": 6,
    "Alphabet": 7,
}

# ---------------------------------------------------------------------------
# 取引時間帯（米国市場のプレ〜通常取引をJSTで表現）
# ---------------------------------------------------------------------------
TIMEZONE = "Asia/Tokyo"
MARKET_START_HOUR = 22
MARKET_START_MINUTE = 30
MARKET_DURATION_HOURS = 6.5

# フォルダ名の日付フォーマット（YYYY_MM_DD）
DATE_FORMAT = "%Y_%m_%d"
