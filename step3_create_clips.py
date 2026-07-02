"""
Step 3: 最新フォルダ内のJPG(グラフ画像)とMP3(音声)を組み合わせてMP4クリップを作成する。
(旧 test3.py)
"""
import subprocess
from pathlib import Path

from config import BASE_DIR
from utils import get_latest_dated_folder


def create_mp4_from_images_and_audios(directory: Path):
    if not directory:
        print("最新のディレクトリが見つかりませんでした。")
        return

    directory = Path(directory)
    for image_path in directory.glob("*.jpg"):
        audio_path = image_path.with_suffix(".mp3")
        output_video_path = image_path.with_suffix(".mp4")

        if not audio_path.exists():
            print(f"音声ファイルが見つかりませんでした: {audio_path} - 無視します")
            continue

        cmd = [
            "ffmpeg",
            "-loop", "1",
            "-i", str(image_path),
            "-i", str(audio_path),
            "-c:v", "libx264",
            "-c:a", "aac",
            "-b:a", "192k",
            "-pix_fmt", "yuv420p",
            "-shortest",
            "-y",
            str(output_video_path),
        ]

        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
            print(result.stdout)
            print(result.stderr)
            result.check_returncode()
            print(f"MP4動画 '{output_video_path}' が作成されました。")
        except subprocess.CalledProcessError as e:
            print(f"エラーが発生しました: {e}")
            print(f"標準出力: {e.stdout}")
            print(f"標準エラー: {e.stderr}")


def run():
    latest_directory = get_latest_dated_folder(BASE_DIR)
    create_mp4_from_images_and_audios(latest_directory)


if __name__ == "__main__":
    run()
