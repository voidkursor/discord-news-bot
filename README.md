# Discord News Bot

A Discord bot that fetches and posts news from various categories.

## Setup

1. **Install Python** (if not installed): https://www.python.org/downloads/

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Create Discord Bot:**
   - Go to https://discord.com/developers/applications
   - Click "New Application"
   - Go to "Bot" section
   - Click "Reset Token" and copy it
   - Enable "Message Content Intent" in Bot settings

4. **Get News API Key (free):**
   - Go to https://newsapi.org/register
   - Register for free account
   - Copy your API key

5. **Set environment variables:**
```bash
export DISCORD_BOT_TOKEN="your_discord_token_here"
export NEWS_API_KEY="your_news_api_key_here"
```

6. **Run the bot:**
```bash
python bot.py
```

7. **Add bot to Discord server:**
   - Go to OAuth2 > URL Generator
   - Select "bot" scope
   - Select "Send Messages" permission
   - Copy generated URL and open it

## Commands

- `!news gaming` - Get gaming/tech news
- `!news politics` - Get political news
- `!news sports` - Get sports news
- `!news business` - Get business news
- `!news science` - Get science news
- `!helpnews` - Show help

## Deploy for Free

- **Render**: Push to GitHub, connect to Render, set env vars
- **Replit**: Create repl, add secrets, run always on
