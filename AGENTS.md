## Cursor Cloud specific instructions

### Overview
This is a Python Telegram bot for managing MikroTik routers. It has two runtime dependencies: `python-telegram-bot` (v20.7) and `routeros-api` (v0.17.0).

### Key gotchas

- **README says `librouteros`; code uses `routeros_api`.** These are different PyPI packages. The correct package is `routeros-api` (installs as `routeros_api`). Do NOT install `librouteros`.
- **No tests exist in the repo.** Validate changes with `py_compile` and `pyflakes` for syntax/import checks.
- **Hardcoded credentials.** The Telegram token is in `bot.py` (line 10) and router credentials are in `config.py`. Both must be replaced with real values for the bot to function.
- The bot requires **two external services** to run end-to-end: Telegram Bot API (internet + valid token) and a MikroTik router with API enabled on port 8728.

### Running the bot

```bash
source venv/bin/activate
python bot.py
```

The bot prints "Bot is running..." then starts polling the Telegram API. It will fail with `InvalidToken` if the token in `bot.py` is still the placeholder.

### Lint checks

```bash
source venv/bin/activate
python -m pyflakes bot.py config.py mikrotik_api.py commands/*.py
```

Note: `bot.py` has two existing lint warnings (unused imports of `ADMIN_IDS` and `GROUP_IDS`) — these are pre-existing in the repo.

### Syntax/compile checks

```bash
source venv/bin/activate
python -m py_compile <file.py>
```
