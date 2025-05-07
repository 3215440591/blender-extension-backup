import bpy

_TRANSLATIONS = {
    "zh_CN": {
        "Extension Backup Utility": "扩展备份工具",
        "Backup Extensions(JSON)": "备份扩展(JSON)",
        "Restore Extensions(JSON)": "恢复扩展(JSON)",
        "Export a list of installed official extensions for backup or migration.": "导出已安装官方扩展列表用于备份或迁移。",
        "Install official extensions from a backup file, with version compatibility check.": "从备份文件安装官方扩展，并检查版本兼容性。",
        "No official extensions (bl_ext.blender_org.*) found.": "未找到已安装的官方扩展（bl_ext.blender_org.*）。",
        "No extensions selected for backup.": "未选择任何要备份的扩展。",
        "Backup saved to: ": "备份已保存到：",
        "Backup failed: ": "备份失败：",
        "No official extensions found.": "未找到已安装的官方扩展。",
        "Or backup path not selected.": "或未选择备份文件路径。",
        "Select extensions to backup:": "请选择要备份的扩展：",
        "Restore Extensions(JSON)": "恢复扩展(JSON)",
        "Install official extensions from a backup file, with version compatibility check.": "从备份文件安装官方扩展，并检查版本兼容性。",
        "Backup file not found or invalid path: ": "未找到备份文件或路径无效：",
        "Failed to parse JSON: ": "解析JSON失败：",
        "Failed to read backup file: ": "读取备份文件失败：",
        "Warning: Backup file is from Blender version ": "警告：备份文件来自 Blender 版本 ",
        "Current Blender version: ": "当前 Blender 版本：",
        "Some extensions may not be compatible. Proceed with caution.": "部分扩展可能不兼容，请谨慎操作。",
        "Please select a backup file.": "请选择备份文件。",
        "No extensions found in backup file.": "备份文件中未找到扩展列表。",
        "Select extensions to install:": "请选择要安装的扩展：",
        "(Installed)": "（已安装）",
        "No extension information found in backup file.": "备份文件中未包含任何扩展信息。",
        "No extensions selected for installation.": "未选择任何要安装的扩展。",
        "Installing: ": "正在安装：",
        "Successfully installed and enabled: ": "成功安装并启用：",
        "Extension already installed and enabled: ": "扩展已安装并启用：",
        "Installation failed: ": "安装失败：",
        "Unknown error during installation: ": "安装时发生未知错误：",
        "Successfully installed {}/{} extensions.": "成功安装了 {}/{} 个扩展。",
        "Failed to install the following extensions: ": "以下扩展安装失败：",
        "Extension Backup Utility": "扩展备份工具",
        "Extension Backup": "扩展备份",
    },
    "ja_JP": {
        "Extension Backup Utility": "拡張機能バックアップユーティリティ",
        "Backup Extensions(JSON)": "拡張機能をバックアップ(JSON)",
        "Restore Extensions(JSON)": "拡張機能を復元(JSON)",
        "Export a list of installed official extensions for backup or migration.": "インストール済みの公式拡張機能のリストをエクスポートしてバックアップまたは移行します。",
        "Install official extensions from a backup file, with version compatibility check.": "バックアップファイルから公式拡張機能をインストールし、バージョン互換性を確認します。",
        "No official extensions (bl_ext.blender_org.*) found.": "公式拡張機能（bl_ext.blender_org.*）が見つかりません。",
        "No extensions selected for backup.": "バックアップする拡張機能が選択されていません。",
        "Backup saved to: ": "バックアップが保存されました：",
        "Backup failed: ": "バックアップに失敗しました：",
        "No official extensions found.": "公式拡張機能が見つかりません。",
        "Or backup path not selected.": "またはバックアップパスが選択されていません。",
        "Select extensions to backup:": "バックアップする拡張機能を選択してください：",
        "Restore Extensions(JSON)": "拡張機能を復元(JSON)",
        "Backup file not found or invalid path: ": "バックアップファイルが見つからないか、パスが無効です：",
        "Failed to parse JSON: ": "JSONの解析に失敗しました：",
        "Failed to read backup file: ": "バックアップファイルの読み取りに失敗しました：",
        "Warning: Backup file is from Blender version ": "警告：バックアップファイルはBlenderバージョン",
        "Current Blender version: ": "現在のBlenderバージョン：",
        "Some extensions may not be compatible. Proceed with caution.": "一部の拡張機能は互換性がない可能性があります。注意して進めてください。",
        "Please select a backup file.": "バックアップファイルを選択してください。",
        "No extensions found in backup file.": "バックアップファイルに拡張機能が見つかりません。",
        "Select extensions to install:": "インストールする拡張機能を選択してください：",
        "(Installed)": "（インストール済み）",
        "No extension information found in backup file.": "バックアップファイルに拡張機能情報が見つかりません。",
        "No extensions selected for installation.": "インストールする拡張機能が選択されていません。",
        "Installing: ": "インストール中：",
        "Successfully installed and enabled: ": "正常にインストールおよび有効化されました：",
        "Extension already installed and enabled: ": "拡張機能はすでにインストールおよび有効化されています：",
        "Installation failed: ": "インストールに失敗しました：",
        "Unknown error during installation: ": "インストール中に不明なエラーが発生しました：",
        "Successfully installed {}/{} extensions.": "{}/{}個の拡張機能が正常にインストールされました。",
        "Failed to install the following extensions: ": "次の拡張機能のインストールに失敗しました：",
        "Extension Backup": "拡張機能バックアップ",
    }
}

def get_language():
    lang = bpy.app.translations.locale if hasattr(bpy.app, "translations") else "en_US"
    if lang.startswith("zh"):
        return "zh_CN"
    if lang.startswith("ja"):
        return "ja_JP"
    return "en_US"

def _(msgid):
    lang = get_language()
    if lang == "en_US":
        return msgid
    return _TRANSLATIONS.get(lang, {}).get(msgid, msgid)