# commands/del_pppoe.py
from config import ADMIN_IDS, GROUP_IDS
from mikrotik_api import MikrotikAPI
from telegram import Update
from telegram.ext import ContextTypes

async def handle_del_pppoe(update: Update, context: ContextTypes.DEFAULT_TYPE):
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
            await message.reply_text("❌ Format salah! Gunakan: /delpppoe username")
            return

        username = command_parts[1]

        mikrotik = MikrotikAPI()
        if mikrotik.delete_pppoe_user(username):
            await message.reply_text(f"✅ PPPoE user `{username}` berhasil dihapus.")
        else:
            await message.reply_text(f"⚠️ PPPoE user `{username}` tidak ditemukan.")
        mikrotik.disconnect()

    except Exception as e:
        await message.reply_text(f"❌ Terjadi kesalahan: {e}")
