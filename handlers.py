from telegram import Update
from telegram.ext import CommandHandler, CallbackContext
import json

# load environment variables
from dotenv import load_dotenv, dotenv_values
load_dotenv()

# Load translations
def load_translations():
    translations = {}
    with open('translations/en.json', 'r', encoding='utf-8') as f:
        translations['en'] = json.load(f)
    with open('translations/fr.json', 'r', encoding='utf-8') as f:
        translations['fr'] = json.load(f)
    return translations

translations = load_translations()

DEFAULT_LANGUAGE = dotenv_values(".env")["DEFAULT_LANGUAGE"]

def translate(text, lang):
    return translations.get(lang, translations[DEFAULT_LANGUAGE]).get(text, text)

async def start(update: Update, context: CallbackContext) -> None:
    user_lang = context.user_data.get('lang', DEFAULT_LANGUAGE)
    await  update.message.reply_text(translate('Hello! Welcome to the bot.', user_lang))

async def hello(update: Update, context: CallbackContext) -> None:
    user_lang = context.user_data.get('lang', DEFAULT_LANGUAGE)
    await update.message.reply_text(translate(f'Hello', user_lang) + f' {update.effective_user.first_name}!')

async def help_command(update: Update, context: CallbackContext) -> None:
    user_lang = context.user_data.get('lang', DEFAULT_LANGUAGE)
    await  update.message.reply_text(translate('Help! This is a bot to demonstrate a boilerplate.', user_lang))

async def change_language(update: Update, context: CallbackContext) -> None:
    lang = context.args[0] if context.args else DEFAULT_LANGUAGE
    if lang in translations:
        context.user_data['lang'] = lang
        await update.message.reply_text(translate('Language changed successfully.', lang))
    else:
        await update.message.reply_text(translate('Language not supported.', DEFAULT_LANGUAGE))