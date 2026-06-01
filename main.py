import os
from dotenv import load_dotenv
import gspread
from google.oauth2.service_account import Credentials
from gspread.client import Client
from gspread.spreadsheet import Spreadsheet
from gspread.worksheet import Worksheet
from gspread_dataframe import set_with_dataframe
from gspread_formatting import *
import pandas as pd

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

def get_spread(gs_credential:Client, spread_id:str)->Spreadsheet:
    spread = gs_credential.open_by_key(spread_id)
    return spread

def get_spread_sheet(spread:Spreadsheet, sheet_name:str) -> Worksheet:
    return spread.worksheet(sheet_name)

def read_spread(spread_sheet:Worksheet) -> pd.DataFrame:
    datas = spread_sheet.get_all_values()
    df = pd.DataFrame(datas[1:],columns=datas[0])
    df = df.astype({"社員ID":int, "年齢":int})
    return df

def get_department_average(df:pd.DataFrame)->pd.DataFrame:
    pvt_table = df.pivot_table(index=["所属"], values=["年齢"], aggfunc="mean")
    pvt_table["年齢"] = pvt_table["年齢"].round().astype(int)
    return pvt_table

def write_pivot_table(spread:Spreadsheet, piv_talbe:pd.DataFrame)-> Worksheet:
    new_spread_sheet = spread.add_worksheet(title="new", rows=100, cols=100)
    set_with_dataframe(worksheet=new_spread_sheet,dataframe=piv_talbe.reset_index(), row=1, col=1)
    return new_spread_sheet

def format_cells(new_sheet: Worksheet):
    head_format = CellFormat(
        backgroundColor=Color(38/255, 166/255, 154/255),
        textFormat=TextFormat(bold=True, foregroundColor=Color(255/255, 255/255, 255/255)),
        horizontalAlignment="CENTER"
    )
    format_cell_range(worksheet=new_sheet, name="A1:B1", cell_format=head_format)

    bk_border = Border(style="SOLID", color=Color(0,0,0,0))
    borders = Borders(top=bk_border, bottom=bk_border, left=bk_border, right=bk_border)
    ruled_line_format = CellFormat(
        borders=borders
    )
    format_cell_range(worksheet=new_sheet, name="A1:B7", cell_format=ruled_line_format)

def main():
    setting = init()
    gs_credential = get_auth(setting["credential_key"])
    spread = get_spread(gs_credential, setting["spread_id"])
    spread_sheet = get_spread_sheet(spread, setting["sheet_name"])
    df = read_spread(spread_sheet)
    piv_talbe = get_department_average(df)
    new_sheet = write_pivot_table(spread=spread, piv_talbe=piv_talbe)
    format_cells(new_sheet)

if __name__ == "__main__":
    main()
