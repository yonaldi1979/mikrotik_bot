# AGENTS.md

## Cursor Cloud specific instructions

### Project overview

This is a Python Telegram bot for managing MikroTik routers via chat commands. See `README.md` for the full feature list and setup instructions (in Indonesian).

### Key dependencies

- `python-telegram-bot==20.7` — Telegram bot framework (async)
- `RouterOS-api` — MikroTik RouterOS API client (note: the README incorrectly references `librouteros`, but the code uses `routeros_api` from the `RouterOS-api` package)

Install with: `pip install -r requirements.txt`

### Running the bot

```bash
python bot.py
```

The bot requires a valid Telegram bot token. The token is hardcoded in `bot.py` (line 10, variable `TOKEN`). For development, replace the placeholder `'TELEGRAM_TOKEN'` with a real token from @BotFather, or set it via an environment variable if the code is updated to support that.

MikroTik router credentials are configured in `config.py`. A real or emulated MikroTik device must be reachable for command handlers to function.

### Linting

```bash
flake8 --max-line-length=120 *.py commands/*.py
```

The existing codebase has style issues (unused imports, spacing); these are pre-existing.

### Important caveats

- There are no automated tests in this repository.
- The `commands/` directory has no `__init__.py`; Python finds it via implicit namespace packages.
- `bot.py` imports `ADMIN_IDS` and `GROUP_IDS` from `config` but does not use them directly — they are used inside each command handler module.
- The `delete_firewall_rule` method in `mikrotik_api.py` accepts `(table, rule_id)`, but `commands/firewall.py` calls it with `(table, chain, src_address, dst_address, protocol)` — this is a known bug in the codebase.
