# KND-Tool (Kino) 🚗💨

<p align="center">
  <img src="https://github.com/iMoDzF4N4T1K/KND-Tool/blob/3f0817668080c411e156ae6616a3c12f011ede62/KNTool.png" />
</p>

[![Platform](https://img.shields.io/badge/platform-Windows-0078D6?logo=windows&logoColor=white)](#)
[![Python](https://img.shields.io/badge/python-3.9%2B-3776AB?logo=python&logoColor=white)](#)
[![License: GPL v3](https://img.shields.io/badge/license-GPLv3-blue.svg)](LICENSE)

**CarX Drift Racing Online (Kino) .knd tune tool:** export **JSON/TXT**, patch back to **.knd**, **diff**, **backups**, **multilingual UI** + **update checker**.

---

## 🌍 Language / Langue

- 🇫🇷 **Français** → [Aller à la section FR](#-français)
- 🇬🇧 **English** → [Go to EN section](#-english)

---

# 🇫🇷 Français

## 🧭 Sommaire
- [Présentation](#-présentation)
- [Téléchargement](#-téléchargement)
- [Prérequis](#-prérequis)
- [Installation & Lancement](#-installation--lancement)
- [Auto-détection du dossier tunes](#-auto-détection-du-dossier-tunes)
- [Fonctions](#-fonctions)
- [Paramètres](#-paramètres)
- [Update Checker GitHub](#-update-checker-github)
- [Dossiers générés](#-dossiers-générés)
- [FAQ](#-faq)
- [Roadmap](#-roadmap)
- [Contribuer](#-contribuer)
- [Crédits](#-crédits)
- [Licence](#-licence)

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

## 📦 Téléchargement

- Recommandé : utilise **Releases** sur GitHub pour télécharger la dernière version.
- Tu peux aussi télécharger le `.py` directement depuis le repo.

> ⚠️ L’update checker fonctionne **uniquement** si le repo configuré publie des **Releases GitHub**.

---

## ✅ Prérequis

- **Windows** (recommandé)
- **Python 3.9+** (testé sur 3.11)
- Aucun module externe requis (standard library uniquement)

---

## 🚀 Installation & Lancement

### Méthode simple (recommandée)
1. Télécharge le script `.py`
2. Mets-le où tu veux (**Bureau**, dossier mods, etc.)
3. Double-clic (ou clic droit → *Ouvrir avec Python*)

### Via console
```bash
python "KND Tool 1.0.1.5.py"
```

---

## 📁 Auto-détection du dossier tunes

KND-Tool essaie de retrouver automatiquement :
```
...\CarX Drift Racing Online\kino\mods\KN_Base\tunes
```

Si CarX est installé sur un autre disque (E:\, D:\, etc.), ça marche aussi.

Si jamais ça ne trouve pas :
- **Paramètres** → **Chemin tunes** → colle le chemin complet

Exemple :
```
E:\SteamLibrary\steamapps\common\CarX Drift Racing Online\kino\mods\KN_Base\tunes
```

---

## 🧭 Fonctions

### 1) Exporter KND → JSON (sections)
- Exporte un `.json` dans `_knd_json`
- Les valeurs sont gérées par sections (**SECTION1 / SECTION2**) quand le format le permet

### 2) Exporter KND → TXT (sections)
- Exporte un `.txt` dans `_knd_txt`
- Parfait pour lire vite / partager

### 3) JSON → KND (patch) → `_EDIT.knd`
- Applique les valeurs d’un `.json` sur un `.knd`
- Sortie dans `_knd_out` avec suffixe **`_EDIT.knd`**
- Option **backup** dans `_backup`

### 4) Afficher paramètres d’un KND
- Affiche les paramètres et valeurs dans la console

### 5) Comparer 2 KND (diff)
- Compare A vs B
- Affiche uniquement ce qui change

---

## ⚙️ Paramètres

Dans **Paramètres**, tu peux :
- changer la **langue**
- définir le **chemin tunes**
- régler les options par défaut :
  - patch SECTION1 / SECTION2
  - backup avant patch
  - scan récursif
- **Update (GitHub)** :
  - configurer `USER/REPO`
  - vérifier une mise à jour via `Releases/latest`
- afficher **Changelog** et **Crédits**

Tout est sauvegardé dans :
```
knd_tool_config.json
```

---

## 🔄 Update Checker GitHub

Le tool peut vérifier si une **nouvelle version** est disponible via les **Releases GitHub**.

### ✅ Repo officiel (recommandé)
Dans **Paramètres → Update (GitHub)**, mets :
```
iMoDzF4N4TiK/KND-Tool
```

### 🧑‍🔧 Si tu utilises un fork (ton propre repo)
Si tu as fork le projet sur ton compte, remplace par ton repo :
```
TON_USER/KND-Tool
```

### 📌 Important
L’update checker fonctionne **uniquement** si le repo configuré publie des **Releases**.  
Crée une Release avec un tag du style :
- `1.0.1.5`
- ou `v1.0.1.5`

---

## 🧩 Dossiers générés

Le tool crée automatiquement :
```
tunes/
  _knd_json/   -> exports JSON
  _knd_txt/    -> exports TXT
  _knd_out/    -> fichiers patchés (_EDIT.knd)
  _backup/     -> backups avant patch
```

---

## 🛟 FAQ

### “Je vois des valeurs > 1.0 (ex: 2.0) dans mon JSON, c’est normal ?”
Oui : le tool peut écrire n’importe quelle valeur float.  
**Mais** le comportement en jeu dépend de ce que CarX/Kino accepte réellement.

### “Pourquoi mon update checker dit OFF ?”
Tu n’as pas configuré `github_repo` dans Paramètres, ou tu n’as pas de Releases.

### “Je peux casser mon tune ?”
Oui si tu patches des valeurs extrêmes.  
👉 Active **backup** (recommandé) pour pouvoir revenir en arrière.

---

## 🗺️ Roadmap
- Export rapport diff en `.txt` / `.json`
- Profils (Stock / Semi / Max) avec multiplicateurs
- Catégories par onglets (Suspension/Moteur/Transmission/Poids)
- GUI (optionnel) si demandé

---

## 🤝 Contribuer
- Bugs / suggestions : onglet **Issues**
- PR : bienvenue si ça garde le tool simple et stable

---

## 👑 Crédits
**Author:** ιMσDzF4Π4ΤιK  
Thanks:
- CarX community modders  
- Testers / users  

---

## 📜 Licence
This project is licensed under the **GNU GPL v3.0**.  
See: [LICENSE](LICENSE)

---

# 🇬🇧 English

## 🧭 Table of Contents
- [Overview](#-overview)
- [Download](#-download)
- [Requirements](#-requirements)
- [Install & Run](#-install--run)
- [Auto-detect tunes folder](#-auto-detect-tunes-folder)
- [Features](#-features)
- [Settings](#-settings)
- [GitHub Update Checker](#-github-update-checker)
- [Generated folders](#-generated-folders)
- [FAQ](#-faq-1)
- [Roadmap](#-roadmap-1)
- [Contributing](#-contributing)
- [Credits](#-credits)
- [License](#-license)

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

- Recommended: use **GitHub Releases** to download the latest version.
- You can also download the `.py` directly from the repository.

> ⚠️ The update checker works **only** if the configured repo publishes **GitHub Releases**.

---

## ✅ Requirements

- **Windows** (recommended)
- **Python 3.9+** (tested on 3.11)
- No external modules required (standard library only)

---

## 🚀 Install & Run

### Easy method (recommended)
1. Download the `.py`
2. Put it anywhere (**Desktop**, mods folder, etc.)
3. Double-click (or right-click → *Open with Python*)

### Command line
```bash
python "KND Tool 1.0.1.5.py"
```

---

## 📁 Auto-detect tunes folder

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

## ⚙️ Settings

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

## 🔄 GitHub Update Checker

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
The update checker works **only** if the configured repo publishes **Releases**.

Create a GitHub Release with a tag like:
- `1.0.1.5`
- or `v1.0.1.5`

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

## 🗺️ Roadmap
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
