# KND-Tool (Kino) 🚗💨

[![Platform](https://img.shields.io/badge/platform-Windows-0078D6?logo=windows&logoColor=white)](#)
[![Python](https://img.shields.io/badge/python-3.9%2B-3776AB?logo=python&logoColor=white)](#)
[![License: GPL v3](https://img.shields.io/badge/license-GPLv3-blue.svg)](LICENSE)

**CarX Drift Racing Online (Kino) .knd tune tool:** export **JSON/TXT**, patch back to **.knd**, **diff**, **backups**, **multilingual UI** + **update checker**.

---

## 🇫🇷 Présentation

**KND-Tool** est un outil simple et rapide pour travailler sur les fichiers **`.knd`** (tunes) utilisés par **Kino** dans *CarX Drift Racing Online*.

✅ Exporter un `.knd` en **JSON** ou **TXT**  
✅ Modifier les valeurs facilement (VSCode / Notepad++ / etc.)  
✅ Repatcher vers un `.knd` (`_EDIT.knd`) avec **backup automatique**  
✅ Comparer deux tunes (**diff**)  
✅ Interface **multi-langues** : FR / EN / DE / RU / ZH / JA / IT / ES / PT  
✅ Option **Update checker GitHub** (via **Releases**)  

---

## 🇬🇧 Overview

**KND-Tool** is a lightweight utility to handle **`.knd`** tune files used by **Kino** in *CarX Drift Racing Online*.

✅ Export `.knd` to **JSON** or **TXT**  
✅ Edit values easily (in any text editor)  
✅ Patch back into `.knd` (`_EDIT.knd`) with **automatic backups**  
✅ Compare two tunes (**diff**)  
✅ **Multilingual UI**: FR / EN / DE / RU / ZH / JA / IT / ES / PT  
✅ Optional **GitHub update checker** (via **Releases**)  

---

## 📦 Download

- Recommended: use **Releases** on GitHub to download the latest version.
- You can also download the `.py` file directly from the repository.

> ⚠️ The update checker works **only** if the configured repository publishes **GitHub Releases**.

---

## ✅ Requirements

- **Windows** (recommended)
- **Python 3.9+** (tested on 3.11)
- No external modules required (standard library only)

---

## 🚀 Installation & Run

### Easy method (recommended)
1. Download the `.py`
2. Put it anywhere (**Desktop**, mods folder, etc.)
3. Double-click (or right-click → *Open with Python*)

### Command line
```bash
python "KND Tool 1.0.1.5.py"
```

> Tip: If Windows asks for an app, install Python from the Microsoft Store or python.org and check “Add to PATH”.

---

## 📁 Auto-detect `tunes` folder

KND-Tool tries to auto-detect:
```
...\CarX Drift Racing Online\kino\mods\KN_Base\tunes
```

If CarX is installed on another drive (E:\, D:\, etc.), it should still work.

If it doesn’t find it:
- **Settings** → **Tunes path** → paste the full path

Example:
```
E:\SteamLibrary\steamapps\common\CarX Drift Racing Online\kino\mods\KN_Base\tunes
```

---

## 🧭 Features

### 1) Export KND → JSON (sections)
- Exports a `.json` into `_knd_json`
- Values are handled by sections (**SECTION1 / SECTION2**) when the format allows

### 2) Export KND → TXT (sections)
- Exports a `.txt` into `_knd_txt`
- Great for quick reading / sharing

### 3) JSON → KND (patch) → `_EDIT.knd`
- Applies a `.json` on a `.knd`
- Output in `_knd_out` with suffix **`_EDIT.knd`**
- Optional backup in `_backup`

### 4) Show KND parameters
- Prints parameters and values to the console

### 5) Compare 2 KND (diff)
- Compare A vs B
- Shows only changed values

---

## 🗂️ Generated folders

The tool automatically creates:
```
tunes/
  _knd_json/   -> JSON exports
  _knd_txt/    -> TXT exports
  _knd_out/    -> patched files (_EDIT.knd)
  _backup/     -> backups before patch
```

---

## ⚙️ Settings (in-tool)

In **Settings**, you can:
- Change **language**
- Set **tunes path**
- Default options:
  - patch SECTION1 / SECTION2
  - backup before patch
  - recursive scan
- **Update (GitHub)**:
  - set repo `USER/REPO`
  - check updates via `Releases/latest`
- Show **Changelog** and **Credits**

All settings are stored in:
```
knd_tool_config.json
```

---

## 🔄 Update Checker (GitHub)

The tool can check if a **new version** is available using **GitHub Releases**.

### ✅ Official repository (recommended)
In **Settings → Update (GitHub)** set:
```
iMoDzF4N4TiK/KND-Tool
```

### 🧑‍🔧 If you use a fork (your own repo)
If you forked the project, set your own repository instead:
```
YOUR_USER/KND-Tool
```

### 📌 Important
The update checker works **only** if the configured repository publishes **Releases**.

Create a GitHub Release with a tag like:
- `1.0.1.5`
- or `v1.0.1.5`

---

## 🛟 FAQ

### “I see values > 1.0 (example 2.0) in JSON. Is it normal?”
Yes: the tool can write any float value.  
**But** in-game behavior depends on what CarX/Kino actually accepts.

### “Update checker says OFF”
You didn’t configure `github_repo` in Settings, or the selected repo has no Releases.

### “Can I break my tune?”
Yes if you patch extreme values.  
👉 Keep **backup** enabled so you can restore quickly.

---

## 🗺️ Roadmap (ideas)
- Export diff report to `.txt` / `.json`
- Presets (Stock / Semi / Max) with multipliers
- Categories (Suspension / Engine / Transmission / Weight)
- Optional GUI (if requested)

---

## 🤝 Contributing
- Bugs / ideas: use **Issues**
- PRs are welcome if the tool stays simple and stable

---

## 👑 Credits
**Author:** ιMσDzF4Π4ΤιK  
Thanks:
- CarX community modders  
- Testers / users  

---

## 📜 License
This project is licensed under the **GNU GPL v3.0**.  
See: [LICENSE](LICENSE)
