# Botoilerplate

This repository provides a boilerplate for creating a Telegram bot using the `python-telegram-bot` library.

## Setup

Follow these steps to set up your environment and run the bot:

1. **Clone the repository:**
   ```
   git clone https://github.com/BabaScience/botoilerplate.git <your_bot_name>
   cd <your_bot_name>
   ```

2. **Create a virtual environment and activate it:**
   ```
   python -m venv venv
   .\venv\Scripts\activate  # On Windows
   source venv/bin/activate  # On macOS/Linux
   ```
   - Alternatively, you can run `make setup` and skip step 3.

3. **Install dependencies:**
   ```
   pip install -r requirements.txt
   ```

4. **Create a new Telegram Bot:**
   - Go to [BotFather](https://t.me/BotFather) on Telegram.
   - Follow the instructions to create a new bot and obtain the bot token.

5. **Add your bot token to the `.env` file:**
   - Create a `.env` file in the root directory of your project.
   - Add the following line to the `.env` file:
     ```
     BOT_TOKEN=6807.....:AAGIlUxxxxxxxxxxxxxxxxxxx...
     ```

6. **Run the bot:**
   ```
   python bot.py
   ```
   - Alternatively, you can run `make run`.

## Makefile Commands

- **`make setup`**: Sets up the virtual environment and installs dependencies.
- **`make run`**: Runs the bot.
- **`make install-lib`**: Installs a specific library and updates `requirements.txt`.
- **`make remove-lib`**: Removes a specific library and updates `requirements.txt`.

Feel free to reach out if you have any questions or encounter any issues!