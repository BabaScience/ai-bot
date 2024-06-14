import logging
import os
import asyncio
from flask import Flask, request
from telegram import Update, Bot
from telegram.ext import ApplicationBuilder, CommandHandler, Updater
from handlers import start, help_command, change_language, hello
from dotenv import load_dotenv, dotenv_values

load_dotenv()

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)

BOT_TOKEN = dotenv_values(".env")["BOT_TOKEN"] if dotenv_values(".env").get("DEV") == "true"  else os.getenv('BOT_TOKEN')
HEROKU_APP_NAME = os.getenv('HEROKU_APP_NAME')
APP_URL = f"https://{HEROKU_APP_NAME}.herokuapp.com/{BOT_TOKEN}" if HEROKU_APP_NAME else None

# Create Flask app
app = Flask(__name__)

# Create Telegram bot and updater
bot = Bot(token=BOT_TOKEN)
update_queue = asyncio.Queue()
updater = Updater(bot=bot, update_queue=update_queue)
application = ApplicationBuilder().token(BOT_TOKEN).build()

application.add_handler(CommandHandler("hello", hello))
application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("help", help_command))
application.add_handler(CommandHandler("lang", change_language))

@app.route(f'/{BOT_TOKEN}', methods=['POST'])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    update_queue.put_nowait(update)
    return 'ok'

async def main():
    if HEROKU_APP_NAME:
        # Running on Heroku
        async with updater:
            await updater.start_webhook(
                listen="0.0.0.0",
                port=int(os.environ.get('PORT', 5000)),
                url_path=BOT_TOKEN,
                webhook_url=APP_URL
            )
            app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
    else:
        # Running locally
        await application.initialize()
        await application.start()
        await application.updater.start_polling()
        try:
            await asyncio.Event().wait()  # Run until interrupted
        finally:
            await application.stop()
            await application.shutdown()

if __name__ == '__main__':
    asyncio.run(main())
