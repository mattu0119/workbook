# Defender CSPM ダッシュボード

Microsoft Defender for Cloud（Defender CSPM）が収集したセキュリティ態勢データを、Azure Resource Graph から取得して可視化するブックです。Log Analytics ワークスペースや連続エクスポートは不要です。

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fmattu0119%2Fworkbook%2Fmain%2FDefenderCSPM%2FDefenderCSPM-Dashboard.azuredeploy.json)

## ファイル

| ファイル | 用途 |
|---|---|
| [DefenderCSPM-Dashboard.workbook.json](./DefenderCSPM-Dashboard.workbook.json) | ブック版。タブで切り替えて詳細を分析します（ギャラリー テンプレート） |
| [DefenderCSPM-Dashboard.dashboard.json](./DefenderCSPM-Dashboard.dashboard.json) | ダッシュボード版。主要な指標を 1 画面にまとめています（ギャラリー テンプレート） |
| [DefenderCSPM-Dashboard.azuredeploy.json](./DefenderCSPM-Dashboard.azuredeploy.json) | ブック版を展開する ARM テンプレート |

## ブック版のタブ構成

| タブ | 内容 |
|---|---|
| 概要 | 平均セキュア スコア、未対応の推奨事項、影響を受けるリソース、リスク 重大・高、攻撃パスの件数。重要度・リスク レベル・環境別の内訳、サブスクリプション別スコア、未対応リソースが多い推奨事項トップ 10 |
| セキュア スコア | サブスクリプション別スコア、セキュリティ コントロール別の達成率と改善余地 |
| 推奨事項 | 重要度で絞り込み、リソースの種類別・カテゴリ別の件数、推奨事項一覧（行を選択すると対象リソースとリスク要因を表示） |
| 攻撃パス | リスク カテゴリ別の件数、攻撃パスの種類別インスタンス数、エントリ ポイント・ターゲット・修復手順 |
| 脆弱性 | 重要度別・評価対象別の件数、影響リソース数が多い脆弱性（CVE など）トップ 100 |
| 規制コンプライアンス | 標準ごとの合格率（行を選択すると不合格のコントロールを表示） |
| ガバナンス | ガバナンス ルールの対応状況（期限超過・期限内・完了）、担当者別の状況、期限超過の一覧 |
| プランの有効化状況 | サブスクリプション別の Defender for Cloud プラン（Defender CSPM、Servers P1/P2、Containers など） |

画面上部の「サブスクリプション」と「環境（Azure / AWS / GCP など）」で絞り込めます。環境の絞り込みは推奨事項ベースの表示に適用されます。

## ダッシュボード版の構成

| 段 | 内容 |
|---|---|
| 1 | KPI タイル：平均セキュア スコア、未対応の推奨事項、影響を受けるリソース、リスク 重大・高、攻撃パス、Defender CSPM 有効サブスクリプション数 |
| 2 | 未対応の推奨事項の内訳（重要度別・リスク レベル別・環境別） |
| 3 | サブスクリプション別セキュア スコア、未対応リソースが多い推奨事項トップ 10 |
| 4 | 攻撃パスの種類別トップ 10、脆弱性の重要度別、影響リソースが多い脆弱性トップ 10 |
| 5 | 規制コンプライアンスの合格率、ガバナンスの対応状況、Defender CSPM の有効化状況 |

## 前提条件

- 閲覧者に、対象サブスクリプション（AWS / GCP コネクタを含む）の **閲覧者 (Reader)** または **セキュリティ閲覧者 (Security Reader)** ロールが必要です。
- 次の表示は **Defender CSPM（有償）** を有効にした環境でのみデータが入ります。
  - リスク レベル / リスク要因（推奨事項のリスク優先度付け）
  - 攻撃パス
  - エージェントレス スキャンによる脆弱性（Defender for Servers Plan 2 でも取得可能）
- ガバナンスの表示は、ガバナンス ルールを設定している場合のみデータが入ります。

## 導入方法

### ブック版

- **ARM テンプレートで展開する**：上の [Deploy to Azure] ボタンから、リソース グループを指定して展開します。Azure CLI の場合は次のとおりです。

  ```bash
  az deployment group create \
    --resource-group <リソース グループ名> \
    --template-file DefenderCSPM-Dashboard.azuredeploy.json
  ```

  パラメーター `workbookSourceId` の既定値は `Azure Security Center`（Defender for Cloud のブック一覧向け）です。Azure Monitor のブック一覧に表示する場合は `azure monitor` を指定します。

- **詳細エディターに貼り付ける**：Defender for Cloud の [ブック] → [+ New] → [New workbook] → [編集] → 詳細エディター（</> アイコン）→ [ギャラリー テンプレート] に `DefenderCSPM-Dashboard.workbook.json` の内容を貼り付けて [適用] → [保存]。

### ダッシュボード版

Defender for Cloud の [ブック] → [+ New] → [New dashboard] を選び、編集画面の詳細エディターに `DefenderCSPM-Dashboard.dashboard.json` の内容を貼り付けて適用し、パーツの配置をドラッグで整えてから保存します。ダッシュボードのレイアウト（位置・サイズ）は JSON に含まれないため、初回は手動で調整してください。詳細エディターが表示されない場合は [New workbook] に貼り付けて 1 ページのサマリーとして使うか、ブックのプレビュー表示で編集メニューからダッシュボード モードに切り替えます。

## 注意事項

- リスク レベルは推奨事項データの `properties.risk.level` を参照しています。このフィールドが返らない環境では「リスク評価なし」と表示されます。
- セキュア スコアは Resource Graph 上の Azure セキュア スコア（ascScore）です。Defender ポータルの「クラウド セキュア スコア」（リスクベース）とは計算方法が異なる場合があります。
- Resource Graph への反映には時間差があり、ポータルの表示とずれることがあります。
- 初回表示時にエラーや空の表示があるパーツは、各パーツの [編集] でクエリを Resource Graph エクスプローラーに貼り付けて確認してください。
