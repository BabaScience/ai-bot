import logging
import os
from flask import Flask, request
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler
from handlers import start, help_command, change_language, hello
from dotenv import load_dotenv, dotenv_values

load_dotenv()

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)

BOT_TOKEN = dotenv_values(".env")["BOT_TOKEN"]
APP_URL = f"https://{dotenv_values('.env')['HEROKU_APP_NAME']}.herokuapp.com/{BOT_TOKEN}"  # Heroku app URL

app = Flask(__name__)

telegram_app = ApplicationBuilder().token(BOT_TOKEN).build()

telegram_app.add_handler(CommandHandler("hello", hello))
telegram_app.add_handler(CommandHandler("start", start))
telegram_app.add_handler(CommandHandler("help", help_command))
telegram_app.add_handler(CommandHandler("lang", change_language))

@app.route(f'/{BOT_TOKEN}', methods=['POST'])
def webhook():
    update = Update.de_json(request.get_json(force=True), telegram_app.bot)
    telegram_app.update_queue.put(update)
    return 'ok'

if __name__ == '__main__':
    telegram_app.run_webhook(
        listen="0.0.0.0",
        port=int(os.environ.get('PORT', 5000)),
        url_path=BOT_TOKEN,
        webhook_url=APP_URL
    )
    app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
