"""
Handlers for agentic interactions with the Telegram bot using Ollama LLM.
"""

import logging
from telegram import Update
from telegram.ext import ContextTypes
from ollama_connector import OllamaConnector
from typing import Dict, Optional

# Set up logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Dictionary to store user's conversation history
conversations: Dict[int, list] = {}

# Default system prompt for the agent
DEFAULT_SYSTEM_PROMPT = """You are a helpful AI assistant on Telegram.
You provide informative, concise, and accurate responses.
If you don't know something, admit it rather than making up information.
Be conversational but efficient in your responses."""

# Initialize the Ollama connector (will be set in setup_agent)
ollama_connector = None

def setup_agent(model_name: str = "llama3.2") -> None:
    """
    Set up the agent with the specified model.
    
    Args:
        model_name (str): The Ollama model to use
    """
    global ollama_connector
    ollama_connector = OllamaConnector(model_name)
    logger.info(f"Agent set up with model: {model_name}")

async def ask_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handle the /ask command to interact with the LLM.
    
    Args:
        update (Update): The update object containing information about the message
        context (ContextTypes.DEFAULT_TYPE): The context for the callback
    """
    user_id = update.effective_user.id
    
    # Check if a prompt was provided
    if not context.args:
        await update.message.reply_text("Please provide a question after /ask. For example: /ask What is Python?")
        return
    
    # Join all arguments to form the prompt
    prompt = " ".join(context.args)
    
    # Send typing action to indicate processing
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
    
    # First check if Ollama is running
    ollama_running = await ollama_connector.check_ollama_running()
    if not ollama_running:
        await update.message.reply_text(
            "❌ Ollama service is not running or not accessible.\n\n"
            "Please start Ollama with the following command:\n"
            "```\nollama serve\n```\n"
            "Then try again."
        )
        return
    
    try:
        # Get response from Ollama
        await update.message.reply_text("🤔 Thinking...")
        response = await ollama_connector.generate_response(
            prompt=prompt,
            system_prompt=DEFAULT_SYSTEM_PROMPT
        )
        
        # Send the response
        await update.message.reply_text(response)
    except Exception as e:
        error_msg = str(e)
        logger.error(f"Error in ask_command: {error_msg}")
        await update.message.reply_text(
            f"Sorry, I encountered an error: {error_msg}\n\n"
            "Please make sure Ollama is running and the model is properly installed."
        )

async def chat_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handle the /chat command to start a chat session with the LLM.
    
    Args:
        update (Update): The update object containing information about the message
        context (ContextTypes.DEFAULT_TYPE): The context for the callback
    """
    user_id = update.effective_user.id
    
    # Check if Ollama is running before starting a chat
    ollama_running = await ollama_connector.check_ollama_running()
    if not ollama_running:
        await update.message.reply_text(
            "❌ Ollama service is not running or not accessible.\n\n"
            "Please start Ollama with the following command:\n"
            "```\nollama serve\n```\n"
            "Then try again."
        )
        return
    
    # Initialize conversation for this user if it doesn't exist
    if user_id not in conversations:
        conversations[user_id] = []
    
    await update.message.reply_text(
        "Chat session started! You can now have a conversation with the AI. "
        "Your messages will be sent to the AI until you type /endchat to end the session."
    )
    
    # Store in user_data that the user is in chat mode
    context.user_data["in_chat_mode"] = True

async def endchat_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handle the /endchat command to end a chat session.
    
    Args:
        update (Update): The update object containing information about the message
        context (ContextTypes.DEFAULT_TYPE): The context for the callback
    """
    user_id = update.effective_user.id
    
    # Check if user is in chat mode
    if context.user_data.get("in_chat_mode", False):
        # Clear conversation history
        if user_id in conversations:
            conversations[user_id] = []
        
        # Set chat mode to False
        context.user_data["in_chat_mode"] = False
        
        await update.message.reply_text("Chat session ended. You can start a new one with /chat.")
    else:
        await update.message.reply_text("You're not in a chat session. Use /chat to start one.")

async def models_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handle the /models command to list available Ollama models.
    
    Args:
        update (Update): The update object containing information about the message
        context (ContextTypes.DEFAULT_TYPE): The context for the callback
    """
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
    
    try:
        # First check if Ollama is running
        ollama_running = await ollama_connector.check_ollama_running()
        if not ollama_running:
            await update.message.reply_text(
                "❌ Ollama service is not running or not accessible.\n\n"
                "Please start Ollama with the following command:\n"
                "```\nollama serve\n```\n"
                "Then try the /models command again."
            )
            return
            
        # If Ollama is running, proceed to fetch models
        await update.message.reply_text("Fetching available models from Ollama...")
        models = await ollama_connector.get_available_models()
        
        if models:
            models_text = "Available models:\n" + "\n".join([f"- {model}" for model in models])
            await update.message.reply_text(models_text)
        else:
            # Provide more detailed error message
            await update.message.reply_text(
                "No models found. Please check:\n"
                "1. You've pulled at least one model using:\n"
                "   `ollama pull llama3.2`\n"
                "2. If you've pulled models with different names, use those instead\n"
                "3. Check the bot logs for more details on any errors"
            )
    except Exception as e:
        error_msg = str(e)
        logger.error(f"Error in models_command: {error_msg}")
        await update.message.reply_text(
            f"Error retrieving models: {error_msg}\n\n"
            "Please ensure Ollama is properly installed and running."
        )

async def setmodel_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handle the /setmodel command to change the Ollama model.
    
    Args:
        update (Update): The update object containing information about the message
        context (ContextTypes.DEFAULT_TYPE): The context for the callback
    """
    global ollama_connector
    
    if not context.args:
        await update.message.reply_text(
            "Please specify a model name. Example: /setmodel llama3.2\n"
            "Use /models to see available models."
        )
        return
    
    model_name = context.args[0]
    
    # Check if Ollama is running
    ollama_running = await ollama_connector.check_ollama_running()
    if not ollama_running:
        await update.message.reply_text(
            "❌ Ollama service is not running or not accessible.\n\n"
            "Please start Ollama with the following command:\n"
            "```\nollama serve\n```\n"
            "Then try again."
        )
        return
    
    try:
        # Check if the model exists
        available_models = await ollama_connector.get_available_models()
        if available_models and model_name not in available_models:
            await update.message.reply_text(
                f"⚠️ Model '{model_name}' is not available.\n\n"
                f"Available models: {', '.join(available_models)}\n\n"
                f"You can pull a new model with:\n"
                f"```\nollama pull {model_name}\n```"
            )
            return
        
        # Create a new connector with the specified model
        ollama_connector = OllamaConnector(model_name)
        
        await update.message.reply_text(f"Model changed to {model_name}")
    except Exception as e:
        error_msg = str(e)
        logger.error(f"Error in setmodel_command: {error_msg}")
        await update.message.reply_text(
            f"Error changing model: {error_msg}\n\n"
            "Please make sure Ollama is running and the model is properly installed."
        )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handle regular messages when user is in chat mode.
    
    Args:
        update (Update): The update object containing information about the message
        context (ContextTypes.DEFAULT_TYPE): The context for the callback
    """
    # Check if this is a command (starts with /)
    if update.message.text.startswith('/'):
        return
    
    user_id = update.effective_user.id
    
    # Check if user is in chat mode
    if context.user_data.get("in_chat_mode", False):
        await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
        
        # Add user message to conversation history
        if user_id not in conversations:
            conversations[user_id] = []
        
        user_message = update.message.text
        # We don't need to store the history in our own format anymore
        # as we'll just directly pass the prompt to generate_response
        
        try:
            # Generate response
            response = await ollama_connector.generate_response(
                prompt=user_message,
                system_prompt=DEFAULT_SYSTEM_PROMPT
            )
            
            # Send the response
            await update.message.reply_text(response)
        except Exception as e:
            logger.error(f"Error in handle_message: {str(e)}")
            await update.message.reply_text(f"Sorry, I encountered an error: {str(e)}") 