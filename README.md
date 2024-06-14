
---

# Botoilerplate

This repository provides a boilerplate for creating a Telegram bot using the `python-telegram-bot` library.

## Setup

Follow these steps to set up your environment and run the bot:

### 1. Clone the Repository
```bash
git clone https://github.com/BabaScience/botoilerplate.git <your_bot_name>
cd <your_bot_name>
```

### 2. Create and Activate a Virtual Environment
```bash
# On Windows
python -m venv venv
.\venv\Scripts\activate

# On macOS/Linux
python -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```
- Alternatively, you can run `python manage.py install` to create the virtual environment and install dependencies in one step.

### 4. Create a New Telegram Bot
- Go to [BotFather](https://t.me/BotFather) on Telegram.
- Follow the instructions to create a new bot and obtain the bot token.

### 5. Add Your Bot Token to the `.env` File
- Create a `.env` file in the root directory of your project.
- Add the following line to the `.env` file:
  ```dotenv
  BOT_TOKEN=6807.....:AAGIlUxxxxxxxxxxxxxxxxxxx...
  ```

### 6. Run the Bot
```bash
python bot.py
```
- Alternatively, you can run `python manage.py run`.

## Using `manage.py`

For users who don't have `make` installed, the `manage.py` script provides similar functionality:

### Create a Virtual Environment
```bash
python manage.py create-venv
```

### Install Dependencies
```bash
python manage.py install
```

### Run the Bot
```bash
python manage.py run
```

### Install a Specific Library and Update `requirements.txt`
```bash
python manage.py install-lib <library_name>
```

### Remove a Specific Library and Update `requirements.txt`
```bash
python manage.py remove-lib <library_name>
```

## Makefile Commands

For users who have `make` installed, you can use the Makefile commands:

### Setup
Sets up the virtual environment and installs dependencies.
```bash
make setup
```

### Run
Runs the bot.
```bash
make run
```

### Install Library
Installs a specific library and updates `requirements.txt`.
```bash
make install-lib
```

### Remove Library
Removes a specific library and updates `requirements.txt`.
```bash
make remove-lib
```

## Troubleshooting

- **Virtual Environment Not Activating**: Ensure you are using the correct command for your operating system.
- **Dependencies Not Installing**: Verify your `requirements.txt` file is correctly formatted and lists all necessary packages.
- **Bot Not Running**: Check your `.env` file for the correct `BOT_TOKEN`.

Feel free to reach out if you have any questions or encounter any issues!

---

This version provides clear, well-formatted instructions for both `make` users and those using the `manage.py` script, ensuring everyone can set up and manage the bot easily.