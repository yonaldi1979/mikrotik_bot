# bot.py
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from config import ADMIN_IDS, GROUP_IDS
from commands.pppoe import handle_add_pppoe
from commands.del_pppoe import handle_del_pppoe
from commands.ip_address import handle_add_ip, handle_del_ip
from commands.firewall import handle_add_firewall, handle_del_firewall

TOKEN = '7708227316:AAERqxasCl8KMFCXnbIo7G-K049--SMrIX0'  # Ganti token Telegram di sini

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bot Mikrotik siap menerima perintah!")

def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler('start', start))
    app.add_handler(CommandHandler('addpppoe', handle_add_pppoe))
    app.add_handler(CommandHandler('delpppoe', handle_del_pppoe))
#----------------------- dibawah untuk ip address ------------------#
    app.add_handler(CommandHandler('addip', handle_add_ip))
    app.add_handler(CommandHandler('delip', handle_del_ip))
#-------------------------- ini bagian firewall ------------------------------#
    app.add_handler(CommandHandler('addfirewall', handle_add_firewall))
    app.add_handler(CommandHandler('delfirewall', handle_del_firewall))
    print("Bot is running...")
    app.run_polling()

if __name__ == '__main__':
    main()
