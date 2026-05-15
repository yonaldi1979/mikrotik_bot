## Cursor Cloud specific instructions

### Ringkasan

Bot Telegram berbasis Python untuk mengelola router MikroTik. Memiliki dua dependency utama: `python-telegram-bot` (v20.7) dan `routeros-api` (v0.17.0).

### Hal Penting yang Perlu Diperhatikan

- **README menyebut `librouteros`, tapi kode menggunakan `routeros_api`.** Ini adalah package PyPI yang berbeda. Package yang benar adalah `routeros-api` (di-import sebagai `routeros_api`). JANGAN install `librouteros`.
- **Tidak ada test di repo ini.** Validasi perubahan menggunakan `py_compile` dan `pyflakes` untuk pengecekan syntax/import.
- **Credentials di-hardcode.** Token Telegram ada di `bot.py` (baris 10) dan credentials router ada di `config.py`. Keduanya harus diganti dengan nilai asli agar bot bisa berjalan.
- Bot membutuhkan **dua layanan eksternal** untuk berjalan: Telegram Bot API (internet + token valid) dan router MikroTik dengan API aktif di port 8728.

### Menjalankan Bot

```bash
source venv/bin/activate
python bot.py
```

Bot akan mencetak "Bot is running..." lalu mulai polling ke Telegram API. Bot akan gagal dengan error `InvalidToken` jika token di `bot.py` masih placeholder.

### Lint Check

```bash
source venv/bin/activate
python -m pyflakes bot.py config.py mikrotik_api.py commands/*.py
```

Catatan: `bot.py` memiliki dua warning lint (unused import `ADMIN_IDS` dan `GROUP_IDS`) — ini sudah ada sejak awal di repo.

### Pengecekan Syntax/Compile

```bash
source venv/bin/activate
python -m py_compile <file.py>
```
