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

def translate(text: str, lang: str) -> str:
    """
    Translates the given text to the specified language.

    Args:
        text (str): The text to be translated.
        lang (str): The language code for translation.

    Returns:
        str: The translated text.

    """
    return translations.get(lang, translations[DEFAULT_LANGUAGE]).get(text, text)

async def start(update: Update, context: CallbackContext) -> None:
    """
    Handles the /start command and sends a welcome message to the user.

    Args:
        update (telegram.Update): The update object containing information about the incoming message.
        context (telegram.ext.CallbackContext): The context object for handling the callback.

    Returns:
        None
    """
    user_lang = context.user_data.get('lang', DEFAULT_LANGUAGE)
    await update.message.reply_text(translate('Hello! Welcome to the bot.', user_lang))

async def hello(update: Update, context: CallbackContext) -> None:
    """
    Handles the /hello command and sends a greeting message to the user.

    Args:
        update (telegram.Update): The update object containing information about the incoming message.
        context (telegram.ext.CallbackContext): The context object for handling the callback.

    Returns:
        None
    """
    user_lang = context.user_data.get('lang', DEFAULT_LANGUAGE)
    await update.message.reply_text(translate(f'Hello', user_lang) + f' {update.effective_user.first_name}!')

async def help_command(update: Update, context: CallbackContext) -> None:
    """
    Handles the /help command and sends a help message to the user.

    Args:
        update (telegram.Update): The update object containing information about the incoming message.
        context (telegram.ext.CallbackContext): The context object for handling the callback.

    Returns:
        None
    """
    user_lang = context.user_data.get('lang', DEFAULT_LANGUAGE)
    await update.message.reply_text(translate('Help! This is a bot to demonstrate a boilerplate.', user_lang))

async def change_language(update: Update, context: CallbackContext) -> None:
    """
    Handles the /change_language command and changes the language for the user.

    Args:
        update (telegram.Update): The update object containing information about the incoming message.
        context (telegram.ext.CallbackContext): The context object for handling the callback.

    Returns:
        None
    """
    lang = context.args[0] if context.args else DEFAULT_LANGUAGE
    if lang in translations:
        context.user_data['lang'] = lang
        await update.message.reply_text(translate('Language changed successfully.', lang))
    else:
        await update.message.reply_text(translate('Language not supported.', DEFAULT_LANGUAGE))

# Add new command handler
# async def new_handler(update: Update, context: CallbackContext) -> None:
#     await update.message.reply_text('New command handler!')