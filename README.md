<div align="center">

# World War Bot
# 🌍⚔️

### A Persian Rubika Strategy Game of Nations

An asynchronous world-strategy bot for Rubika: players choose a country, build an economy, raise an army, trade, form alliances, and compete on a shared board — with saved JSON state and a keypad interface.

<br>

# 👨‍💻 **Sadra Hatami**

### *Developer • Software Engineer • Creator*

<br>

[![Python](https://img.shields.io/badge/Python-3.8%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Rubka](https://img.shields.io/badge/Rubka-Rubika%20Bot-8E44AD?style=for-the-badge)](https://pypi.org/)
[![AsyncIO](https://img.shields.io/badge/AsyncIO-Asynchronous-2C3E50?style=for-the-badge&logo=python&logoColor=white)](https://docs.python.org/3/library/asyncio.html)
[![JSON](https://img.shields.io/badge/Storage-JSON-003B57?style=for-the-badge)](#-architecture)
[![Strategy](https://img.shields.io/badge/Genre-Strategy-C0392B?style=for-the-badge)](#-key-features)
[![Persian](https://img.shields.io/badge/Language-Persian-success?style=for-the-badge)](https://en.wikipedia.org/wiki/Persian_language)
[![License](https://img.shields.io/badge/License-MIT-green.svg?style=for-the-badge)](LICENSE)
![Open Source](https://img.shields.io/badge/Open_Source-Project-black?style=for-the-badge&logo=github)

<br>

[🌐 GitHub Profile](https://github.com/sadra-hatami)
•
[📘 نسخه فارسی راهنما](README.fa.md)
•
[📧 Email](mailto:sadra.hatami.1732@gmail.com)

</div>

---

# 📑 Table of Contents

- [About](#-about)
- [Related Repositories](#-related-repositories)
- [Why This Project?](#-why-this-project)
- [Key Features](#-key-features)
- [Architecture](#-architecture)
- [Project Structure](#-project-structure)
- [Technologies](#️-technologies)
- [Installation](#-installation)
- [Configuration](#️-configuration)
- [Usage](#️-usage)
- [Target Audience](#-target-audience)
- [Roadmap](#️-roadmap)
- [FAQ](#-faq)
- [Contributing](#-contributing)
- [Contact](#-contact)
- [License](#-license)
- [Copyright](#-copyright)
- [Support](#-support)

---

# 📖 About

**World War Bot** is a Persian strategy game for Rubika.

A player picks a server, a continent, and a country. From the keypad they manage resources, buildings, research, and an army, then meet other players through diplomacy, trade, alliances, and rankings. Daily rewards, invites, statements, and a chance wheel keep the session alive between visits.

The application is one asynchronous file, `bot.py`, built with `rubka`. Game state is a `GameDB` layer that loads and writes JSON files under `war_game_v3/`.

> **Tagline:** *A Persian Rubika strategy bot where players lead a nation, grow an economy, and compete in a shared world.*

---

# 🔗 Related Repositories

| Repository | Role |
|------------|------|
| **[World War Bot](https://github.com/sadra-hatami/World-War-Bot)** | World strategy game (this repo) |
| **[Countries War Bot](https://github.com/sadra-hatami/Countries-War-Bot)** | Earlier nation strategy game |
| **[Rubika Group Bot](https://github.com/sadra-hatami/Rubika-Group-Bot)** | Complete group platform |
| **[Rubika Advanced Group Bot](https://github.com/sadra-hatami/Rubika-Advanced-Group-Bot)** | Newest, larger group platform |
| **[Telegram Rubika Account Panel](https://github.com/sadra-hatami/Telegram-Rubika-Account-Panel)** | Telegram panel for a Rubika user account |

Use this repository for the world strategy game.  
Use **Countries War Bot** for the earlier country game.  
Use the group bots for moderation and automation.  
Use the **Account Panel** only to control a user account from Telegram.

---

# 🚀 Why This Project?

A chat bot can answer one command. A strategy bot has to remember a country.

This project keeps a shared world:

- Every player owns a named nation
- Economy, buildings, and research change over time
- Diplomacy, trade, and alliances connect players
- Rankings and daily rewards pull people back
- JSON saves survive a restart

It shows how a Rubika bot can carry a full game loop, not only a help menu.

---

# ✨ Key Features

- 🌍 Server, continent, and country selection
- 🏛️ Country profile and resources
- ⚔️ Army menu and military actions
- 🏗️ Buildings and upgrades
- 🛒 Market, exchange, and trade offers
- 🤝 Diplomacy, alliances, and ally chat
- 🔬 Research
- 🕵️ Intelligence actions
- 🏆 World ranking
- 🎖️ Achievements
- 🎁 Daily bonus and invite codes
- 🎲 Lucky wheel
- 🌐 Shared institutions and public statements
- 🎛️ Persian keypad interface
- 🛡️ Operator panel for the running instance
- 💾 JSON save folder `war_game_v3/`

---

# 🏗️ Architecture

```text
Player
 └─ Rubika chat + keypads
     └─ bot.py
         └─ GameDB
             └─ war_game_v3/*.json
```

Button IDs route into country, army, market, diplomacy, research, and ranking flows. `GameDB.save()` writes the in-memory world back to disk. Secrets belong in environment variables, not in the source file.

---

# 📁 Project Structure

```text
World-War-Bot/
├── bot.py
├── war_game_v3/     # created at runtime — do not commit
└── README.md
```

`bot.py` is the application. The JSON folder holds players, taken countries, market prices, alliances, trade, statements, invites, and logs.

---

# 🛠️ Technologies

- Python 3.8+
- `rubka` (`Robot`, `Message`, `ChatKeypadBuilder`)
- asyncio
- JSON persistence

---

# 🚀 Installation

```bash
git clone https://github.com/sadra-hatami/World-War-Bot.git
cd World-War-Bot
pip install rubka
```

```bash
python bot.py
```

---

# ⚙️ Configuration

```text
RUBIKA_BOT_TOKEN
RUBIKA_ADMIN_IDS
```

`.gitignore`:

```text
.env
war_game_v3/
__pycache__/
```

---

# ▶️ Usage

1. Put the token in the environment.
2. Run `bot.py`.
3. Open the bot in Rubika.
4. Choose a server and a country.
5. Use the keypad for army, market, diplomacy, research, and rank.

The operator panel opens from the private command `پنل`.

---

# 🎓 Target Audience

- Rubika communities that want a long strategy session
- Developers studying a large keypad-driven game bot
- Students building a games portfolio

---

# 🗺️ Roadmap

- Split systems into packages
- Clearer notes per menu
- Safer default configuration
- Optional database backend

---

# ❓ FAQ

### Is this a group lock bot?

No. Group tools live in [Rubika Group Bot](https://github.com/sadra-hatami/Rubika-Group-Bot) and [Rubika Advanced Group Bot](https://github.com/sadra-hatami/Rubika-Advanced-Group-Bot).

### How is this different from Countries War Bot?

[Countries War Bot](https://github.com/sadra-hatami/Countries-War-Bot) is the earlier nation game. This repository is the world-strategy build: servers, continents, market, diplomacy, research, invites, and a shared board.

### Does progress survive a restart?

Yes, when the `war_game_v3/` folder stays on disk.

### Can the token be published?

No. Use an environment variable only.

---

# 🤝 Contributing

Bug reports, menu polish, and safer configuration are welcome.

---

# 📬 Contact

**Developer:**

### Sadra Hatami

📧 [Email](mailto:sadra.hatami.1732@gmail.com)

🌐 [GitHub](https://github.com/sadra-hatami)

---

# 📄 License

This project is licensed under the **MIT License**.

---

# © Copyright

© 2026 **Sadra Hatami**

All rights reserved.

---

# ⭐ Support

If this bot belongs in a portfolio or a community, please consider giving it a ⭐ on GitHub.

---

<div align="center">

## Designed & Developed with ❤️ for the developer community of Iran and the world by **Sadra Hatami**

</div>
