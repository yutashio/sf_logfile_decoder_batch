# Salesforce イベントログ Base64 デコードツール（一括処理版）

> [!NOTE]
> Event Log File の Base64 文字列を一括で CSV に変換するためのツールです。

**Salesforce の Event Log File** の `LogFile` 項目に格納された **Base64 文字列**をまとめてデコードし、人が読める文章＆CSV形式に変換するための Python スクリプトを作成してみました。  

## はじめに
Salesforce の Event Log File を Data Loader を使用して一括ダウンロードした際、`LogFile` 項目には **Base64 形式**でログデータが格納されています。  

しかし、この Base64 文字列のままでは中身を確認することができません。  
内容を確認するためには、 Base64 のデコードが必要です。  

そこで、EventLogFile の CSV ファイルをセットして Python スクリプトを実行するだけで、ログ内容をまとめて確認できる **一括デコードツール**を作成しました 🧑‍💻  

## 使い方
### 1. EventLogFile CSV を用意する
正しく動作するためには、CSV に以下の 3 項目が含まれている必要があります。  
| 項目名 | 用途 |  
|--------|------|  
| **Id** | 出力ファイル名に使用（識別子） |  
| **EventType** | 出力ファイル名に使用（ログ種別） |  
| **LogFile** | Base64 形式のログ本体（デコード対象） |  

Data Loader などで以下のように EventLogFile を取得します。  
取得した CSV ファイルをローカルに保存しておきます。  
```sql
SELECT Id, EventType, LogFile FROM EventLogFile
```
※その他の項目が含まれていても問題ありません。  

### 2. スクリプト実行
#### 基本コマンド  
ターミナルまたはコマンドプロンプトから下記を実行します：  
``` bash
python logfile_decode.py <取得したCSVファイルのパス>
```

例：
``` bash
python logfile_decode.py C:\Users\Hoge\Downloads\EventLogFile.csv
```

#### 出力先フォルダを指定する場合のコマンド  
ターミナルまたはコマンドプロンプトから下記を実行します：  
``` bash
python logfile_decode.py <取得したCSVファイルのパス> --outdir <出力先パス>
```

例：
``` bash
python logfile_decode.py C:\Users\Hoge\Downloads\EventLogFile.csv --outdir C:\Users\Hoge\Downloads\decoded
```
> [!TIP]
>出力先フォルダを指定しない場合、本スクリプトが置かれているフォルダ直下に出力されます。

### 3.出力結果
#### 成功時
- 実行時に result_YYYYMMDDHHMMSS フォルダが自動生成されます。  
- 各レコードごとに [EventType]_[Id].csv 形式で出力します。  
  - 例：
    - Login_0ATXXXXXXXXXXXX.csv
    - API_0ATXXXXXXXXXXXX.csv

#### 出力例：
```
---------------------------------------------------------------------
[INFO] 出力先フォルダ: C:\Users\Hoge\Downloads\result_20251031104512
---------------------------------------------------------------------
C:\Users\Hoge\Downloads\result_20251031104512\Login_0ATXXXXXXXXXXXX.csv
[SUCCESS] 出力完了: Login_0ATXXXXXXXXXXXX.csv
C:\Users\Hoge\Downloads\result_20251031104512\API_0ATXXXXXXXXXXXX.csv
[SUCCESS] 出力完了: API_0ATXXXXXXXXXXXX.csv
```

#### エラー発生時
Base64 が不正な場合やファイルが見つからない場合はエラーメッセージを表示して処理を終了します。  