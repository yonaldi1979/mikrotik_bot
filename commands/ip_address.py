# commands/ip_address.py
from config import ADMIN_IDS, GROUP_IDS
from mikrotik_api import MikrotikAPI
from telegram import Update
from telegram.ext import ContextTypes

async def handle_add_ip(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    chat_id = message.chat_id
    user_id = message.from_user.id

    if chat_id not in GROUP_IDS:
        await message.reply_text("❌ Perintah hanya bisa dijalankan di group terdaftar.")
        return

    if user_id not in ADMIN_IDS:
        await message.reply_text("❌ Kamu tidak punya izin menjalankan perintah ini.")
        return

    try:
        command_parts = message.text.split()

        if len(command_parts) != 4:
            await message.reply_text("❌ Format salah!\nGunakan format: /addip <address> <network> <interface>")
            return

        address = command_parts[1]
        network = command_parts[2]
        interface = command_parts[3]

        mikrotik = MikrotikAPI()
        mikrotik.add_ip_address(address, network, interface)
        mikrotik.disconnect()

        await message.reply_text(f"✅ IP Address `{address}` berhasil ditambahkan di interface `{interface}`.")
    except Exception as e:
        await message.reply_text(f"❌ Terjadi kesalahan: {e}")

async def handle_del_ip(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    chat_id = message.chat_id
    user_id = message.from_user.id

    if chat_id not in GROUP_IDS:
        await message.reply_text("❌ Perintah hanya bisa dijalankan di group terdaftar.")
        return

    if user_id not in ADMIN_IDS:
        await message.reply_text("❌ Kamu tidak punya izin menjalankan perintah ini.")
        return

    try:
        command_parts = message.text.split()

        if len(command_parts) != 2:
            await message.reply_text("❌ Format salah!\nGunakan format: /delip <address>")
            return

        address = command_parts[1]

        mikrotik = MikrotikAPI()
        mikrotik.delete_ip_address(address)
        mikrotik.disconnect()

        await message.reply_text(f"✅ IP Address `{address}` berhasil dihapus.")
    except Exception as e:
        await message.reply_text(f"❌ Terjadi kesalahan: {e}")
