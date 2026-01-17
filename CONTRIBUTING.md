# Contributing / Contribuer

- 🇫🇷 Aller à : [Français](#-français)
- 🇬🇧 Go to : [English](#-english)

---

## 🇫🇷 Français

Merci de contribuer à **KND-Tool** 🙌

### ✅ Avant de créer un ticket (Issue)
- **Bug** : utilise le template **Bug report**
- **Idée / Feature** : utilise **Feature request**
- **Question / Aide** : préfère **Discussions** (Support / Q&A)

> Astuce : ajoute un screenshot / log console quand c'est possible.

### 🧪 Reproduire / Tester
Quand tu proposes une modif, essaye de fournir :
- Étapes pour reproduire
- Exemple de fichier `.knd` (si possible **sans** contenu protégé/illégal)
- Résultat attendu vs résultat actuel

### 🧱 Style & bonnes pratiques
- Reste simple : c'est un tool CLI, on évite les dépendances inutiles.
- Garde la compatibilité Windows en priorité.
- Les textes UI doivent passer par le dictionnaire **I18N**.
- Évite de casser la config (`knd_tool_config.json`).

### 🌍 Traductions
- Ne change pas les **keys** (ex: `menu`, `choice`, `settings_title`…)
- Si une langue manque une clé, garde l'anglais en fallback.

### 🧷 Pull Requests
- 1 PR = 1 sujet (bugfix OU feature OU doc)
- Explique comment tester
- Si tu touches aux releases / versions : incrémente proprement la version et mets à jour le changelog

---

## 🇬🇧 English

Thanks for contributing to **KND-Tool** 🙌

### ✅ Before opening an Issue
- **Bug**: use the **Bug report** template
- **Idea / Feature**: use **Feature request**
- **Question / Help**: please use **Discussions** (Support / Q&A)

> Tip: add screenshots / console logs whenever possible.

### 🧪 Reproduce / Test
When proposing changes, please provide:
- Steps to reproduce
- Example `.knd` (when possible, without copyrighted/protected content)
- Expected result vs actual result

### 🧱 Style & best practices
- Keep it simple: CLI tool, avoid unnecessary dependencies.
- Windows compatibility is the priority.
- UI strings must go through the **I18N** dictionary.
- Do not break config (`knd_tool_config.json`).

### 🌍 Translations
- Do not rename existing **keys** (e.g. `menu`, `choice`, `settings_title`…)
- If a language misses a key, keep English as a fallback.

### 🧷 Pull Requests
- 1 PR = 1 topic (bugfix OR feature OR docs)
- Explain how to test
- If you touch releases / versions: bump version properly and update the changelog
