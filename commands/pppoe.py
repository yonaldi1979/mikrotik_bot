# commands/pppoe.py
from config import ADMIN_IDS, GROUP_IDS
from mikrotik_api import MikrotikAPI
from telegram import Update
from telegram.ext import ContextTypes

async def handle_add_pppoe(update: Update, context: ContextTypes.DEFAULT_TYPE):
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

        if len(command_parts) not in [3, 5]:
            await message.reply_text(
                "❌ Format salah!\nGunakan format:\n"
                "/addpppoe <username> <password>\n"
                "atau\n"
                "/addpppoe <username> <password> <local-address> <remote-address>"
            )
            return

        username = command_parts[1]
        password = command_parts[2]
        local_address = None
        remote_address = None

        if len(command_parts) == 5:
            local_address = command_parts[3]
            remote_address = command_parts[4]

        mikrotik = MikrotikAPI()
        mikrotik.add_pppoe_user(username, password, local_address, remote_address)
        mikrotik.disconnect()

        if local_address and remote_address:
            await message.reply_text(
                f"✅ PPPoE user `{username}` berhasil ditambahkan.\n"
                f"📍 Local Address: {local_address}\n"
                f"📍 Remote Address: {remote_address}"
            )
        else:
            await message.reply_text(f"✅ PPPoE user `{username}` berhasil ditambahkan.")

    except Exception as e:
        await message.reply_text(f"❌ Terjadi kesalahan: {e}")

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
            await message.reply_text("❌ Format salah!\nGunakan format: /delpppoe <username>")
            return

        username = command_parts[1]

        mikrotik = MikrotikAPI()
        if mikrotik.delete_pppoe_user(username):
            await message.reply_text(f"✅ User PPPoE `{username}` sudah dihapus.")
        mikrotik.disconnect()

    except Exception as e:
        await message.reply_text(f"❌ Terjadi kesalahan: {e}")
