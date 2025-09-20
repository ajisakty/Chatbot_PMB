import os
from telegram import Update
from telegram.ext import ContextTypes
from config import ADMIN_PASSWORD
from services.file_service import excel_to_json

#Save login Admin Session
admin_session = set()

async def handle_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id

    if chat_id in admin_session:
        await update.message.reply_text("Anda Sudah Login, Silahkan Upload")
        return
    
    if not context.args:
        await update.message.reply_text("Masukkan password admin: /admin <password>")
        return
    
    password = context.args[0]
    if password == ADMIN_PASSWORD:
        admin_session.add(chat_id)
        await update.message.reply_text("Login Berhasil. Silakan upload file Excel untuk memperbarui FAQ.")
    else:
        await update.message.reply_text("Password Salah")

async def handle_file_upload(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id

    if chat_id not in admin_session:
        await update.message.reply_text("Silahkan Login Admin Terlebih Dahulu")
        return
    
    if not update.message.document:
        await update.message.reply_text("Silahkan Upload File Excel.")
        return
    
    file = await update.message.document.get_file()
    file_path = f"temp/{update.message.document.file_name}"
    os.makedirs("temp", exist_ok=True)
    await file.download_to_drive(file_path)

    faq_data = excel_to_json(file_path)
    await update.message.reply_text(f"FAQ Berhasil Diperbarui. Total {len(faq_data)} pertanyaan.")