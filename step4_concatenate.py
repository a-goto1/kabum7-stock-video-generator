"""
Step 4: 各銘柄のMP4クリップを指定順（NVIDIA→Apple→...）で連結し、1本の動画にする。
(旧 test4.py)

【修正点】
旧コードは `folders = [f for f in folders if f.startswith('2024_')]` と
年をハードコードしていたため、2024年以外のフォルダが見つからず動作しなくなる
バグがありました。utils.get_latest_dated_folder() で日付形式そのものを
判定する方式に変更し、年に依存しないようにしています。
"""
import subprocess
from pathlib import Path

from config import BASE_DIR, CUSTOM_ORDER
from utils import get_latest_dated_folder


def extract_order(filename: str) -> int:
    for key, order in CUSTOM_ORDER.items():
        if key in filename:
            return order
    return float("inf")  # 定義されていないファイルは最下位にする


def create_file_list(directory: Path, output_file_list_path: Path) -> bool:
    files = sorted(
        (f.name for f in directory.glob("*.mp4") if f.name != "output.mp4"),
        key=extract_order,
    )

    if not files:
        print("動画ファイルが見つかりませんでした。")
        return False

    with open(output_file_list_path, "w", encoding="utf-8") as file_list:
        for filename in files:
            file_path = (directory / filename).as_posix()
            file_list.write(f"file '{file_path}'\n")

    return True


def concatenate_videos(directory: Path, output_video_path: Path):
    file_list_path = directory / "file_list.txt"

    if not create_file_list(directory, file_list_path):
        print("ファイルリストの作成に失敗しました。")
        return

    cmd = [
        "ffmpeg",
        "-f", "concat",
        "-safe", "0",
        "-i", str(file_list_path),
        "-c:v", "copy",
        "-c:a", "aac",
        "-b:a", "192k",
        "-y",
        str(output_video_path),
    ]

    try:
        subprocess.run(cmd, check=True)
        print(f"連結動画 '{output_video_path}' が作成されました。")
    except subprocess.CalledProcessError as e:
        print(f"エラーが発生しました: {e}")


def run():
    latest_folder = get_latest_dated_folder(BASE_DIR)
    if latest_folder:
        output_video_path = latest_folder / "output.mp4"
        concatenate_videos(latest_folder, output_video_path)
    else:
        print("最新のフォルダーが見つかりませんでした。")


if __name__ == "__main__":
    run()
