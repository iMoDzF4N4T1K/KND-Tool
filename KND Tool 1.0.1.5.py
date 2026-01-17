# -*- coding: utf-8 -*-
# KND Tool 1.0.1.5
# - Settings: GitHub update checker + Changelog + Credits
# - Settings UI: redesigned into a numbered submenu (more intuitive)
# - Menu loop: tool no longer closes after an action (returns to main menu)
# - Auto refresh: rescans .knd files on each return to menu
# - Python compatibility: removed deprecated locale.getdefaultlocale() (future-proof 3.15+)
# - Multilingual UI: FR / EN / DE + RU / ZH / JA / IT / ES / PT
# - Config file (knd_tool_config.json): language, tunes path, defaults, update repo
# - Export .knd -> JSON/TXT (SECTION1 + SECTION2)
# - Patch from JSON (SECTION1/SECTION2/both) + backup option
# - Compare 2 KND (diff)
# - Credit ιMσDzF4Π4ΤιK

import os
import json
import struct
import re
import shutil
from datetime import datetime
import locale
import urllib.request

# Console cosmetics (Windows)
try:
    os.system("chcp 65001 > nul")  # better unicode display in console
except:
    pass
os.system("color 0E")

# -------------------- CONFIG --------------------
SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
CONFIG_PATH = os.path.join(SCRIPT_DIR, "knd_tool_config.json")

DEFAULT_CONFIG = {
    "language": "",                 # "" => auto detect
    "tunes_path": "",               # "" => auto detect
    "default_patch_section1": True,
    "default_patch_section2": True,
    "backup_before_patch": True,
    "scan_recursive": True,
    "github_repo": "",              # e.g. "USER/REPO" (empty => OFF)
    "github_check_timeout": 6,      # seconds
}

# -------------------- LANG --------------------
# Keep keys stable, add translations safely.
I18N = {
    "fr": {
        "title": "KND Tool {ver} (Kino)",
        "folder": "Dossier",
        "found_knd": "Fichiers .knd trouvés",
        "no_knd": "Aucun .knd trouvé.",
        "tip": "Astuce: mets le tool dans '...\\KN_Base\\tunes' OU laisse-le sur le bureau (recherche auto).",
        "menu": "================ MENU ================",
        "m1": "1) Exporter KND -> JSON (sections)",
        "m2": "2) Exporter KND -> TXT  (sections)",
        "m3": "3) JSON -> KND (patch) => _EDIT.knd",
        "m4": "4) Afficher les paramètres d'un KND (sections)",
        "m5": "5) Comparer 2 KND (diff)",
        "m6": "6) Paramètres",
        "m7": "7) Quitter",
        "choice": "Choix (1-7): ",
        "export_all": "Exporter TOUS les .knd ?",
        "choose_knd_export_json": "Choisis un .knd à exporter en JSON :",
        "choose_knd_export_txt": "Choisis un .knd à exporter en TXT :",
        "choose_knd_patch": "Choisis le .knd à patcher :",
        "choose_knd_show": "Choisis un .knd à afficher :",
        "choose_a": "Choisis le KND A (base) :",
        "choose_b": "Choisis le KND B (comparaison) :",
        "use_default_json": "Utiliser le JSON par défaut ?",
        "default_json": "JSON par défaut",
        "json_path": "Chemin du JSON (glisse-dépose possible): ",
        "json_missing": "JSON introuvable, annulation.",
        "patch_s1": "Patcher SECTION1 ?",
        "patch_s2": "Patcher SECTION2 ?",
        "backup": "Faire un backup avant patch ?",
        "backup_done": "Backup",
        "export_json_ok": "Export JSON",
        "export_txt_ok": "Export TXT",
        "patch_ok": "Patch OK",
        "patched": "patched",
        "ignored": "ignored",
        "cancel": "Annulé.",
        "bye": "Bye.",
        "press_key": "Appuyez sur une touche pour continuer...",
        "settings_title": "============= PARAMETRES =============",
        "settings_lang": "Langue",
        "settings_path": "Chemin tunes",
        "settings_defaults": "Valeurs par défaut",
        "settings_save": "Sauvegarder ?",
        "settings_set_lang": "Changer la langue ?",
        "settings_set_path": "Changer le chemin du dossier tunes ?",
        "settings_toggle": "Modifier les options par défaut ?",
        "lang_pick": "Entre le code: fr/en/de/ru/zh/ja/it/es/pt ou 'auto'",
        "enter_path": "Colle le chemin complet du dossier tunes (ou ENTER=annuler): ",
        "invalid_path": "Chemin invalide (dossier introuvable).",
        "opt_patch_s1": "Par défaut: patch SECTION1",
        "opt_patch_s2": "Par défaut: patch SECTION2",
        "opt_backup": "Par défaut: backup avant patch",
        "opt_scanrec": "Scan récursif",
        "saved": "Config sauvegardée.",
    },
    "en": {
        "title": "KND Tool {ver} (Kino)",
        "folder": "Folder",
        "found_knd": ".knd files found",
        "no_knd": "No .knd found.",
        "tip": "Tip: place the tool in '...\\KN_Base\\tunes' OR run it from Desktop (auto search).",
        "menu": "================ MENU ================",
        "m1": "1) Export KND -> JSON (sections)",
        "m2": "2) Export KND -> TXT  (sections)",
        "m3": "3) JSON -> KND (patch) => _EDIT.knd",
        "m4": "4) Show KND parameters (sections)",
        "m5": "5) Compare 2 KND (diff)",
        "m6": "6) Settings",
        "m7": "7) Quit",
        "choice": "Choice (1-7): ",
        "export_all": "Export ALL .knd ?",
        "choose_knd_export_json": "Pick a .knd to export as JSON:",
        "choose_knd_export_txt": "Pick a .knd to export as TXT:",
        "choose_knd_patch": "Pick the .knd to patch:",
        "choose_knd_show": "Pick a .knd to show:",
        "choose_a": "Pick KND A (base):",
        "choose_b": "Pick KND B (compare):",
        "use_default_json": "Use default JSON?",
        "default_json": "Default JSON",
        "json_path": "JSON path (drag&drop supported): ",
        "json_missing": "JSON not found, cancelled.",
        "patch_s1": "Patch SECTION1?",
        "patch_s2": "Patch SECTION2?",
        "backup": "Backup before patch?",
        "backup_done": "Backup",
        "export_json_ok": "JSON export",
        "export_txt_ok": "TXT export",
        "patch_ok": "Patch OK",
        "patched": "patched",
        "ignored": "ignored",
        "cancel": "Cancelled.",
        "bye": "Bye.",
        "press_key": "Press any key to continue...",
        "settings_title": "============== SETTINGS ==============",
        "settings_lang": "Language",
        "settings_path": "Tunes path",
        "settings_defaults": "Defaults",
        "settings_save": "Save?",
        "settings_set_lang": "Change language?",
        "settings_set_path": "Change tunes folder path?",
        "settings_toggle": "Edit default options?",
        "lang_pick": "Enter code: fr/en/de/ru/zh/ja/it/es/pt or 'auto'",
        "enter_path": "Paste full tunes folder path (or ENTER=cancel): ",
        "invalid_path": "Invalid path (folder not found).",
        "opt_patch_s1": "Default: patch SECTION1",
        "opt_patch_s2": "Default: patch SECTION2",
        "opt_backup": "Default: backup before patch",
        "opt_scanrec": "Recursive scan",
        "saved": "Config saved.",
    },
    "de": {
        "title": "KND Tool {ver} (Kino)",
        "folder": "Ordner",
        "found_knd": ".knd Dateien gefunden",
        "no_knd": "Keine .knd gefunden.",
        "tip": "Tipp: Tool in '...\\KN_Base\\tunes' legen ODER vom Desktop starten (Auto-Suche).",
        "menu": "================ MENU ================",
        "m1": "1) KND -> JSON exportieren (Sektionen)",
        "m2": "2) KND -> TXT exportieren  (Sektionen)",
        "m3": "3) JSON -> KND (Patch) => _EDIT.knd",
        "m4": "4) KND-Parameter anzeigen (Sektionen)",
        "m5": "5) 2 KND vergleichen (Diff)",
        "m6": "6) Einstellungen",
        "m7": "7) Beenden",
        "choice": "Auswahl (1-7): ",
        "export_all": "ALLE .knd exportieren?",
        "choose_knd_export_json": ".knd für JSON-Export wählen:",
        "choose_knd_export_txt": ".knd für TXT-Export wählen:",
        "choose_knd_patch": ".knd zum Patchen wählen:",
        "choose_knd_show": ".knd zum Anzeigen wählen:",
        "choose_a": "KND A (Basis) wählen:",
        "choose_b": "KND B (Vergleich) wählen:",
        "use_default_json": "Standard-JSON benutzen?",
        "default_json": "Standard-JSON",
        "json_path": "JSON-Pfad (Drag&Drop möglich): ",
        "json_missing": "JSON nicht gefunden, abgebrochen.",
        "patch_s1": "SECTION1 patchen?",
        "patch_s2": "SECTION2 patchen?",
        "backup": "Backup vor Patch?",
        "backup_done": "Backup",
        "export_json_ok": "JSON Export",
        "export_txt_ok": "TXT Export",
        "patch_ok": "Patch OK",
        "patched": "patched",
        "ignored": "ignored",
        "cancel": "Abgebrochen.",
        "bye": "Tschüss.",
        "press_key": "Beliebige Taste drücken...",
        "settings_title": "============ EINSTELLUNGEN ==========",
        "settings_lang": "Sprache",
        "settings_path": "Tunes-Pfad",
        "settings_defaults": "Standardwerte",
        "settings_save": "Speichern?",
        "settings_set_lang": "Sprache ändern?",
        "settings_set_path": "Tunes-Ordner ändern?",
        "settings_toggle": "Standardoptionen ändern?",
        "lang_pick": "Code eingeben: fr/en/de/ru/zh/ja/it/es/pt oder 'auto'",
        "enter_path": "Vollen Tunes-Ordnerpfad einfügen (oder ENTER=Abbruch): ",
        "invalid_path": "Ungültiger Pfad (Ordner nicht gefunden).",
        "opt_patch_s1": "Standard: SECTION1 patchen",
        "opt_patch_s2": "Standard: SECTION2 patchen",
        "opt_backup": "Standard: Backup vor Patch",
        "opt_scanrec": "Rekursiver Scan",
        "saved": "Config gespeichert.",
    },
}

# Add extra languages
I18N["ru"] = {  # (same as you pasted)
    "title": "KND Tool {ver} (Kino)",
    "folder": "Папка",
    "found_knd": "Найдено файлов .knd",
    "no_knd": "Файлы .knd не найдены.",
    "tip": "Совет: положи tool в '...\\KN_Base\\tunes' или запускай с рабочего стола (автопоиск).",
    "menu": "================ MENU ================",
    "m1": "1) Экспорт KND -> JSON (секции)",
    "m2": "2) Экспорт KND -> TXT  (секции)",
    "m3": "3) JSON -> KND (патч) => _EDIT.knd",
    "m4": "4) Показать параметры KND (секции)",
    "m5": "5) Сравнить 2 KND (diff)",
    "m6": "6) Настройки",
    "m7": "7) Выход",
    "choice": "Выбор (1-7): ",
    "export_all": "Экспортировать ВСЕ .knd?",
    "choose_knd_export_json": "Выбери .knd для экспорта в JSON:",
    "choose_knd_export_txt": "Выбери .knd для экспорта в TXT:",
    "choose_knd_patch": "Выбери .knd для патча:",
    "choose_knd_show": "Выбери .knd для просмотра:",
    "choose_a": "Выбери KND A (база):",
    "choose_b": "Выбери KND B (сравнение):",
    "use_default_json": "Использовать JSON по умолчанию?",
    "default_json": "JSON по умолчанию",
    "json_path": "Путь к JSON (можно drag&drop): ",
    "json_missing": "JSON не найден, отмена.",
    "patch_s1": "Патчить SECTION1?",
    "patch_s2": "Патчить SECTION2?",
    "backup": "Сделать backup перед патчем?",
    "backup_done": "Backup",
    "export_json_ok": "Экспорт JSON",
    "export_txt_ok": "Экспорт TXT",
    "patch_ok": "Патч OK",
    "patched": "изменено",
    "ignored": "пропущено",
    "cancel": "Отменено.",
    "bye": "Пока.",
    "press_key": "Нажмите любую клавишу...",
    "settings_title": "============= НАСТРОЙКИ =============",
    "settings_lang": "Язык",
    "settings_path": "Путь tunes",
    "settings_defaults": "Значения по умолчанию",
    "settings_save": "Сохранить?",
    "settings_set_lang": "Сменить язык?",
    "settings_set_path": "Сменить путь к папке tunes?",
    "settings_toggle": "Изменить параметры по умолчанию?",
    "lang_pick": "Введи код языка: fr/en/de/ru/zh/ja/it/es/pt или 'auto'",
    "enter_path": "Вставь полный путь к папке tunes (или ENTER чтобы отменить): ",
    "invalid_path": "Неверный путь (папка не найдена).",
    "opt_patch_s1": "По умолчанию: патчить SECTION1",
    "opt_patch_s2": "По умолчанию: патчить SECTION2",
    "opt_backup": "По умолчанию: backup перед патчем",
    "opt_scanrec": "Рекурсивный скан",
    "saved": "Конфиг сохранён.",
}

I18N["zh"] = {  # simplified chinese
    "title": "KND 工具 {ver} (Kino)",
    "folder": "目录",
    "found_knd": "找到 .knd 文件数量",
    "no_knd": "未找到 .knd 文件。",
    "tip": "提示：把工具放到 '...\\KN_Base\\tunes' 或放在桌面运行（自动搜索）。",
    "menu": "================ MENU ================",
    "m1": "1) 导出 KND -> JSON（分区）",
    "m2": "2) 导出 KND -> TXT（分区）",
    "m3": "3) JSON -> KND（写入）=> _EDIT.knd",
    "m4": "4) 查看 KND 参数（分区）",
    "m5": "5) 对比 2 个 KND（差异）",
    "m6": "6) 设置",
    "m7": "7) 退出",
    "choice": "选择 (1-7): ",
    "export_all": "导出所有 .knd？",
    "choose_knd_export_json": "选择要导出为 JSON 的 .knd：",
    "choose_knd_export_txt": "选择要导出为 TXT 的 .knd：",
    "choose_knd_patch": "选择要写入的 .knd：",
    "choose_knd_show": "选择要查看的 .knd：",
    "choose_a": "选择 KND A（基准）：",
    "choose_b": "选择 KND B（对比）：",
    "use_default_json": "使用默认 JSON？",
    "default_json": "默认 JSON",
    "json_path": "JSON 路径（支持拖拽）：",
    "json_missing": "未找到 JSON，已取消。",
    "patch_s1": "写入 SECTION1？",
    "patch_s2": "写入 SECTION2？",
    "backup": "写入前备份？",
    "backup_done": "备份",
    "export_json_ok": "JSON 导出",
    "export_txt_ok": "TXT 导出",
    "patch_ok": "写入完成",
    "patched": "已写入",
    "ignored": "已忽略",
    "cancel": "已取消。",
    "bye": "再见。",
    "press_key": "按任意键继续…",
    "settings_title": "=============== 设置 ================",
    "settings_lang": "语言",
    "settings_path": "tunes 路径",
    "settings_defaults": "默认选项",
    "settings_save": "保存？",
    "settings_set_lang": "更改语言？",
    "settings_set_path": "更改 tunes 文件夹路径？",
    "settings_toggle": "修改默认选项？",
    "lang_pick": "输入语言代码：fr/en/de/ru/zh/ja/it/es/pt 或输入 'auto'",
    "enter_path": "粘贴 tunes 文件夹完整路径（或回车取消）：",
    "invalid_path": "路径无效（找不到文件夹）。",
    "opt_patch_s1": "默认：写入 SECTION1",
    "opt_patch_s2": "默认：写入 SECTION2",
    "opt_backup": "默认：写入前备份",
    "opt_scanrec": "递归扫描",
    "saved": "配置已保存。",
}

I18N["ja"] = {  # japanese
    "title": "KND ツール {ver} (Kino)",
    "folder": "フォルダ",
    "found_knd": ".knd ファイル数",
    "no_knd": ".knd が見つかりません。",
    "tip": "ヒント: '...\\KN_Base\\tunes' に置くか、デスクトップから実行（自動検索）。",
    "menu": "================ MENU ================",
    "m1": "1) KND -> JSON 出力（セクション）",
    "m2": "2) KND -> TXT 出力（セクション）",
    "m3": "3) JSON -> KND（パッチ）=> _EDIT.knd",
    "m4": "4) KND パラメータ表示（セクション）",
    "m5": "5) 2つのKNDを比較（差分）",
    "m6": "6) 設定",
    "m7": "7) 終了",
    "choice": "選択 (1-7): ",
    "export_all": "すべての .knd を出力しますか？",
    "choose_knd_export_json": "JSON に出力する .knd を選択:",
    "choose_knd_export_txt": "TXT に出力する .knd を選択:",
    "choose_knd_patch": "パッチする .knd を選択:",
    "choose_knd_show": "表示する .knd を選択:",
    "choose_a": "KND A（ベース）を選択:",
    "choose_b": "KND B（比較）を選択:",
    "use_default_json": "デフォルト JSON を使いますか？",
    "default_json": "デフォルト JSON",
    "json_path": "JSON のパス（ドラッグ&ドロップ可）: ",
    "json_missing": "JSON が見つかりません。中止しました。",
    "patch_s1": "SECTION1 をパッチしますか？",
    "patch_s2": "SECTION2 をパッチしますか？",
    "backup": "パッチ前にバックアップしますか？",
    "backup_done": "バックアップ",
    "export_json_ok": "JSON 出力",
    "export_txt_ok": "TXT 出力",
    "patch_ok": "パッチ完了",
    "patched": "適用",
    "ignored": "無視",
    "cancel": "キャンセルしました。",
    "bye": "終了。",
    "press_key": "続行するには何かキーを押してください…",
    "settings_title": "=============== 設定 ================",
    "settings_lang": "言語",
    "settings_path": "tunes パス",
    "settings_defaults": "既定値",
    "settings_save": "保存しますか？",
    "settings_set_lang": "言語を変更しますか？",
    "settings_set_path": "tunes フォルダのパスを変更しますか？",
    "settings_toggle": "既定オプションを編集しますか？",
    "lang_pick": "言語コードを入力: fr/en/de/ru/zh/ja/it/es/pt または 'auto'",
    "enter_path": "tunes フォルダのフルパスを貼り付け（ENTERで中止）: ",
    "invalid_path": "無効なパス（フォルダが見つかりません）。",
    "opt_patch_s1": "既定: SECTION1 をパッチ",
    "opt_patch_s2": "既定: SECTION2 をパッチ",
    "opt_backup": "既定: パッチ前にバックアップ",
    "opt_scanrec": "再帰スキャン",
    "saved": "設定を保存しました。",
}

I18N["it"] = {
    "title": "KND Tool {ver} (Kino)",
    "folder": "Cartella",
    "found_knd": "File .knd trovati",
    "no_knd": "Nessun file .knd trovato.",
    "tip": "Suggerimento: metti il tool in '...\\KN_Base\\tunes' oppure eseguilo dal Desktop (ricerca automatica).",
    "menu": "================ MENU ================",
    "m1": "1) Esporta KND -> JSON (sezioni)",
    "m2": "2) Esporta KND -> TXT  (sezioni)",
    "m3": "3) JSON -> KND (patch) => _EDIT.knd",
    "m4": "4) Mostra parametri KND (sezioni)",
    "m5": "5) Confronta 2 KND (diff)",
    "m6": "6) Impostazioni",
    "m7": "7) Esci",
    "choice": "Scelta (1-7): ",
    "export_all": "Esportare TUTTI i .knd?",
    "choose_knd_export_json": "Scegli un .knd da esportare in JSON:",
    "choose_knd_export_txt": "Scegli un .knd da esportare in TXT:",
    "choose_knd_patch": "Scegli il .knd da patchare:",
    "choose_knd_show": "Scegli un .knd da mostrare:",
    "choose_a": "Scegli KND A (base):",
    "choose_b": "Scegli KND B (confronto):",
    "use_default_json": "Usare il JSON predefinito?",
    "default_json": "JSON predefinito",
    "json_path": "Percorso JSON (drag&drop supportato): ",
    "json_missing": "JSON non trovato, annullato.",
    "patch_s1": "Patch SECTION1?",
    "patch_s2": "Patch SECTION2?",
    "backup": "Backup prima del patch?",
    "backup_done": "Backup",
    "export_json_ok": "Export JSON",
    "export_txt_ok": "Export TXT",
    "patch_ok": "Patch OK",
    "patched": "patchati",
    "ignored": "ignorati",
    "cancel": "Annullato.",
    "bye": "Ciao.",
    "press_key": "Premi un tasto per continuare...",
    "settings_title": "============= IMPOSTAZIONI ============",
    "settings_lang": "Lingua",
    "settings_path": "Percorso tunes",
    "settings_defaults": "Valori predefiniti",
    "settings_save": "Salvare?",
    "settings_set_lang": "Cambiare lingua?",
    "settings_set_path": "Cambiare percorso cartella tunes?",
    "settings_toggle": "Modificare opzioni predefinite?",
    "lang_pick": "Inserisci il codice lingua: fr/en/de/ru/zh/ja/it/es/pt oppure 'auto'",
    "enter_path": "Incolla il percorso completo della cartella tunes (o ENTER per annullare): ",
    "invalid_path": "Percorso non valido (cartella non trovata).",
    "opt_patch_s1": "Predefinito: patch SECTION1",
    "opt_patch_s2": "Predefinito: patch SECTION2",
    "opt_backup": "Predefinito: backup prima del patch",
    "opt_scanrec": "Scansione ricorsiva",
    "saved": "Config salvata.",
}

I18N["es"] = {
    "title": "KND Tool {ver} (Kino)",
    "folder": "Carpeta",
    "found_knd": "Archivos .knd encontrados",
    "no_knd": "No se encontraron archivos .knd.",
    "tip": "Consejo: pon el tool en '...\\KN_Base\\tunes' o ejecútalo desde el Escritorio (búsqueda automática).",
    "menu": "================ MENU ================",
    "m1": "1) Exportar KND -> JSON (secciones)",
    "m2": "2) Exportar KND -> TXT  (secciones)",
    "m3": "3) JSON -> KND (patch) => _EDIT.knd",
    "m4": "4) Ver parámetros KND (secciones)",
    "m5": "5) Comparar 2 KND (diff)",
    "m6": "6) Ajustes",
    "m7": "7) Salir",
    "choice": "Opción (1-7): ",
    "export_all": "¿Exportar TODOS los .knd?",
    "choose_knd_export_json": "Elige un .knd para exportar a JSON:",
    "choose_knd_export_txt": "Elige un .knd para exportar a TXT:",
    "choose_knd_patch": "Elige el .knd para parchear:",
    "choose_knd_show": "Elige un .knd para ver:",
    "choose_a": "Elige KND A (base):",
    "choose_b": "Elige KND B (comparación):",
    "use_default_json": "¿Usar el JSON por defecto?",
    "default_json": "JSON por defecto",
    "json_path": "Ruta del JSON (soporta arrastrar y soltar): ",
    "json_missing": "JSON no encontrado, cancelado.",
    "patch_s1": "¿Parchear SECTION1?",
    "patch_s2": "¿Parchear SECTION2?",
    "backup": "¿Copia de seguridad antes de parchear?",
    "backup_done": "Backup",
    "export_json_ok": "Export JSON",
    "export_txt_ok": "Export TXT",
    "patch_ok": "Patch OK",
    "patched": "modificados",
    "ignored": "ignorados",
    "cancel": "Cancelado.",
    "bye": "Adiós.",
    "press_key": "Pulsa una tecla para continuar...",
    "settings_title": "=============== AJUSTES ===============",
    "settings_lang": "Idioma",
    "settings_path": "Ruta tunes",
    "settings_defaults": "Valores por defecto",
    "settings_save": "¿Guardar?",
    "settings_set_lang": "¿Cambiar idioma?",
    "settings_set_path": "¿Cambiar ruta de la carpeta tunes?",
    "settings_toggle": "¿Editar opciones por defecto?",
    "lang_pick": "Escribe el código de idioma: fr/en/de/ru/zh/ja/it/es/pt o 'auto'",
    "enter_path": "Pega la ruta completa de la carpeta tunes (o ENTER para cancelar): ",
    "invalid_path": "Ruta inválida (carpeta no encontrada).",
    "opt_patch_s1": "Por defecto: parchear SECTION1",
    "opt_patch_s2": "Por defecto: parchear SECTION2",
    "opt_backup": "Por defecto: backup antes del patch",
    "opt_scanrec": "Escaneo recursivo",
    "saved": "Config guardada.",
}

I18N["pt"] = {
    "title": "KND Tool {ver} (Kino)",
    "folder": "Pasta",
    "found_knd": "Arquivos .knd encontrados",
    "no_knd": "Nenhum arquivo .knd encontrado.",
    "tip": "Dica: coloque o tool em '...\\KN_Base\\tunes' ou execute da Área de Trabalho (busca automática).",
    "menu": "================ MENU ================",
    "m1": "1) Exportar KND -> JSON (seções)",
    "m2": "2) Exportar KND -> TXT  (seções)",
    "m3": "3) JSON -> KND (patch) => _EDIT.knd",
    "m4": "4) Mostrar parâmetros do KND (seções)",
    "m5": "5) Comparar 2 KND (diff)",
    "m6": "6) Configurações",
    "m7": "7) Sair",
    "choice": "Opção (1-7): ",
    "export_all": "Exportar TODOS os .knd?",
    "choose_knd_export_json": "Escolha um .knd para exportar em JSON:",
    "choose_knd_export_txt": "Escolha um .knd para exportar em TXT:",
    "choose_knd_patch": "Escolha o .knd para aplicar patch:",
    "choose_knd_show": "Escolha um .knd para visualizar:",
    "choose_a": "Escolha KND A (base):",
    "choose_b": "Escolha KND B (comparação):",
    "use_default_json": "Usar o JSON padrão?",
    "default_json": "JSON padrão",
    "json_path": "Caminho do JSON (suporta arrastar e soltar): ",
    "json_missing": "JSON não encontrado, cancelado.",
    "patch_s1": "Aplicar patch na SECTION1?",
    "patch_s2": "Aplicar patch na SECTION2?",
    "backup": "Fazer backup antes do patch?",
    "backup_done": "Backup",
    "export_json_ok": "Export JSON",
    "export_txt_ok": "Export TXT",
    "patch_ok": "Patch OK",
    "patched": "alterados",
    "ignored": "ignorados",
    "cancel": "Cancelado.",
    "bye": "Tchau.",
    "press_key": "Pressione qualquer tecla para continuar...",
    "settings_title": "============ CONFIGURACOES ============",
    "settings_lang": "Idioma",
    "settings_path": "Caminho tunes",
    "settings_defaults": "Padroes",
    "settings_save": "Salvar?",
    "settings_set_lang": "Mudar idioma?",
    "settings_set_path": "Mudar caminho da pasta tunes?",
    "settings_toggle": "Editar opcoes padrao?",
    "lang_pick": "Digite o codigo do idioma: fr/en/de/ru/zh/ja/it/es/pt ou 'auto'",
    "enter_path": "Cole o caminho completo da pasta tunes (ou ENTER para cancelar): ",
    "invalid_path": "Caminho invalido (pasta nao encontrada).",
    "opt_patch_s1": "Padrao: patch SECTION1",
    "opt_patch_s2": "Padrao: patch SECTION2",
    "opt_backup": "Padrao: backup antes do patch",
    "opt_scanrec": "Varredura recursiva",
    "saved": "Config salva.",
}


# -------------------- I18N Extra (Settings submenu) --------------------
# Adds missing keys used by the Settings numbered submenu.
I18N_EXTRA = {
    "fr": {
        "settings_menu_title": "=========== PARAMETRES ===========",
        "settings_item_language": "Langue",
        "settings_item_path": "Chemin tunes",
        "settings_item_defaults": "Options par defaut",
        "settings_item_update": "Update",
        "settings_item_changelog": "Changelog",
        "settings_item_credits": "Credits",
        "settings_item_back": "Retour",
        "choice_1_5": "Choix (1-5): ",
        "choice_1_3": "Choix (1-3): ",
        "current": "Actuel",
        "enter_cancel_auto": "ENTER = annuler | 'auto' = Auto",
        "invalid_choice": "Choix invalide.",
        "invalid_lang_code": "Code langue invalide.",
        "update_repo": "GitHub repo",
        "update_configure": "Configurer repo",
        "update_check": "Verifier maintenant",
        "update_need_repo": "Update OFF: configure d'abord un repo (option 1).",
        "update_set_repo_prompt": "Repo (format: USER/REPO) ou ENTER pour OFF: ",
    },
    "en": {
        "settings_menu_title": "============= SETTINGS =============",
        "settings_item_language": "Language",
        "settings_item_path": "Tunes path",
        "settings_item_defaults": "Default options",
        "settings_item_update": "Update",
        "settings_item_changelog": "Changelog",
        "settings_item_credits": "Credits",
        "settings_item_back": "Back",
        "choice_1_5": "Choice (1-5): ",
        "choice_1_3": "Choice (1-3): ",
        "current": "Current",
        "enter_cancel_auto": "ENTER = cancel | 'auto' = Auto",
        "invalid_choice": "Invalid choice.",
        "invalid_lang_code": "Invalid language code.",
        "update_repo": "GitHub repo",
        "update_configure": "Set repo",
        "update_check": "Check now",
        "update_need_repo": "Update OFF: set a repo first (option 1).",
        "update_set_repo_prompt": "Repo (format: USER/REPO) or ENTER for OFF: ",
    },
    "de": {
        "settings_menu_title": "============= EINSTELLUNGEN =============",
        "settings_item_language": "Sprache",
        "settings_item_path": "Tunes-Pfad",
        "settings_item_defaults": "Standardoptionen",
        "settings_item_update": "Update",
        "settings_item_changelog": "Changelog",
        "settings_item_credits": "Credits",
        "settings_item_back": "Zuruck",
        "choice_1_5": "Wahl (1-5): ",
        "choice_1_3": "Wahl (1-3): ",
        "current": "Aktuell",
        "enter_cancel_auto": "ENTER = Abbrechen | 'auto' = Auto",
        "invalid_choice": "Ungueltige Auswahl.",
        "invalid_lang_code": "Ungueltiger Sprachcode.",
        "update_repo": "GitHub Repo",
        "update_configure": "Repo setzen",
        "update_check": "Jetzt prufen",
        "update_need_repo": "Update OFF: zuerst Repo setzen (Option 1).",
        "update_set_repo_prompt": "Repo (Format: USER/REPO) oder ENTER fur OFF: ",
    },
    "ru": {
        "settings_menu_title": "=========== ПАРАМЕТРЫ ===========",
        "settings_item_language": "Язык",
        "settings_item_path": "Путь tunes",
        "settings_item_defaults": "Опции по умолчанию",
        "settings_item_update": "Обновление",
        "settings_item_changelog": "История версий",
        "settings_item_credits": "Авторы",
        "settings_item_back": "Назад",
        "choice_1_5": "Выбор (1-5): ",
        "choice_1_3": "Выбор (1-3): ",
        "current": "Текущий",
        "enter_cancel_auto": "ENTER = отмена | 'auto' = Auto",
        "invalid_choice": "Неверный выбор.",
        "invalid_lang_code": "Неверный код языка.",
        "update_repo": "GitHub repo",
        "update_configure": "Настроить repo",
        "update_check": "Проверить сейчас",
        "update_need_repo": "Update OFF: сначала настрой repo (пункт 1).",
        "update_set_repo_prompt": "Repo (формат: USER/REPO) или ENTER для OFF: ",
    },
    "zh": {
        "settings_menu_title": "============= 设置 =============",
        "settings_item_language": "语言",
        "settings_item_path": "tunes 路径",
        "settings_item_defaults": "默认选项",
        "settings_item_update": "更新",
        "settings_item_changelog": "更新日志",
        "settings_item_credits": "致谢",
        "settings_item_back": "返回",
        "choice_1_5": "选择 (1-5): ",
        "choice_1_3": "选择 (1-3): ",
        "current": "当前",
        "enter_cancel_auto": "ENTER = 取消 | 'auto' = 自动",
        "invalid_choice": "选择无效。",
        "invalid_lang_code": "语言代码无效。",
        "update_repo": "GitHub 仓库",
        "update_configure": "设置仓库",
        "update_check": "立即检查",
        "update_need_repo": "更新关闭：请先设置仓库（选项 1）。",
        "update_set_repo_prompt": "仓库 (USER/REPO) 或回车关闭: ",
    },
    "ja": {
        "settings_menu_title": "=============== 設定 ===============",
        "settings_item_language": "言語",
        "settings_item_path": "tunes パス",
        "settings_item_defaults": "既定オプション",
        "settings_item_update": "更新",
        "settings_item_changelog": "更新履歴",
        "settings_item_credits": "クレジット",
        "settings_item_back": "戻る",
        "choice_1_5": "選択 (1-5): ",
        "choice_1_3": "選択 (1-3): ",
        "current": "現在",
        "enter_cancel_auto": "ENTER = キャンセル | 'auto' = 自動",
        "invalid_choice": "無効な選択です。",
        "invalid_lang_code": "無効な言語コードです。",
        "update_repo": "GitHub リポジトリ",
        "update_configure": "リポジトリ設定",
        "update_check": "今すぐ確認",
        "update_need_repo": "更新OFF: 先にリポジトリを設定してください (1)。",
        "update_set_repo_prompt": "Repo (USER/REPO) または ENTER でOFF: ",
    },
    "it": {
        "settings_menu_title": "============= IMPOSTAZIONI =============",
        "settings_item_language": "Lingua",
        "settings_item_path": "Percorso tunes",
        "settings_item_defaults": "Valori predefiniti",
        "settings_item_update": "Aggiornamento",
        "settings_item_changelog": "Changelog",
        "settings_item_credits": "Crediti",
        "settings_item_back": "Indietro",
        "choice_1_5": "Scelta (1-5): ",
        "choice_1_3": "Scelta (1-3): ",
        "current": "Attuale",
        "enter_cancel_auto": "ENTER = annulla | 'auto' = Auto",
        "invalid_choice": "Scelta non valida.",
        "invalid_lang_code": "Codice lingua non valido.",
        "update_repo": "GitHub repo",
        "update_configure": "Imposta repo",
        "update_check": "Controlla ora",
        "update_need_repo": "Update OFF: imposta prima un repo (opzione 1).",
        "update_set_repo_prompt": "Repo (formato: USER/REPO) o ENTER per OFF: ",
    },
    "es": {
        "settings_menu_title": "============= AJUSTES =============",
        "settings_item_language": "Idioma",
        "settings_item_path": "Ruta tunes",
        "settings_item_defaults": "Opciones por defecto",
        "settings_item_update": "Actualizacion",
        "settings_item_changelog": "Changelog",
        "settings_item_credits": "Creditos",
        "settings_item_back": "Volver",
        "choice_1_5": "Opcion (1-5): ",
        "choice_1_3": "Opcion (1-3): ",
        "current": "Actual",
        "enter_cancel_auto": "ENTER = cancelar | 'auto' = Auto",
        "invalid_choice": "Opcion invalida.",
        "invalid_lang_code": "Codigo de idioma invalido.",
        "update_repo": "GitHub repo",
        "update_configure": "Configurar repo",
        "update_check": "Verificar ahora",
        "update_need_repo": "Update OFF: configura un repo primero (opcion 1).",
        "update_set_repo_prompt": "Repo (formato: USER/REPO) o ENTER para OFF: ",
    },
    "pt": {
        "settings_menu_title": "============ CONFIGURACOES ============",
        "settings_item_language": "Idioma",
        "settings_item_path": "Caminho tunes",
        "settings_item_defaults": "Padroes",
        "settings_item_update": "Atualizacao",
        "settings_item_changelog": "Changelog",
        "settings_item_credits": "Creditos",
        "settings_item_back": "Voltar",
        "choice_1_5": "Opcao (1-5): ",
        "choice_1_3": "Opcao (1-3): ",
        "current": "Atual",
        "enter_cancel_auto": "ENTER = cancelar | 'auto' = Auto",
        "invalid_choice": "Opcao invalida.",
        "invalid_lang_code": "Codigo de idioma invalido.",
        "update_repo": "GitHub repo",
        "update_configure": "Configurar repo",
        "update_check": "Verificar agora",
        "update_need_repo": "Update OFF: configure um repo primeiro (opcao 1).",
        "update_set_repo_prompt": "Repo (formato: USER/REPO) ou ENTER para OFF: ",
    },
}

for _lang, _extra in I18N_EXTRA.items():
    if _lang in I18N:
        for _k, _v in _extra.items():
            if _k not in I18N[_lang]:
                I18N[_lang][_k] = _v

# -------------------- Helpers --------------------
KEY_RE = re.compile(rb"^[A-Za-z0-9_]+$")

def yn(prompt, default_yes=True):
    suffix = " [Y/n] " if default_yes else " [y/N] "
    while True:
        s = input(prompt + suffix).strip().lower()
        if s == "":
            return default_yes
        if s in ("y", "yes", "o", "oui"):
            return True
        if s in ("n", "no", "non"):
            return False
        print("Réponds par Y ou N." if True else "Answer Y or N.")

def pause():
    os.system("pause")

def detect_system_lang():
    """
    Python 3.11+ safe (no locale.getdefaultlocale).
    Tries:
      1) locale.getlocale()
      2) Windows env vars: LC_ALL / LANG / LANGUAGE
    Returns one of: fr, en, de, ru, zh, ja, it, es, pt
    """
    loc = ""

    # 1) Python locale
    try:
        loc = (locale.getlocale()[0] or "").lower()
    except:
        loc = ""

    # 2) Fallback env (Windows / cross-platform)
    if not loc:
        for k in ("LC_ALL", "LANG", "LANGUAGE"):
            v = os.environ.get(k, "")
            if v:
                loc = v.lower()
                break

    # Normalize a bit
    # examples: "fr_FR", "en_US", "de_DE", "pt_BR", "zh_CN", "ja_JP"
    if loc.startswith("fr"):
        return "fr"
    if loc.startswith("en"):
        return "en"
    if loc.startswith("de"):
        return "de"
    if loc.startswith("ru"):
        return "ru"
    if loc.startswith("zh"):
        return "zh"
    if loc.startswith("ja"):
        return "ja"
    if loc.startswith("it"):
        return "it"
    if loc.startswith("es"):
        return "es"
    if loc.startswith("pt"):
        return "pt"

    return "en"


# -------------------- UPDATE / CHANGELOG / CREDITS --------------------
CHANGELOG_TEXT = """KND Tool - Changelog

1.0.1.5
- Settings: fully translated submenu (no mixed FR/other languages)
- Fixed Settings > Update: now calls correct function (check_github_update)

1.0.1.4
- Settings: redesigned into a numbered submenu (more intuitive)

1.0.1.3
- Settings: added GitHub update checker (checks latest release tag)
- Settings: added Changelog and Credits display

1.0.1.2
- Menu loop: tool no longer closes after an action (returns to main menu)
- Auto refresh: rescans .knd files each time you return to the menu
- Locale: removed deprecated locale.getdefaultlocale() (Python 3.15+ safe)
- Multilingual UI: FR/EN/DE + RU/ZH/JA/IT/ES/PT
- Config file: saves language, tunes path, defaults
- Export JSON/TXT: SECTION1 + SECTION2
- Patch from JSON: per-section selection + backup
- Compare 2 KND: diff by sections
"""

CREDITS_TEXT = """KND Tool (Kino)\n\nAuthor / Credit: ιMσDzF4Π4ΤιK\n\nThanks:\n- CarX community modders\n- Testers / users\n\nGitHub:\n- You can set your repo in Settings to enable update checks.\n"""


def show_changelog():
    print("\n" + CHANGELOG_TEXT.strip() + "\n")


def show_credits():
    print("\n" + CREDITS_TEXT.strip() + "\n")


def ver_tuple(v: str):
    v = (v or "").strip().lower()
    if v.startswith("v"):
        v = v[1:]
    parts = []
    for x in v.split("."):
        try:
            parts.append(int(x))
        except:
            parts.append(0)
    while len(parts) < 4:
        parts.append(0)
    return tuple(parts[:4])


def http_get_json(url: str, timeout: int = 6):
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "KND-Tool-Update-Checker",
            "Accept": "application/vnd.github+json",
        },
    )
    with urllib.request.urlopen(req, timeout=timeout) as r:
        data = r.read().decode("utf-8", errors="replace")
    return json.loads(data)


def check_github_update(current_version: str):
    repo = (CFG.get("github_repo") or "").strip()
    if not repo:
        print("Update GitHub OFF (configure github_repo in Settings).")
        return

    url = f"https://api.github.com/repos/{repo}/releases/latest"
    try:
        data = http_get_json(url, timeout=int(CFG.get("github_check_timeout", 6)))
    except Exception as e:
        print("GitHub update check failed:", e)
        return

    latest_tag = (data.get("tag_name") or "").strip()
    latest_name = (data.get("name") or "").strip()
    html_url = (data.get("html_url") or "").strip()
    published = (data.get("published_at") or "").strip()

    if not latest_tag:
        print("No latest release found (tag_name empty).")
        return

    cur_t = ver_tuple(current_version)
    lat_t = ver_tuple(latest_tag)

    print("\n============= UPDATE =============")
    print("Repo:", repo)
    print("Current version:", current_version)
    print("Latest release :", latest_tag, (f"({latest_name})" if latest_name else ""))
    if published:
        print("Published     :", published)
    if html_url:
        print("Release page  :", html_url)

    if lat_t > cur_t:
        print("\n>>> UPDATE AVAILABLE")
        body = (data.get("body") or "").strip()
        if body:
            lines = body.splitlines()
            preview = "\n".join(lines[:10]).strip()
            if preview:
                print("\n--- Notes (preview) ---")
                print(preview)
                if len(lines) > 10:
                    print("... (truncated)")
    else:
        print("\n>>> You are up to date")

    print("==================================\n")


def load_config():
    cfg = dict(DEFAULT_CONFIG)
    if os.path.exists(CONFIG_PATH):
        try:
            with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                user = json.load(f)
            if isinstance(user, dict):
                cfg.update(user)
        except:
            pass
    return cfg

def save_config(cfg):
    try:
        with open(CONFIG_PATH, "w", encoding="utf-8") as f:
            json.dump(cfg, f, indent=2, ensure_ascii=False)
        return True
    except:
        return False

CFG = load_config()

LANG = (CFG.get("language") or "").strip().lower()
if LANG not in I18N:
    LANG = detect_system_lang()

def t(key, **kw):
    # safe fallback to EN if missing
    base = I18N.get(LANG, I18N["en"])
    s = base.get(key, I18N["en"].get(key, key))
    if kw:
        try:
            return s.format(**kw)
        except:
            return s
    return s

# -------------------- KND parsing helpers --------------------
def find_anchor(raw: bytes):
    anchors = [
        b"front_spring_way",
        b"mass",
        b"max_torque",
        b"turbo_pressure",
        b"final_drive",
    ]
    for a in anchors:
        idx = raw.find(a)
        if idx != -1:
            return idx, a
    return -1, None

# -------------------- PATH (auto detect) --------------------
def auto_find_tunes_dir():
    forced = (CFG.get("tunes_path") or "").strip().strip('"')
    if forced and os.path.exists(forced) and os.path.isdir(forced):
        return forced + ("\\" if not forced.endswith("\\") else "")

    # If tool is inside tunes or has "tunes" subfolder
    if os.path.basename(SCRIPT_DIR).lower() == "tunes":
        return SCRIPT_DIR + "\\"
    tunes_sub = os.path.join(SCRIPT_DIR, "tunes")
    if os.path.exists(tunes_sub) and os.path.isdir(tunes_sub):
        return tunes_sub + "\\"

    # Try common Steam locations on available drives
    drives = []
    for c in "CDEFGHIJKLMNOPQRSTUVWXYZ":
        root = c + ":\\"
        if os.path.exists(root):
            drives.append(root)

    candidates = [
        r"SteamLibrary\steamapps\common\CarX Drift Racing Online\kino\mods\KN_Base\tunes",
        r"Program Files (x86)\Steam\steamapps\common\CarX Drift Racing Online\kino\mods\KN_Base\tunes",
        r"Program Files\Steam\steamapps\common\CarX Drift Racing Online\kino\mods\KN_Base\tunes",
    ]

    for d in drives:
        for rel in candidates:
            p = os.path.join(d, rel)
            if os.path.exists(p) and os.path.isdir(p):
                return p + "\\"

    return SCRIPT_DIR + "\\"

baseDirectory = auto_find_tunes_dir()

# Output folders inside tunes dir
jsonOutDir = os.path.join(baseDirectory, "_knd_json") + "\\"
txtOutDir  = os.path.join(baseDirectory, "_knd_txt") + "\\"
outKndDir  = os.path.join(baseDirectory, "_knd_out") + "\\"
bakDir     = os.path.join(baseDirectory, "_backup") + "\\"

for d in (jsonOutDir, txtOutDir, outKndDir, bakDir):
    if not os.path.exists(d):
        os.makedirs(d, exist_ok=True)

def short_rel(path):
    try:
        return os.path.relpath(path, baseDirectory)
    except:
        return os.path.basename(path)

def backup_file(src):
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    name = os.path.splitext(os.path.basename(src))[0]
    dst = os.path.join(bakDir, f"{name}_{ts}.knd")
    shutil.copy2(src, dst)
    return dst

# -------------------- KND PARSER (sections) --------------------
def parse_knd_sections(src):
    raw = open(src, "rb").read()

    idx, anchor = find_anchor(raw)
    if idx < 0:
        raise Exception("Format inattendu: aucun anchor connu trouvé.")

    pos = idx - 1
    if pos < 0:
        raise Exception("Format inattendu: anchor trop proche du début.")

    section1 = []  # (key, off, val)
    section2 = []  # (key, off, val)
    refs = {}      # key -> list of (off, sec)

    def read_kv(p):
        if p >= len(raw):
            return None
        klen = raw[p]
        if klen == 0 or klen > 64:
            return None
        keyb = raw[p+1:p+1+klen]
        if len(keyb) != klen or b"\x00" in keyb or not KEY_RE.match(keyb):
            return None
        v_off = p + 1 + klen
        if v_off + 4 > len(raw):
            return None
        val = struct.unpack_from("<f", raw, v_off)[0]
        return keyb.decode("ascii"), v_off, val, v_off + 4

    # SECTION1 until marker 00 00 00 00 + count
    while True:
        if pos + 8 <= len(raw) and raw[pos:pos+4] == b"\x00\x00\x00\x00":
            count = struct.unpack_from("<I", raw, pos + 4)[0]
            pos += 8
            break

        res = read_kv(pos)
        if res is None:
            raise Exception("Parse échoué en SECTION1 (offset {}).".format(pos))
        k, off, val, pos = res
        section1.append((k, off, val))
        refs.setdefault(k, []).append((off, 1))

    # SECTION2: exactly <count> pairs
    for _ in range(count):
        res = read_kv(pos)
        if res is None:
            raise Exception("Parse échoué en SECTION2 (offset {}).".format(pos))
        k, off, val, pos = res
        section2.append((k, off, val))
        refs.setdefault(k, []).append((off, 2))

    return raw, section1, section2, anchor, count, refs

# -------------------- EXPORT --------------------
def export_json_sections(src):
    raw, s1, s2, anchor, count, refs = parse_knd_sections(src)
    name = os.path.splitext(os.path.basename(src))[0]
    out = os.path.join(jsonOutDir, name + ".json")

    data = {
        "file": os.path.basename(src),
        "anchor": anchor.decode("ascii") if anchor else None,
        "sections": {"section2_count": int(count)},
        "section1": {k: float(v) for (k, off, v) in s1},
        "section2": {k: float(v) for (k, off, v) in s2},
    }

    with open(out, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f'{t("export_json_ok")}: "{out}"')

def export_txt_sections(src):
    raw, s1, s2, anchor, count, refs = parse_knd_sections(src)
    name = os.path.splitext(os.path.basename(src))[0]
    out = os.path.join(txtOutDir, name + ".txt")

    with open(out, "w", encoding="utf-8") as f:
        f.write("# file: {}\n".format(os.path.basename(src)))
        f.write("# anchor: {}\n".format(anchor.decode("ascii") if anchor else "None"))
        f.write("# section2_count: {}\n\n".format(count))

        f.write("[SECTION1]\n")
        for (k, off, v) in s1:
            f.write("{}={}\n".format(k, v))

        f.write("\n[SECTION2]\n")
        for (k, off, v) in s2:
            f.write("{}={}\n".format(k, v))

    print(f'{t("export_txt_ok")}: "{out}"')

# -------------------- PATCH --------------------
def patch_from_json_sections(src_knd, src_json):
    raw, s1, s2, anchor, count, refs = parse_knd_sections(src_knd)
    barr = bytearray(raw)

    with open(src_json, "r", encoding="utf-8") as f:
        data = json.load(f)

    patch_s1 = yn(t("patch_s1"), CFG.get("default_patch_section1", True))
    patch_s2 = yn(t("patch_s2"), CFG.get("default_patch_section2", True))

    if yn(t("backup"), CFG.get("backup_before_patch", True)):
        b = backup_file(src_knd)
        print(f'{t("backup_done")}: "{b}"')

    s1_params = data.get("section1", {})
    s2_params = data.get("section2", {})

    patched = 0
    skipped = 0

    def apply(params, sec_id):
        nonlocal patched, skipped
        for k, v in params.items():
            found = False
            for (off, sec) in refs.get(k, []):
                if sec == sec_id:
                    try:
                        struct.pack_into("<f", barr, off, float(v))
                        patched += 1
                    except:
                        print('Valeur invalide pour "{}": {}'.format(k, v))
                    found = True
                    break
            if not found:
                skipped += 1

    if patch_s1:
        apply(s1_params, 1)
    if patch_s2:
        apply(s2_params, 2)

    base = os.path.splitext(os.path.basename(src_knd))[0]
    out = os.path.join(outKndDir, base + "_EDIT.knd")

    with open(out, "wb") as f:
        f.write(barr)

    print(f'{t("patch_ok")}: "{out}" ({t("patched")}={patched}, {t("ignored")}={skipped})')

# -------------------- SHOW / COMPARE --------------------
def list_knd_sections(src):
    raw, s1, s2, anchor, count, refs = parse_knd_sections(src)
    print("\n--- {} ---".format(os.path.basename(src)))
    print("Anchor:", anchor.decode("ascii") if anchor else "None")
    print("SECTION1:", len(s1), "params")
    print("SECTION2:", len(s2), f"params (count={count})")

    show = 25
    print("\n[SECTION1] (first {})".format(show))
    for i, (k, off, v) in enumerate(s1[:show], 1):
        print("  {:>2}) {} = {}".format(i, k, v))
    if len(s1) > show:
        print("  ... (+{} autres)".format(len(s1) - show))

    print("\n[SECTION2]")
    for i, (k, off, v) in enumerate(s2, 1):
        print("  {:>2}) {} = {}".format(i, k, v))
    print("")

def compare_knd(a_path, b_path):
    _, a1, a2, _, _, _ = parse_knd_sections(a_path)
    _, b1, b2, _, _, _ = parse_knd_sections(b_path)

    def to_dict(sec):
        d = {}
        for (k, off, v) in sec:
            d[k] = float(v)
        return d

    A1, A2 = to_dict(a1), to_dict(a2)
    B1, B2 = to_dict(b1), to_dict(b2)

    def diff_print(title, A, B):
        print("\n[" + title + "]")
        keys = sorted(set(A.keys()) | set(B.keys()))
        changed = 0
        for k in keys:
            va = A.get(k, None)
            vb = B.get(k, None)
            if va != vb:
                changed += 1
                delta = None if (va is None or vb is None) else (vb - va)
                print(f"{k}: {va} -> {vb} (delta={delta})")
        if changed == 0:
            print("Aucun changement." if LANG == "fr" else "No changes.")

    print("\n=== COMPARE ===")
    print("A:", short_rel(a_path))
    print("B:", short_rel(b_path))
    diff_print("SECTION1", A1, B1)
    diff_print("SECTION2", A2, B2)

# -------------------- SCAN --------------------
IGNORE_DIRS = {"_knd_json", "_knd_txt", "_knd_out", "_backup"}

def scanDir(srcDir, subpath, out_list):
    full = os.path.join(srcDir, subpath)
    with os.scandir(full) as it:
        for p in it:
            if p.is_dir():
                if p.name in IGNORE_DIRS:
                    continue
                if CFG.get("scan_recursive", True):
                    scanDir(srcDir, os.path.join(subpath, p.name), out_list)
            else:
                if p.name.lower().endswith(".knd"):
                    out_list.append(os.path.join(full, p.name))

def pick_file(files, title):
    print("\n" + title)
    for i, f in enumerate(files, 1):
        print("  {}) {}".format(i, short_rel(f)))
    while True:
        s = input("Numéro (ENTER=annuler): ").strip()
        if s == "":
            return None
        if s.isdigit():
            n = int(s)
            if 1 <= n <= len(files):
                return files[n-1]
        print("Choix invalide.")

# -------------------- SETTINGS --------------------
def settings_menu():
    global LANG, CFG, baseDirectory, jsonOutDir, txtOutDir, outKndDir, bakDir

    def apply_and_save():
        # apply language
        desired = (CFG.get("language") or "").strip().lower()
        if desired in ("auto", ""):
            CFG["language"] = ""

        if CFG.get("language"):
            lang = CFG.get("language").strip().lower()
            if lang in I18N:
                globals()["LANG"] = lang
            else:
                globals()["LANG"] = detect_system_lang()
                CFG["language"] = ""
        else:
            globals()["LANG"] = detect_system_lang()

        save_config(CFG)

        # refresh paths / output dirs
        globals()["baseDirectory"] = auto_find_tunes_dir()
        globals()["jsonOutDir"] = os.path.join(baseDirectory, "_knd_json") + "\\"
        globals()["txtOutDir"]  = os.path.join(baseDirectory, "_knd_txt") + "\\"
        globals()["outKndDir"]  = os.path.join(baseDirectory, "_knd_out") + "\\"
        globals()["bakDir"]     = os.path.join(baseDirectory, "_backup") + "\\"
        for d in (jsonOutDir, txtOutDir, outKndDir, bakDir):
            if not os.path.exists(d):
                os.makedirs(d, exist_ok=True)

    def show_main():
        os.system("cls")
        print(t("settings_title"))
        print(f"{t('settings_lang')}: {CFG.get('language') or 'Auto'} (active: {LANG})")
        print(f"{t('settings_path')}: {CFG.get('tunes_path') or 'Auto'}")
        print(f"{t('settings_defaults')}:")
        print(f" - {t('opt_patch_s1')}: {CFG.get('default_patch_section1', True)}")
        print(f" - {t('opt_patch_s2')}: {CFG.get('default_patch_section2', True)}")
        print(f" - {t('opt_backup')}: {CFG.get('backup_before_patch', True)}")
        print(f" - {t('opt_scanrec')}: {CFG.get('scan_recursive', True)}")
        print("")
        print(t("settings_menu_title"))
        print(f"1) {t('settings_item_language')}")
        print(f"2) {t('settings_item_path')}")
        print(f"3) {t('settings_item_defaults')}")
        print(f"4) {t('settings_item_update')} (GitHub)")
        print(f"5) {t('settings_item_changelog')}")
        print(f"6) {t('settings_item_credits')}")
        print(f"7) {t('settings_item_back')}")
        print("================================")

    while True:
        show_main()
        c = input(t("choice")).strip()
        if c in ("7", ""):
            return

        # 1) Language
        if c == "1":
            os.system("cls")
            print(f"=== {t('settings_item_language')} ===")
            print(t("lang_pick"))
            code = input("> ").strip().lower()
            if code == "":
                continue
            if code in ("auto", "off"):
                CFG["language"] = ""
                apply_and_save()
                print(t("saved"))
                pause()
                continue
            if code in I18N:
                CFG["language"] = code
                apply_and_save()
                print(t("saved"))
            else:
                print(t("invalid_lang_code"))
            pause()
            continue

        # 2) Tunes path
        if c == "2":
            os.system("cls")
            print(f"=== {t('settings_item_path')} ===")
            print(f"{t('current')}: {CFG.get('tunes_path') or 'Auto'}")
            print(t("enter_cancel_auto"))
            p = input(t("enter_path")).strip().strip('"')
            if p == "":
                continue
            if p.lower() in ("auto", "off"):
                CFG["tunes_path"] = ""
                apply_and_save()
                print(t("saved"))
                pause()
                continue
            if os.path.exists(p) and os.path.isdir(p):
                CFG["tunes_path"] = p
                apply_and_save()
                print(t("saved"))
            else:
                print(t("invalid_path"))
            pause()
            continue

        # 3) Default options
        if c == "3":
            while True:
                os.system("cls")
                print(f"=== {t('settings_item_defaults')} ===")
                print(f"1) {t('opt_patch_s1')}: {CFG.get('default_patch_section1', True)}")
                print(f"2) {t('opt_patch_s2')}: {CFG.get('default_patch_section2', True)}")
                print(f"3) {t('opt_backup')}: {CFG.get('backup_before_patch', True)}")
                print(f"4) {t('opt_scanrec')}: {CFG.get('scan_recursive', True)}")
                print(f"5) {t('settings_item_back')}")
                s = input(t("choice_1_5")).strip()
                if s in ("5", ""):
                    apply_and_save()
                    break
                if s == "1":
                    CFG["default_patch_section1"] = not CFG.get("default_patch_section1", True)
                elif s == "2":
                    CFG["default_patch_section2"] = not CFG.get("default_patch_section2", True)
                elif s == "3":
                    CFG["backup_before_patch"] = not CFG.get("backup_before_patch", True)
                elif s == "4":
                    CFG["scan_recursive"] = not CFG.get("scan_recursive", True)
                else:
                    print(t("invalid_choice"))
                    pause()
            print(t("saved"))
            pause()
            continue

        # 4) Update (GitHub)
        if c == "4":
            while True:
                os.system("cls")
                print(f"=== {t('settings_item_update')} (GitHub) ===")
                print(f"{t('update_repo')}: {CFG.get('github_repo') or 'OFF'}")
                print(f"1) {t('update_configure')}")
                print(f"2) {t('update_check')}")
                print(f"3) {t('settings_item_back')}")
                s = input(t("choice_1_3")).strip()
                if s in ("3", ""):
                    break
                if s == "1":
                    repo = input(t("update_set_repo_prompt")).strip()
                    CFG["github_repo"] = repo if repo else ""
                    apply_and_save()
                    print(t("saved"))
                    pause()
                elif s == "2":
                    apply_and_save()
                    if not (CFG.get("github_repo") or "").strip():
                        print(t("update_need_repo"))
                    else:
                        check_github_update(VER)
                    pause()
                else:
                    print(t("invalid_choice"))
                    pause()
            continue

        # 5) Changelog
        if c == "5":
            show_changelog()
            pause()
            continue

        # 6) Credits
        if c == "6":
            show_credits()
            pause()
            continue

        print(t("invalid_choice"))
        pause()


# -------------------- MAIN --------------------
VER = "1.0.1.5"

def rebuild_file_list():
    files = []
    scanDir(baseDirectory, "", files)
    return files

while True:
    os.system("cls")  # clear screen (Windows)
    print("=======================")
    print(t("title", ver=VER))
    print("=======================")
    print(t("folder") + ":", baseDirectory)

    kndFiles = rebuild_file_list()
    print(t("found_knd") + ":", len(kndFiles))

    if len(kndFiles) == 0:
        print(t("no_knd"))
        print(t("tip"))
        pause()
        break

    print("\n" + t("menu"))
    print(t("m1"))
    print(t("m2"))
    print(t("m3"))
    print(t("m4"))
    print(t("m5"))
    print(t("m6"))
    print(t("m7"))
    print("======================================")

    choice = input(t("choice")).strip()

    try:
        if choice == "1":
            if yn(t("export_all"), True):
                for f in kndFiles:
                    try:
                        export_json_sections(f)
                    except Exception as e:
                        print('ERREUR export JSON "{}": {}'.format(short_rel(f), e))
            else:
                f = pick_file(kndFiles, t("choose_knd_export_json"))
                if f:
                    export_json_sections(f)

        elif choice == "2":
            if yn(t("export_all"), True):
                for f in kndFiles:
                    try:
                        export_txt_sections(f)
                    except Exception as e:
                        print('ERREUR export TXT "{}": {}'.format(short_rel(f), e))
            else:
                f = pick_file(kndFiles, t("choose_knd_export_txt"))
                if f:
                    export_txt_sections(f)

        elif choice == "3":
            f = pick_file(kndFiles, t("choose_knd_patch"))
            if not f:
                print(t("cancel"))
            else:
                base = os.path.splitext(os.path.basename(f))[0]
                default_json = os.path.join(jsonOutDir, base + ".json")
                print("\n{}: {}".format(t("default_json"), default_json))

                if os.path.exists(default_json) and yn(t("use_default_json"), True):
                    patch_from_json_sections(f, default_json)
                else:
                    j = input(t("json_path")).strip().strip('"')
                    if j and os.path.exists(j):
                        patch_from_json_sections(f, j)
                    else:
                        print(t("json_missing"))

        elif choice == "4":
            f = pick_file(kndFiles, t("choose_knd_show"))
            if f:
                list_knd_sections(f)

        elif choice == "5":
            a = pick_file(kndFiles, t("choose_a"))
            if not a:
                print(t("cancel"))
            else:
                b = pick_file(kndFiles, t("choose_b"))
                if b:
                    compare_knd(a, b)

        elif choice == "6":
            settings_menu()
            # Si le user change le chemin tunes, on veut re-scan direct au prochain loop
            # (settings_menu() refresh deja baseDirectory et les out dirs)

        elif choice == "7":
            print(t("bye"))
            break

        else:
            print("Choix invalide.")
    except Exception as e:
        print("ERREUR:", e)

    pause()
