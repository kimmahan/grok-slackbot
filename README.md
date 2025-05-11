# Grok Slackbot

A custom Slack bot that uses xAI's Grok API to provide AI-powered responses to your team.

## Features

- Responds to direct messages
- Responds when mentioned in channels
- Uses xAI's Grok model for intelligent, context-aware responses

## Prerequisites

- Python 3.8+
- A Slack workspace with admin permissions
- xAI API access (see [x.ai/api](https://x.ai/api))

## Setup Instructions

### 1. Create a Slack App

1. Go to [https://api.slack.com/apps](https://api.slack.com/apps) and click "Create New App"
2. Choose "From scratch"
3. Name your app (e.g., "Grok Assistant") and select your workspace
4. Click "Create App"

### 2. Configure Bot User and Permissions

1. In the left sidebar, click on "Bot Users"
2. Click "Add Bot User"
3. Configure the display name and username for your bot
4. Toggle "Always Show My Bot as Online" to ON
5. Save changes
6. Go to "OAuth & Permissions" in the sidebar
7. Under "Scopes", add the following Bot Token Scopes:
   - `app_mentions:read`
   - `chat:write`
   - `im:history`
   - `im:write`
   - `channels:history`
8. Save changes

### 3. Enable Socket Mode

1. Go to "Socket Mode" in the sidebar
2. Toggle "Enable Socket Mode" to ON
3. Enter an App-Level Token Name (e.g., "Grok Socket")
4. Click "Generate"
5. Copy the generated token (starts with `xapp-`) - you'll need this for the SLACK_APP_TOKEN

### 4. Enable Events

1. Go to "Event Subscriptions" in the sidebar
2. Toggle "Enable Events" to ON
3. Under "Subscribe to bot events", add:
   - `app_mention`
   - `message.im`
4. Save changes

### 5. Install the App to Your Workspace

1. Go to "Install App" in the sidebar
2. Click "Install to Workspace"
3. Review and approve the permissions
4. Copy the "Bot User OAuth Token" (starts with `xoxb-`) - you'll need this for the SLACK_BOT_TOKEN

### 6. Set Up xAI Grok API Access

1. Sign up for access to the xAI API at [x.ai/api](https://x.ai/api)
2. Generate an API key from your xAI dashboard
3. Copy your API key - you'll need this for the XAI_API_KEY

### 7. Set Up and Run the Bot

1. Clone this repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Create a `.env` file in the project root:
   ```
   SLACK_BOT_TOKEN=xoxb-your-bot-token
   SLACK_APP_TOKEN=xapp-your-app-token
   XAI_API_KEY=your-xai-api-key
   ```
4. Run the bot:
   ```
   python app.py
   ```
5. The bot should now be online and ready to respond!

## Usage

- Send a direct message to your bot
- Mention your bot in a channel using `@botname`

## Customization

You can customize the bot's behavior by modifying the following:

- The `ask_grok` function parameters (e.g., adjust temperature for more/less creative responses)
- Add conversation history tracking for more contextual responses
- Implement specific commands or workflows for your team's needs

## Deployment

For production deployment, consider:

- Using a proper hosting platform (Heroku, AWS, etc.)
- Setting up monitoring and error reporting
- Implementing rate limiting to manage API usage
- Using an HTTPS endpoint instead of Socket Mode
- Setting up a database for conversation history

## License

MIT