# Example Workflow: Telegram Echo Bot

This example demonstrates how to create a simple echo bot using the Telegram custom nodes.

## Workflow Steps:

1. **Telegram Listener Node**
   - Input your bot token
   - Set timeout to 30 seconds (or desired wait time)
   - This will output the received message text and chat ID

2. **Processing** (Optional)
   - You can add any processing nodes here
   - For example: text transformation, AI processing, image generation, etc.

3. **Save to Telegram Node**
   - Use the same bot token
   - Connect the chat_id from the listener
   - Connect your processed message (or just echo the original)

## ComfyUI Workflow JSON

```json
{
  "1": {
    "inputs": {
      "bot_token": "YOUR_BOT_TOKEN_HERE",
      "timeout": 30
    },
    "class_type": "TelegramListener",
    "_meta": {
      "title": "Telegram Listener"
    }
  },
  "2": {
    "inputs": {
      "text": [
        "1",
        0
      ]
    },
    "class_type": "CLIPTextEncode",
    "_meta": {
      "title": "Echo the message"
    }
  },
  "3": {
    "inputs": {
      "bot_token": "YOUR_BOT_TOKEN_HERE",
      "chat_id": [
        "1",
        1
      ],
      "message": [
        "1",
        0
      ]
    },
    "class_type": "SaveToTelegram",
    "_meta": {
      "title": "Send back to Telegram"
    }
  }
}
```

## Setup Instructions:

1. Replace `YOUR_BOT_TOKEN_HERE` with your actual bot token from BotFather
2. Load this workflow in ComfyUI
3. Queue the workflow
4. Send a message to your bot in Telegram
5. The bot will echo the message back to you

## Advanced Usage:

You can extend this workflow by:
- Adding image generation nodes between the listener and sender
- Processing the text through AI models
- Adding conditional logic based on message content
- Storing conversation history
- Adding multiple response types
