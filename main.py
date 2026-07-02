"""
kabum7 メイン実行スクリプト

Step1〜4を順番に実行し、米国株7銘柄の値動き動画を自動生成する。

使い方:
    python main.py

保存先を変更したい場合は環境変数 KABUM7_BASE_DIR を設定してください。
    (Windows例) set KABUM7_BASE_DIR=C:\\Users\\YourName\\Documents\\kabum7\\output
"""
import time

import step1_fetch_stock_data
import step2_generate_audio
import step3_create_clips
import step4_concatenate


def main():
    steps = [
        ("Step1: 株価データ取得・PDF/JPG作成", step1_fetch_stock_data.run),
        ("Step2: コメント/音声作成", step2_generate_audio.run),
        ("Step3: JPG+音声からMP4クリップ作成", step3_create_clips.run),
        ("Step4: MP4クリップ連結", step4_concatenate.run),
    ]

    for label, func in steps:
        print(f"\n=== {label} ===")
        func()
        time.sleep(3)

    print("\n全ステップが完了しました。")


if __name__ == "__main__":
    main()
