# kst-txg

**K**eio **S**cience and **T**echnology—**t**rip E**x**cel **g**enerator です。Microsoft Excel ファイルを展開した XML ファイルを Python スクリプトによって編集し、学外研究や学会活動などの出張に必要な書類を出力します。

## 【重要】出力ファイル「○○.xlsx」を開いたときのエラーについて

出力ファイル「○○.xlsx」を開くと、以下のようなエラーメッセージが表示されます：

> '○○.xlsx' の一部の内容に問題が見つかりました。可能な限り内容を回復しますか？ ブックの発行元が信頼できる場合は、\[はい\] をクリックしてください。

これは、Excel 内部で自動生成されるフリガナに起因することを確認しています。**このフリガナはシートの見た目・セルの内容には影響しない**ので、\[はい\] をクリックして問題を修復してください。その上で、修復後のファイルを保存してください。

詳しくは以下のリンクを参照してください。
- [PhoneticProperties クラス](https://learn.microsoft.com/ja-jp/dotnet/api/documentformat.openxml.spreadsheet.phoneticproperties?view=openxml-2.8.1)
- [Excelの破損【/xl/sharedStrings.xml パーツ内の文字列プロパティ (文字列)】について](https://answers.microsoft.com/ja-jp/msoffice/forum/all/excel%E3%81%AE%E7%A0%B4%E6%90%8Dxlsharedstringsxml/af4b9ebc-18e7-4df1-b02d-9364a9a4bc61)

## 要件

- Python3

## 使い方

1. prof.py, student.py, trips.py, gen.py を編集
2. コマンドラインから `python3 -m gen` を実行
3. 出力ファイル「○○.xlsx」を開く
4. エラーメッセージが表示されたら問題を修復し、修復後のファイルを保存する

なお、「立替払い精算」の書類では、資金名が「5. その他」に記入されます。資金が「1. 教育研究費」「2. 指定寄付」「3. 受託研究」「4. 預り金」のいずれかの場合は、出力ファイルを直接編集してください。

## 書類一覧

次の書類が一つのファイルにまとまって出力されます。

1. 学外研究・学会活動届
2. 様式32_出張旅費申請書
3. 様式33_出張依頼書
4. 立替払い精算
5. 様式51_立替金請求書

## ライセンス

- MIT License ([LICENSE](https://github.com/ty-foobar/kst-txg/blob/main/LICENSE) を参照)
