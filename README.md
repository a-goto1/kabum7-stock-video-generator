# kabum7 — 米国株7銘柄 自動株価動画生成ツール

米国主要テック株7銘柄（NVIDIA, Apple, Tesla, Microsoft, Amazon, Meta, Alphabet）の
値動きを毎営業日自動で取得し、グラフ画像・PDFレポート・日本語音声コメント付きの
動画（MP4）を自動生成するPythonツールです。

## できること

1. **株価取得**（Step1）: yfinanceで米国市場の取引時間帯（プレ〜通常取引、日本時間換算）の株価を取得し、PDFレポートとグラフJPGを作成
2. **コメント音声生成**（Step2）: 始値・終値のサマリーを日本語コメントにし、PDFと音声(mp3)を作成（gTTS使用）
3. **クリップ動画作成**（Step3）: グラフ画像＋音声をffmpegで合成し、銘柄ごとにMP4クリップを作成
4. **動画連結**（Step4）: 全銘柄のクリップを指定順に連結し、1本のMP4にまとめる

すべて `main.py` から一括実行できます。

## 技術要素

- **データ取得**: yfinance（Yahoo Finance API）
- **PDF生成**: reportlab（日本語フォント埋め込み対応）
- **グラフ描画**: matplotlib
- **音声合成**: gTTS（Google Text-to-Speech）
- **動画処理**: ffmpeg（subprocess経由）
- **日時処理**: pytz, holidays（米国祝日を考慮した営業日判定）

## セットアップ

```bash
pip install -r requirements.txt
```

ffmpegがインストールされていない場合は別途インストールしてください。

- Windows: https://ffmpeg.org/download.html からダウンロードしPATHを通す
- Mac: `brew install ffmpeg`

## 使い方

```bash
python main.py
```

保存先フォルダはデフォルトで `./output` ですが、環境変数で変更できます。

```bash
# Windowsの例
set KABUM7_BASE_DIR=C:\Users\YourName\Documents\kabum7\output
python main.py
```

Windowsでダブルクリック実行したい場合は `run_kabum7.bat` を使用してください。

## フォルダ構成

```
kabum7/
├── main.py                     # 一括実行スクリプト
├── config.py                   # 銘柄・パス・時間帯などの共通設定
├── utils.py                    # 営業日判定・最新フォルダ探索などの共通処理
├── step1_fetch_stock_data.py   # 株価取得 → PDF/JPG作成
├── step2_generate_audio.py     # コメント・音声作成
├── step3_create_clips.py       # JPG+音声 → MP4クリップ作成
├── step4_concatenate.py        # MP4クリップ連結
├── assets/
│   └── ipag.ttf                # 日本語表示用フォント（各自で配置）
├── requirements.txt
└── run_kabum7.bat
```

実行すると `output/YYYY_MM_DD/` フォルダに、銘柄ごとのPDF・JPG・MP3・MP4と、
連結済みの `output.mp4` が生成されます。

## 元コードからの主な改善点

- 個人PCの絶対パスのハードコードを廃止し、環境変数で保存先を指定できるように変更
- `2024_` と年を固定でフィルタしていたバグを修正し、年をまたいでも動作するように変更（`utils.get_latest_dated_folder`）
- Step3/Step4で重複していた「最新フォルダ探索」ロジックを `utils.py` に共通化
- 銘柄リスト・取引時間帯などの設定値を `config.py` に一元化
- 4本の独立したスクリプトを `main.py` から一括実行できるように整理

## 今後の拡張案

- 対象銘柄・時間帯を実行時引数で切り替えられるようにする
- ログをファイル出力し、失敗銘柄だけリトライできるようにする
- クラウド（GitHub Actions等）でのスケジュール実行に対応する

## 注意事項

本ツールは学習・ポートフォリオ用途の自動動画生成ツールです。  
投資判断や売買助言を目的としたものではありません。

日本語表示にはフォントファイルが必要です。  
`assets/ipag.ttf` を各自で配置してください。  
フォントファイル本体はこのリポジトリには含めていません。
