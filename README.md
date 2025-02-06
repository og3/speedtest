## 概要
- 30分に一度speedtest-cli --secureを実行してGoogleSpreadSheetに結果を記録するスクリプト

## セットアップ
### スクリプトの実行に必要なライブラリをインストールしたconda環境を作る

### Google スプレッドシートの準備
- 新しいスプレッドシートを作成し、シート名(エクセルでいうとこの「ブック」)を SpeedTest に変更。
- A1 に「Timestamp」、B1 に「Download (Mbps)」、C1 に「Upload (Mbps)」と入力。
### Google Cloud Console でプロジェクトを作成。
- Google Sheets API を有効化。
- サービスアカウント を作成し、JSONキーをダウンロード。
- そのキーを credentials.json としてローカル(このディレクトリ)に保存。
### Pythonスクリプトを実行
```bash
python speedtester.py
```
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
