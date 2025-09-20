from telegram.ext import Application, CommandHandler, MessageHandler, filters
from config import TELEGRAM_TOKEN
from handlers.user_handler import handle_ask
from handlers.admin_handler import handle_admin, handle_file_upload

async def start(update, context):
    await update.message.reply_text(
        "Selamat datang di Chatbot PMB Universitas Pamulang \n"
        "Gunakan kata perintah berikut: \n"
        "- /ask <pertanyaan> → untuk calon mahasiswa\n"
        "- /admin <password> → untuk admin"
    )

def main():
    app = Application.builder().token(TELEGRAM_TOKEN)

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("ask", handle_ask))
    app.add_handler(CommandHandler("admin", handle_admin))
    app.add_handler(MessageHandler(filters.Document.ALL, handle_file_upload))

    app.run_polling()

if __name__ == "__main__":
    main()