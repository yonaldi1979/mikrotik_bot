# Mikrotik Telegram Bot

Bot Telegram untuk mengelola perangkat Mikrotik melalui Telegram. Bot ini mendukung beberapa fitur seperti:

- Manajemen PPPoE user (add dan delete)
- Manajemen IP Address (add dan delete)
- Manajemen Firewall (add dan delete rule)

> **Catatan:** Mikrotik Bot ini butuh pengembangan lebih lanjut dari komunitas GitHub, dan sangat jauh dari kata sempurna.

---

## 📋 Prasyarat

Sebelum menggunakan bot ini, pastikan kamu sudah menyiapkan:

- **Python 3.8+** (disarankan Python 3.10 ke atas)
- **Telegram Bot Token** — buat bot baru melalui [@BotFather](https://t.me/BotFather) di Telegram
- **Mikrotik Router** dengan API service yang sudah diaktifkan (port default: 8728)
- **Telegram User ID** dan **Group ID** yang akan digunakan untuk mengontrol bot

### Cara Mengaktifkan API di Mikrotik

1. Login ke Mikrotik via Winbox atau terminal.
2. Buka menu **IP > Services**.
3. Pastikan service **api** (port 8728) dalam status **enabled**.
4. Buat user khusus untuk bot dengan hak akses yang sesuai:

    ```
    /user add name=apibot password=passwdapi123 group=full
    ```

### Cara Mendapatkan Telegram User ID dan Group ID

- Kirim pesan ke [@userinfobot](https://t.me/userinfobot) untuk mendapatkan **User ID** kamu.
- Untuk **Group ID**, tambahkan [@RawDataBot](https://t.me/RawDataBot) ke group, lalu lihat field `chat.id` pada pesan yang dikirim bot tersebut.

---

## 📁 Struktur Proyek

```
mikrotik_bot/
├── bot.py                  # Entry point utama, setup bot dan register handler
├── config.py               # Konfigurasi koneksi Mikrotik dan whitelist admin/group
├── mikrotik_api.py         # Wrapper class untuk komunikasi ke Mikrotik via API
├── commands/
│   ├── pppoe.py            # Handler untuk /addpppoe dan /delpppoe
│   ├── del_pppoe.py        # Handler alternatif untuk /delpppoe
│   ├── ip_address.py       # Handler untuk /addip dan /delip
│   └── firewall.py         # Handler untuk /addfirewall dan /delfirewall
├── requirements.txt        # Daftar dependency Python
├── LICENSE                 # Lisensi MIT
└── README.md               # Dokumentasi proyek
```

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

4. Konfigurasi bot dan Mikrotik (lihat bagian [Konfigurasi](#-konfigurasi) di bawah).

5. Jalankan bot:

    ```bash
    python bot.py
    ```

---

## 🔗 Konfigurasi

### Token Telegram (`bot.py`)

Buka file `bot.py` dan ganti placeholder token dengan token bot kamu dari @BotFather:

```python
TOKEN = 'ISI_TOKEN_BOT_TELEGRAM_KAMU_DI_SINI'
```

### Koneksi Mikrotik dan Akses Kontrol (`config.py`)

Buka file `config.py` dan sesuaikan dengan pengaturan router dan akses kontrol kamu:

```python
MIKROTIK_ROUTER = {
    'host': '192.168.1.1',       # IP address Mikrotik
    'username': 'apibot',        # Username API Mikrotik
    'password': 'passwdapi123',  # Password API Mikrotik
    'port': 8728,                # Port API Mikrotik (default: 8728)
}

ADMIN_IDS = [123456789, 987654321]  # List Telegram User ID yang diizinkan
GROUP_IDS = [-123456789]            # List Group ID tempat command diterima
```

> **⚠️ Catatan Keamanan:**
> - Untuk penggunaan produksi, **jangan gunakan hardcoded credentials** seperti di atas.
> - Sebaiknya gunakan environment variable atau file `.env` yang tidak di-commit ke repository.

---

## 📖 Daftar Perintah Bot

| Perintah | Deskripsi | Format |
|---|---|---|
| `/start` | Menampilkan pesan selamat datang | `/start` |
| `/addpppoe` | Menambahkan user PPPoE | `/addpppoe <username> <password>` atau `/addpppoe <username> <password> <local-address> <remote-address>` |
| `/delpppoe` | Menghapus user PPPoE | `/delpppoe <username>` |
| `/addip` | Menambahkan IP Address ke interface | `/addip <address> <network> <interface>` |
| `/delip` | Menghapus IP Address | `/delip <address>` |
| `/addfirewall` | Menambahkan rule firewall | `/addfirewall <table> <chain> <action> <src-address> <dst-address> <protocol> <port>` |
| `/delfirewall` | Menghapus rule firewall | `/delfirewall <table> <chain> <src-address> <dst-address> <protocol>` |

### Contoh Penggunaan

**Menambahkan user PPPoE:**
```
/addpppoe user1 password123
/addpppoe user1 password123 10.10.10.1 10.10.10.2
```

**Menghapus user PPPoE:**
```
/delpppoe user1
```

**Menambahkan IP Address:**
```
/addip 192.168.1.100/24 192.168.1.0 ether1
```

**Menghapus IP Address:**
```
/delip 192.168.1.100/24
```

**Menambahkan rule firewall:**
```
/addfirewall filter forward drop 192.168.1.0/24 10.0.0.0/8 tcp 80
```

Pilihan parameter:
- **table:** `filter`, `nat`
- **protocol:** `tcp`, `udp`, `icmp`

**Menghapus rule firewall:**
```
/delfirewall filter forward 192.168.1.0/24 10.0.0.0/8 tcp
```

---

## 📄 Dependencies

File `requirements.txt` berisi:

```text
python-telegram-bot==20.7
routeros-api==0.17.0
```

| Package | Kegunaan |
|---|---|
| `python-telegram-bot` | Framework bot Telegram (versi 20+, menggunakan async `Application` API) |
| `routeros-api` | Library untuk koneksi ke Mikrotik via RouterOS API |

> **Catatan:**
> - Pastikan `python-telegram-bot` versi 20 ke atas, karena struktur `Application` dan `CommandHandler` menggunakan API async yang baru.
> - Package `routeros-api` digunakan untuk koneksi ke Mikrotik via API (import sebagai `routeros_api` di kode).

---

## 🔒 Keamanan dan Akses Kontrol

Bot ini memiliki dua lapisan keamanan:

1. **ADMIN_IDS** — Hanya Telegram User ID yang terdaftar di list ini yang bisa menjalankan perintah.
2. **GROUP_IDS** — Perintah hanya bisa dijalankan di group Telegram yang terdaftar.

Setiap command handler melakukan pengecekan kedua kondisi di atas sebelum memproses perintah. Jika salah satu tidak terpenuhi, bot akan menolak perintah dengan pesan error.

---

## 🖥️ Deploy sebagai Systemd Service (Linux)

Untuk menjalankan bot secara otomatis saat server boot:

1. Buat file service:

    ```bash
    sudo nano /etc/systemd/system/mikrotik_bot.service
    ```

2. Isi dengan konfigurasi berikut (sesuaikan path):

    ```ini
    [Unit]
    Description=Telegram Mikrotik Bot Service
    After=network.target

    [Service]
    WorkingDirectory=/opt/mikrotik_bot
    ExecStart=/opt/mikrotik_bot/venv/bin/python /opt/mikrotik_bot/bot.py
    Restart=always
    User=root
    StandardOutput=syslog
    StandardError=syslog
    SyslogIdentifier=mikrotik_bot

    [Install]
    WantedBy=multi-user.target
    ```

3. Aktifkan dan jalankan service:

    ```bash
    sudo systemctl daemon-reload
    sudo systemctl enable mikrotik_bot
    sudo systemctl start mikrotik_bot
    ```

4. Cek status bot:

    ```bash
    sudo systemctl status mikrotik_bot
    ```

> **Catatan:** Sesuaikan `WorkingDirectory` dan `ExecStart` dengan lokasi folder project kamu.

---

## 🛠️ Pengembangan

### Menambahkan Fitur Baru

Untuk menambahkan fitur baru (misal: DHCP, BGP, Hotspot), ikuti langkah berikut:

1. Buat file handler baru di folder `commands/`, contoh: `commands/dhcp.py`.
2. Implementasikan fungsi handler async dengan pola yang sama seperti handler yang sudah ada.
3. Daftarkan handler baru di `bot.py` menggunakan `app.add_handler(CommandHandler(...))`.
4. Tambahkan method API yang dibutuhkan di class `MikrotikAPI` pada file `mikrotik_api.py`.

### Menjalankan Lint Check

```bash
pip install pyflakes
python -m pyflakes bot.py config.py mikrotik_api.py commands/*.py
```

---

## 🤝 Kontribusi

Kontribusi sangat diterima! Silakan fork repository ini, buat branch baru, dan kirim pull request.

1. Fork repository ini
2. Buat branch fitur: `git checkout -b fitur-baru`
3. Commit perubahan: `git commit -m "Menambahkan fitur baru"`
4. Push ke branch: `git push origin fitur-baru`
5. Buat Pull Request

---

## 📄 Lisensi

Proyek ini dilisensikan di bawah [MIT License](LICENSE).

Copyright (c) 2025 Yonaldi
