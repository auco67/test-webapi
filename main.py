import os
from dotenv import load_dotenv

# .envファイルの内容を環境変数に読み込む
load_dotenv()

# os.getenv() を使って値を取得する
credential_key = os.getenv("CREDENTIAL_PATH")

def main():
    print(credential_key)

if __name__ == "__main__":
    main()
