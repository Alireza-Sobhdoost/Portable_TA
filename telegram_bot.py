from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import re
from llm import LLM
from voice_trans import VoiceModel
from User import User
from telegramify_markdown import markdownify
from functools import wraps



TOKEN = "your_api_key"
LLM_Agent = LLM()
Voice_Agent = VoiceModel()



from functools import wraps
import tempfile
import os

def Voice_mode(transcriber):
    def decorator(func):
        @wraps(func)
        async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
            text = None
            if update.message.voice:
                chat_id = update.effective_chat.id
                voice_file = await update.message.voice.get_file()

                # Download to a temporary file
                with tempfile.NamedTemporaryFile(delete=False, suffix=".ogg") as tmp_file:
                    await voice_file.download_to_drive(tmp_file.name)
                    tmp_file_path = tmp_file.name

                try:
                    # Transcribe the audio file
                    transcribed_text = transcriber(tmp_file_path)
                    # text = LLM_Agent.clean_voice_data(transcribed_text)
                    text = transcribed_text
                except Exception as e:
                    pass 
                finally:
                    os.remove(tmp_file_path)  # Clean up

            return await func(update, context, text)
        return wrapper
    return decorator


def replace_double_dolor(text):
    return text.replace('$$', '$')
def replace_dollar_math(text):
    return re.sub(r'\$(.+?)\$', r'\\[\1\\]', text)
def replace_double_backslashes(text):
    return text.replace('\\\\', '\\')
def remove_zwnj(text):
    return text.replace('\u200c', '')
# def replace_zwnj_with_space(text):
#     return text.replace('\u200c', ' ')

def clean_text(text):
    text = replace_double_dolor(text)
    text = replace_dollar_math(text)
    text = replace_double_backslashes(text)
    text = remove_zwnj(text)  # or replace_zwnj_with_space(text) if preferred
    return text


@Voice_mode(transcriber=Voice_Agent)
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE, text = None):
    user_text = text if text is not None else update.message.text
    print(text)
    chat_id = update.effective_chat.id

    try:
        current_user = User.DB[chat_id]
    except KeyError:
        current_user = User(chat_id)

    llm_response, current_user.messages, current_user.summery = LLM_Agent(
        user_text, current_user.messages, current_user.summery
    )

    llm_response = clean_text(llm_response)
    reply_text = markdownify(llm_response)
    await update.message.reply_text(reply_text, parse_mode='MarkdownV2')


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    if chat_id not in User.DB.keys() :
        u = User(chat_id)
    await update.message.reply_text("سلام! سوال خود را بفرستید و جواب محاسباتی دقیق را دریافت کنید.")

def main():
    application = ApplicationBuilder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler((filters.TEXT | filters.VOICE) & ~filters.COMMAND, handle_message))
    application.run_polling()

if __name__ == "__main__":
    main()
