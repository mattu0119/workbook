"""ブックのギャラリー テンプレート (*.workbook.json) から ARM テンプレート (*.azuredeploy.json) を生成します。

使い方:
    python tools/build_arm.py <workbook.json> [表示名] [sourceId]

    表示名   : 省略時はファイル名
    sourceId : 省略時は "Azure Security Center"（Defender for Cloud のブック一覧）。
               Azure Monitor のブック一覧に出す場合は "azure monitor"
"""
import json
import sys
from pathlib import Path


def build(workbook_path: Path, display_name: str, source_id: str) -> Path:
    workbook = json.loads(workbook_path.read_text(encoding="utf-8"))
    arm = {
        "$schema": "https://schema.management.azure.com/schemas/2019-04-01/deploymentTemplate.json#",
        "contentVersion": "1.0.0.0",
        "parameters": {
            "workbookDisplayName": {"type": "string", "defaultValue": display_name,
                                    "metadata": {"description": "ブックの表示名"}},
            "workbookSourceId": {"type": "string", "defaultValue": source_id,
                                 "metadata": {"description": "ブックを表示するギャラリー。Azure Monitor のブック一覧に出す場合は azure monitor を指定"}},
            "workbookId": {"type": "string", "defaultValue": "[newGuid()]",
                           "metadata": {"description": "ブックのリソース名 (GUID)"}},
            "location": {"type": "string", "defaultValue": "[resourceGroup().location]"},
        },
        "resources": [{
            "name": "[parameters('workbookId')]",
            "type": "microsoft.insights/workbooks",
            "location": "[parameters('location')]",
            "apiVersion": "2022-04-01",
            "kind": "shared",
            "properties": {
                "displayName": "[parameters('workbookDisplayName')]",
                "serializedData": json.dumps(workbook, ensure_ascii=False),
                "version": "1.0",
                "sourceId": "[parameters('workbookSourceId')]",
                "category": "workbook",
            },
        }],
        "outputs": {"workbookId": {"type": "string",
                                   "value": "[resourceId('microsoft.insights/workbooks', parameters('workbookId'))]"}},
    }
    name = workbook_path.name.replace(".workbook.json", "")
    out = workbook_path.with_name(f"{name}.azuredeploy.json")
    out.write_text(json.dumps(arm, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return out


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    path = Path(sys.argv[1])
    display = sys.argv[2] if len(sys.argv) > 2 else path.name.replace(".workbook.json", "")
    source = sys.argv[3] if len(sys.argv) > 3 else "Azure Security Center"
    print(f"生成しました: {build(path, display, source)}")
