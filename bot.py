import logging
import os
import asyncio
from flask import Flask, request
from telegram import Update, Bot
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, Updater
from handlers import start, help_command, change_language, hello
from agent_handlers import (
    setup_agent, ask_command, chat_command, endchat_command, 
    models_command, setmodel_command, handle_message
)
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
DEFAULT_MODEL = os.getenv('DEFAULT_MODEL', 'llama3.2')

# Create Flask app
app = Flask(__name__)

# Create Telegram bot and updater
bot = Bot(token=BOT_TOKEN)
update_queue = asyncio.Queue()
updater = Updater(bot=bot, update_queue=update_queue)
application = ApplicationBuilder().token(BOT_TOKEN).build()

# Set up the Ollama agent
setup_agent(model_name=DEFAULT_MODEL)

# Add basic command handlers
application.add_handler(CommandHandler("hello", hello))
application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("help", help_command))
application.add_handler(CommandHandler("lang", change_language))

# Add agent command handlers
application.add_handler(CommandHandler("ask", ask_command))
application.add_handler(CommandHandler("chat", chat_command))
application.add_handler(CommandHandler("endchat", endchat_command))
application.add_handler(CommandHandler("models", models_command))
application.add_handler(CommandHandler("setmodel", setmodel_command))

# Add message handler for chat mode (must be added last)
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

@app.route(f'/{BOT_TOKEN}', methods=['POST'])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    update_queue.put_nowait(update)
    return 'ok'

async def main():
    """
    Main function to run the bot.
    """
    try:
        if HEROKU_APP_NAME:
            # Running on Heroku or other server
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
            logger.info(f"Bot started with Ollama integration using model: {DEFAULT_MODEL}")
            logger.info(f"Available commands: /start, /help, /lang, /ask, /chat, /endchat, /models, /setmodel")
            
            # Create a proper event to wait on
            stop_signal = asyncio.Event()
            await stop_signal.wait()
    except Exception as e:
        logger.error(f"Error in main function: {str(e)}")
        raise
    finally:
        # Ensure proper cleanup
        if 'application' in locals() and application:
            try:
                await application.stop()
                await application.shutdown()
            except Exception as e:
                logger.error(f"Error during shutdown: {str(e)}")

if __name__ == '__main__':
    # Python 3.12+ has improved asyncio
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Fatal error: {str(e)}")
