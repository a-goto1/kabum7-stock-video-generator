"""
kabum7 共通ユーティリティ

test3.py / test4.py で重複していた「最新フォルダを探す」ロジックと、
営業日判定ロジックをここに集約します。
"""
from datetime import datetime, timedelta
from pathlib import Path

import holidays
import pytz

from config import DATE_FORMAT, MARKET_DURATION_HOURS, MARKET_START_HOUR, MARKET_START_MINUTE, TIMEZONE


def get_last_trading_day() -> datetime:
    """土日・米国祝日を除いた直近の営業日（JST基準）を返す。"""
    us_holidays = holidays.US()
    jst = pytz.timezone(TIMEZONE)
    now_jst = datetime.now(jst)

    if now_jst.hour < 6:
        target_date_jst = now_jst - timedelta(days=2)
    else:
        target_date_jst = now_jst - timedelta(days=1)

    while True:
        target_date_utc = target_date_jst.astimezone(pytz.UTC).date()
        if target_date_jst.weekday() >= 5 or target_date_utc in us_holidays:
            target_date_jst -= timedelta(days=1)
        else:
            break

    return target_date_jst


def get_market_window(last_trading_day_jst: datetime):
    """取引時間帯の開始・終了時刻（JST）を返す。"""
    start_jst = last_trading_day_jst.replace(
        hour=MARKET_START_HOUR, minute=MARKET_START_MINUTE, second=0, microsecond=0
    )
    end_jst = (start_jst + timedelta(hours=MARKET_DURATION_HOURS)).replace(
        hour=5, minute=0, second=0, microsecond=0
    )
    return start_jst, end_jst


def get_latest_dated_folder(base_directory: Path):
    """
    base_directory 直下にある "YYYY_MM_DD" 形式のフォルダのうち、
    最新の日付のものを返す。年をハードコードしないので毎年使い回せる。
    """
    base_directory = Path(base_directory)
    latest_date = None
    latest_dir = None

    if not base_directory.exists():
        return None

    for entry in base_directory.iterdir():
        if not entry.is_dir():
            continue
        try:
            date = datetime.strptime(entry.name, DATE_FORMAT)
        except ValueError:
            continue
        if latest_date is None or date > latest_date:
            latest_date = date
            latest_dir = entry

    return latest_dir


def ensure_folder(folder: Path) -> Path:
    folder = Path(folder)
    folder.mkdir(parents=True, exist_ok=True)
    return folder
