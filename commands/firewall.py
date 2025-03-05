from config import ADMIN_IDS, GROUP_IDS
from mikrotik_api import MikrotikAPI
from telegram import Update
from telegram.ext import ContextTypes

async def handle_add_firewall(update: Update, context: ContextTypes.DEFAULT_TYPE):
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

        if len(command_parts) != 8:
            await message.reply_text(
                "❌ Format salah!\nGunakan format:\n"
                "/addfirewall <table> <chain> <action> <src-address> <dst-address> <protocol> <port>"
            )
            return

        _, table, chain, action, src_address, dst_address, protocol, port = command_parts

        if table not in ['filter', 'nat']:
            await message.reply_text("❌ Tabel firewall tidak valid. Pilihan: filter, nat")
            return

        if protocol not in ['tcp', 'udp', 'icmp']:
            await message.reply_text("❌ Protocol tidak valid. Pilihan: tcp, udp, icmp")
            return

        mikrotik = MikrotikAPI()
        mikrotik.add_firewall_rule(table, chain, action, src_address, dst_address, protocol, port)
        mikrotik.disconnect()

        await message.reply_text(f"✅ Rule firewall berhasil ditambahkan di tabel `{table}`.")
    except Exception as e:
        await message.reply_text(f"❌ Terjadi kesalahan: {e}")

async def handle_del_firewall(update: Update, context: ContextTypes.DEFAULT_TYPE):
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

        if len(command_parts) != 6:
            await message.reply_text(
                "❌ Format salah!\nGunakan format:\n"
                "/delfirewall <table> <chain> <src-address> <dst-address> <protocol>"
            )
            return

        _, table, chain, src_address, dst_address, protocol = command_parts

        if table not in ['filter', 'nat']:
            await message.reply_text("❌ Tabel firewall tidak valid. Pilihan: filter, nat")
            return

        if protocol not in ['tcp', 'udp', 'icmp']:
            await message.reply_text("❌ Protocol tidak valid. Pilihan: tcp, udp, icmp")
            return

        mikrotik = MikrotikAPI()
        rule_deleted = mikrotik.delete_firewall_rule(table, chain, src_address, dst_address, protocol)
        mikrotik.disconnect()

        if rule_deleted:
            await message.reply_text(f"✅ Rule firewall berhasil dihapus dari tabel `{table}`.")
        else:
            await message.reply_text(f"⚠️ Rule firewall tidak ditemukan di tabel `{table}`.")
    except Exception as e:
        await message.reply_text(f"❌ Terjadi kesalahan: {e}")
