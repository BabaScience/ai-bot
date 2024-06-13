from telegram import Update
from telegram.ext import CommandHandler, CallbackContext

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Hello! Welcome to the bot.')

def help_command(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Help! This is a bot to demonstrate a boilerplate.')
