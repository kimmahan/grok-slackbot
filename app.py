import os
import logging
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from openai import AsyncOpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize the Slack app
app = App(token=os.environ.get("SLACK_BOT_TOKEN"))

# Initialize the xAI client
# xAI API uses the same client library as OpenAI but with a different base_url
client = AsyncOpenAI(
    api_key=os.environ.get("XAI_API_KEY"),
    base_url="https://api.x.ai/v1"
)

# Define a function to interact with Grok
async def ask_grok(prompt, conversation_history=None):
    try:
        # Format the messages for the API
        messages = [
            {"role": "system", "content": "You are a helpful assistant that provides concise, accurate information."}
        ]
        
        # Add conversation history if provided
        if conversation_history:
            for message in conversation_history:
                if message["user"] == "user":
                    messages.append({"role": "user", "content": message["text"]})
                else:
                    messages.append({"role": "assistant", "content": message["text"]})
        
        # Add the current prompt
        messages.append({"role": "user", "content": prompt})
        
        # Make the API call to Grok
        response = await client.chat.completions.create(
            model="grok-beta",  # Using Grok's beta model
            messages=messages,
            temperature=0.7,
            max_tokens=1024
        )
        
        # Return the response
        return response.choices[0].message.content
    except Exception as e:
        logger.error(f"Error calling Grok API: {e}")
        return f"Sorry, I encountered an error when trying to generate a response: {str(e)}"

# Listen for direct messages
@app.event("message")
async def handle_direct_messages(event, say):
    # Ignore messages from the bot itself or if it's not in a direct message channel
    if "user" not in event or event.get("channel_type") != "im":
        return
        
    # Get the bot's user ID
    bot_user_id = app.client.auth_test()["user_id"]
    if event.get("user") == bot_user_id:
        return
    
    # Process the message with Grok
    user_message = event.get("text", "")
    logger.info(f"Received DM: {user_message}")
    
    # Get conversation history (simplified - in production you might want to use a database)
    conversation_history = []  # You can implement history tracking here
    
    # Get response from Grok
    response = await ask_grok(user_message, conversation_history)
    logger.info(f"Sending response: {response[:50]}...")
    
    # Send the response back to Slack
    await say(response)

# Listen for mentions in channels
@app.event("app_mention")
async def handle_mentions(event, say):
    # Extract the text after the mention
    text = event.get("text", "")
    logger.info(f"Received mention: {text}")
    
    # Get the bot's user ID
    bot_user_id = app.client.auth_test()["user_id"]
    mention = f"<@{bot_user_id}>"
    
    if mention in text:
        user_message = text.split(mention)[1].strip()
    else:
        user_message = text.strip()
    
    if not user_message:
        user_message = "Hello!"  # Default message if user just mentioned the bot
    
    # Get response from Grok
    response = await ask_grok(user_message)
    logger.info(f"Sending response: {response[:50]}...")
    
    # Send the response back to Slack
    await say(response)

# Start the app
if __name__ == "__main__":
    # Log startup information
    logger.info("Starting Grok Slackbot...")
    
    # Use Socket Mode for easier development (no public URL needed)
    handler = SocketModeHandler(app, os.environ.get("SLACK_APP_TOKEN"))
    
    try:
        logger.info("App is running!")
        handler.start()
    except Exception as e:
        logger.error(f"Error starting app: {e}")