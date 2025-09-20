from telegram import Update
from telegram.ext import ContextTypes
from services.nlp_service import get_best_answer

async def handle_ask(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Silahkan Masukan Pertanyaan setelah /ask")
        return
    
    question = " ".join(context.args)
    answer = get_best_answer(question)
    await Update.message.reply_text(answer)