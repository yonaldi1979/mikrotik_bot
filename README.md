# Mikrotik Telegram Bot

Bot Telegram untuk mengelola perangkat Mikrotik melalui Telegram. Bot ini mendukung beberapa fitur seperti:
- Manajemen PPPoE user (add dan delete)
- Manajemen IP Address (add dan delete)
- Manajemen Firewall (add dan delete rule)
- Mikrotik Bot ini butuh pengembangan lebih lanjut dari komunitas github, dan sangat jauh dari kata sempurna.

---

## ⚙️ Instalasi

1. Clone repository ini:

    ```bash
    git clone https://github.com/yonaldi1979/mikrotik_bot.git
    cd mikrotik_bot
    ```

2. Buat virtual environment (opsional tapi disarankan):

    ```bash
    python3 -m venv venv
    source venv/bin/activate   # Linux/macOS
    .\venv\Scripts\activate    # Windows
    ```

3. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

4. Konfigurasi bot dan Mikrotik di `config.py`.

5. Jalankan bot:

    ```bash
    python bot.py
    ```

---
## 🔗 Konfigurasi (config.py)

Pastikan file `config.py` berisi:

```python
BOT_TOKEN = "TOKEN_BOT_TELEGRAM"
MIKROTIK_HOST = "192.168.88.1"
MIKROTIK_USERNAME = "admin"
MIKROTIK_PASSWORD = "password"
ADMIN_IDS = [123456789]  # List Telegram User ID yang diizinkan
GROUP_IDS = [-123456789]  # List Group ID yang diizinkan

Perintah	Deskripsi
/start	Menampilkan pesan selamat datang
/help	Menampilkan daftar perintah
/addpppoe	Menambahkan user PPPoE
/delpppoe	Menghapus user PPPoE
/addip	Menambahkan IP Address
/delip	Menghapus IP Address
/addfirewall	Menambahkan rule firewall
/delfirewall	Menghapus rule firewall


---

## 📄 requirements.txt

```text
python-telegram-bot==20.7
librouteros==3.0.0

Catatan
Pastikan python-telegram-bot versi 20 ke atas, karena struktur Application dan CommandHandler sudah pakai versi baru.
librouteros untuk koneksi ke Mikrotik via API.
Kalau nanti ada tambahan fitur (misal BGP atau DHCP), tinggal tambahin aja handler baru di folder commands.


Service Systemd :
nano /etc/systemd/system/mikrotik_bot.service
[Unit]
Description=Telegram Mikrotik Bot Service
After=network.target

[Service]
WorkingDirectory=/opt/mikrotik_bot
ExecStart=/usr/bin/python3 /opt/mikrotik_bot/bot.py
Restart=always
User=root
StandardOutput=syslog
StandardError=syslog
SyslogIdentifier=mikrotik_bot

[Install]
WantedBy=multi-user.target

Sesuaikan PATH dengan folder project masing-masing.


  
