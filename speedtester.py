import os
import time
import speedtest
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
from dotenv import load_dotenv

# .env を読み込む
load_dotenv()

# 環境変数から SPREADSHEET_ID を取得
SPREADSHEET_ID = os.getenv("SPREADSHEET_ID")

# Google Sheets APIの認証設定
SCOPE = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]
CREDS = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", SCOPE)
client = gspread.authorize(CREDS)

# スプレッドシートを開く
sheet = client.open_by_key(SPREADSHEET_ID).worksheet("result")


def run_speed_test():
    """ネット速度を計測する関数"""
    try:
        st = speedtest.Speedtest(secure=True)
        st.get_best_server()

        download_speed = st.download() / 1_000_000  # Mbpsに変換
        upload_speed = st.upload() / 1_000_000  # Mbpsに変換
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        return [timestamp, round(download_speed, 2), round(upload_speed, 2)]

    except Exception as e:
        print(f"Speedtest error: {e}")
        return None


def log_speed_to_sheet():
    """計測データをスプレッドシートに記録する関数"""
    try:
        data = run_speed_test()
        if data:
            sheet.append_row(data)
            print(f"Logged: {data}")
        else:
            print("Speedtest failed, skipping this round.")

    except gspread.exceptions.APIError as e:
        print(f"Google Sheets API error: {e}")

    except Exception as e:
        print(f"Unexpected error: {e}")


if __name__ == "__main__":
    while True:
        log_speed_to_sheet()
        time.sleep(1800)  # 30分ごとに実行
