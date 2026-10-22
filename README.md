# workbook

Azure ブック（Azure Workbooks）のテンプレートを管理するリポジトリです。

## ブック一覧

| フォルダー | 内容 | データ ソース |
|---|---|---|
| [DefenderCSPM](./DefenderCSPM) | Microsoft Defender for Cloud（Defender CSPM）のセキュリティ態勢を可視化するブックとダッシュボード | Azure Resource Graph |

## フォルダー構成のルール

1 つのブックを 1 つのフォルダーで管理します。

| ファイル | 必須 | 内容 |
|---|---|---|
| `README.md` | ○ | ブックの概要、前提条件、導入手順 |
| `<名前>.workbook.json` | ○ | ギャラリー テンプレート（ブックの詳細エディターに貼り付ける JSON） |
| `<名前>.dashboard.json` | | ダッシュボード（プレビュー）向けの 1 画面版 |
| `<名前>.azuredeploy.json` | | ブックを展開する ARM テンプレート（`tools/build_arm.py` で生成） |

## 更新の流れ

1. Azure portal でブックを開いて編集し、[詳細エディター] → [ギャラリー テンプレート] の JSON をコピーします。
2. フォルダー内の `<名前>.workbook.json` を置き換えます。
3. ARM テンプレートを再生成します。

   ```bash
   python tools/build_arm.py DefenderCSPM/DefenderCSPM-Dashboard.workbook.json "Defender CSPM ダッシュボード"
   ```

4. 変更内容をコミットします。
