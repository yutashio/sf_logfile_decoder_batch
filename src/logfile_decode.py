import os
import csv
import base64
import sys
import datetime
import argparse


ap = argparse.ArgumentParser(description="Salesforce EventLogFile の LogFile(Base64) を一括デコードしてCSV出力するツール")
ap.add_argument("input", help="EventLogFile CSVファイルへのパス")
ap.add_argument("--outdir", help="出力先パス（省略時は実行ディレクトリ直下に出力）")
args = ap.parse_args()

# EventLogFile CSVファイルのチェック
input_csv = args.input
if not os.path.isfile(input_csv):
    print(f"[ERROR] 指定されたファイルが見つかりません: {input_csv}")
    sys.exit(1)
if not input_csv.lower().endswith(".csv"):
    print(f"[ERROR] 指定されたファイルはCSVではありません: {input_csv}")
    sys.exit(1)

# 出力先フォルダの決定と作成
timestamp  = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
if args.outdir is None:
    # 出力先フォルダの指定なし（Pythonスクリプト直下に出力）
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(script_dir, f"result_{timestamp}")
else:
    # 出力先フォルダの指定あり（指定された場所の配下に出力）
    output_dir = os.path.join(args.outdir, f"result_{timestamp}")
    if not os.path.isdir(args.outdir):
        print(f"[ERROR] 指定された出力先ファルダが見つかりません: {args.outdir}")
        sys.exit(1)

# フォルダを作成
os.makedirs(output_dir, exist_ok=True)
print("---------------------------------------------------------------------")
print(f"[INFO] 出力先フォルダ: {output_dir}")
print("---------------------------------------------------------------------")

# CSV読み込み & Base64デコード
try:
    with open(input_csv, encoding="UTF-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            b64 = row["LogFile"].strip()
            event_type = row["EventType"].strip()
            record_id  = row["Id"].strip()

            if not b64:
                print(f"[WARN] LogFile が空のためスキップ: EventType={event_type}, Id={record_id}")
                continue

            try:
                decoded = base64.b64decode(b64).decode("utf-8")
            except Exception as e:
                print(f"[ERROR] Base64デコードに失敗しました: EventType={event_type}, Id={record_id}")
                print(f"       詳細: {e}")
                continue

            filename = f"{event_type}_{record_id}.csv"
            filepath = os.path.join(output_dir, filename)
            print(filepath)
            with open(filepath, "w", encoding="utf-8", newline="") as out:
                out.write(decoded)
            print(f"[SUCCESS] 出力完了: {filename}")
except Exception as e :
    print(f"[ERROR] 処理中に予期せぬエラーが発生しました:{e}")
    sys.exit(1)