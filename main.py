import os
from dotenv import load_dotenv
import gspread
from google.oauth2.service_account import Credentials
from gspread.client import Client

def init():
    # .envファイルの内容を環境変数に読み込む
    load_dotenv()

    # os.getenv() を使って値を取得する
    credential_key = os.getenv("CREDENTIAL_PATH")
    spread_id = os.getenv("SPREAD_ID")
    sheet_name = os.getenv("SHEET_NAME")

    setting = {
        "credential_key":credential_key,
        "spread_id":spread_id, 
        "sheet_name": sheet_name
    }
    return setting

def get_auth(credential_key:str) -> Client:
    scopes = [
        'https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive'
    ]

    credentials = Credentials.from_service_account_file(credential_key,scopes=scopes)

    gc = gspread.authorize(credentials)

    return gc

def read_spread(gs_credential:Client, spread_id:str, sheet_name:str):
    spread = gs_credential.open_by_key(spread_id)
    spread_sheet = spread.worksheet(sheet_name)
    print(spread_sheet.get_values())

def main():
    setting = init()
    gs_credential = get_auth(setting["credential_key"])
    read_spread(gs_credential, setting["spread_id"], setting["sheet_name"])

if __name__ == "__main__":
    main()
