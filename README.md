## 概要
　30分に一度speedtest-cli --secureを実行してGoogleSpreadSheetに結果を記録するスクリプト。
## セットアップ
### スクリプトの実行に必要なライブラリをインストールしたconda環境を作る
```
# 環境の作成
conda env create -f environment.yml
# 環境の立ち上げ
conda activate speedtest_env
```
### Google スプレッドシートの準備～その1～
- 新しいスプレッドシートを作成し、シート名(エクセルでいうとこの「ブック」)を result に変更。
- A1 に「Timestamp」、B1 に「Download (Mbps)」、C1 に「Upload (Mbps)」と入力。
### Google Cloud Console でプロジェクトを作成
- Google Sheets API を有効化。
- サービスアカウント を作成し、JSONキーをダウンロード。
- そのキーを credentials.json としてローカル(このディレクトリ)に保存。
### Google スプレッドシートの準備～その2～
- 上記で作ったサービスアカウントのメールアドレスを「編集者」としてシートを「共有する」にする。
- 追加するメールアドレスは、作成した credentials.json の client_email の中身の値。
### Pythonスクリプトを実行
```bash
python speedtester.py
```
### 結果
![スクリーンショット 2025-02-06 143658](https://github.com/user-attachments/assets/e791796e-479b-4366-837b-c07d36721694)
## トラブルシュート
　カスタマイズするときの参考に。
### ファイル名がspeedtest.pyだとライブラリと名前衝突する
```
@speedtest.py
speedtest.Speedtest(secure=True)
=>   File "C:\Users\og3\dev\speedtest\speedtest.py", line 24, in run_speed_test
    st = speedtest.Speedtest(secure=True)
         ^^^^^^^^^^^^^^^^^^^
AttributeError: module 'speedtest' has no attribute 'Speedtest'. Did you mean: 'speedtest'?
```
### speedtest.Speedtest(secure=True)じゃないと403エラーが返る
```
speedtest.Speedtest
=> ERROR: HTTP Error 403: Forbidden
speedtest.Speedtest(secure=True)
=> おｋ
```
## cronを使って1週間定点観測する
### 編集モードを開く
```bash
crontab -e
```
### ライフチェックと復活の設定
```bash
*/5 * * * * pgrep -f speedtester.py || nohup python3 /path/to/speedtester.py > /path/to/speedtester.log 2>&1 &
```
```
*/5 * * * * → 5分ごとに実行
pgrep -f speedtest.py → スクリプトが動いているかチェック
||（OR条件）→ 動いてなかったら実行
nohup python3 /path/to/speedtest.py & → バックグラウンドで実行
> /path/to/speedtest.log 2>&1 → ログを speedtest.log に保存（デバッグ用）
```
### 設定の確認
```bash
crontab -l
```
ここに登録されてたらおk
