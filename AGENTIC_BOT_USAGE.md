# Agentic Telegram Bot with Ollama Integration

This document explains how to set up and use the agentic capabilities of the Telegram bot, powered by Ollama for local LLM execution.

## Prerequisites

Before using the agentic features, you need to:

1. **Install Ollama**: Follow the instructions at [Ollama's official website](https://ollama.ai/) to install Ollama on your machine.

2. **Pull models**: After installing Ollama, pull at least one model:
   ```bash
   ollama pull llama3.2
   ```
   You can pull additional models based on your needs (e.g., `ollama pull mistral` or `ollama pull gemma:7b`).

3. **Start Ollama**: Make sure Ollama is running before starting the bot.
   ```bash
   # On most systems, Ollama runs as a service after installation
   # If not, you can start it manually
   ollama serve
   ```

4. **Configure the bot**: In your `.env` file, add the `DEFAULT_MODEL` setting (this has been done for you already):
   ```
   DEFAULT_MODEL='llama3.2'
   ```

## Using Agentic Features

The bot now supports the following commands for interacting with the AI:

### Single Questions

```
/ask [your question here]
```

Use this command to ask a one-off question to the AI without starting a conversation. For example:
- `/ask What is Python?`
- `/ask How does photosynthesis work?`

### Conversations

To have a back-and-forth conversation with the AI:

1. Start a conversation:
   ```
   /chat
   ```

2. Simply type your messages, and the AI will respond directly (no need to use any command).

3. End the conversation when you're done:
   ```
   /endchat
   ```

### Managing Models

You can check available models and switch between them:

1. See installed models:
   ```
   /models
   ```

2. Switch to a different model:
   ```
   /setmodel [model_name]
   ```
   For example: `/setmodel gemma:7b` or `/setmodel mistral`

## Troubleshooting

If you encounter issues:

1. **Error connecting to Ollama**: 
   - Make sure Ollama is running on your system: `ollama serve`
   - The bot will try to connect to Ollama on localhost at the default port
   - Check that there are no firewalls blocking the connection

2. **"No models found" error**: 
   - Ensure you've pulled the model specified in your `.env` file:
     ```bash
     ollama pull llama3.2
     ```
   - Verify that the pulled model name exactly matches the one in your configuration
   - If you want to use a different model, pull it first and then use `/setmodel` to switch
   - You can check your available models directly with: `ollama list`

3. **Slow responses**: 
   - Local LLMs can be resource-intensive. Consider:
     - Using a smaller model if your hardware is limited (e.g., `tinyllama` instead of `llama3.2`)
     - Closing other resource-intensive applications
     - Ensuring your computer meets the minimum requirements for running LLMs

4. **Unexpected responses**: 
   - Some models are better at certain tasks than others
   - Try switching models: `/setmodel [model_name]`
   - Some smaller models may have more limited capabilities

5. **Model not found when using `/setmodel`**:
   - Make sure to pull the model first: `ollama pull [model_name]`
   - Use `/models` to see which models are available
   - Check for typos in the model name

## Customization

You can customize the AI's behavior by editing the `DEFAULT_SYSTEM_PROMPT` in `agent_handlers.py`. This prompt guides how the AI responds to users.

## Advanced: Using Different Ollama Models

The bot is pre-configured to use the `llama3.2` model, but Ollama supports many different models:

- **Llama family**: llama3, llama3.2, llama3:8b, llama3:70b
- **Mistral family**: mistral, mistral:7b, mistral-openorca
- **Other models**: gemma:7b, phi3, tinyllama, etc.

To use a different model:
1. Pull the model: `ollama pull [model_name]`
2. Use the `/setmodel` command: `/setmodel [model_name]`

For a complete list of available models, visit [Ollama's model library](https://ollama.ai/library). 