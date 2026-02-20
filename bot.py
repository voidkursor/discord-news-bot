import discord
from discord.ext import commands, tasks
import requests
import os
from datetime import datetime
import asyncio
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

NEWS_API_KEY = os.getenv('NEWS_API_KEY', 'demo')

SCHEDULED_CHANNEL_ID = os.getenv('CHANNEL_ID')  # Set this for auto-posting

CATEGORIES = {
    'gaming': 'technology',
    'tech': 'technology',
    'politics': 'politics',
    'business': 'business',
    'science': 'science',
    'sports': 'sports',
    'entertainment': 'entertainment',
    'general': 'top'
}

@bot.event
async def on_ready():
    print(f'Bot is ready as {bot.user}')
    daily_news.start()

@tasks.loop(minutes=1)
async def daily_news():
    now = datetime.now()
    
    # Post at 6:00 AM every day
    if now.hour == 6 and now.minute == 0:
        channel_id = os.getenv('CHANNEL_ID')
        if channel_id:
            try:
                channel = bot.get_channel(int(channel_id))
                if channel:
                    await post_gaming_news(channel)
            except Exception as e:
                logger.error(f"Error posting daily news: {e}")

async def post_gaming_news(channel):
    try:
        url = f'https://newsdata.io/api/1/latest?apikey={NEWS_API_KEY}&category=technology&country=in'
        response = requests.get(url)
        data = response.json()
        
        if data.get('status') != 'success':
            return
        
        articles = data.get('results', [])[:5]
        
        if not articles:
            return
        
        embed = discord.Embed(
            title=f"📰 Good Morning! Latest Gaming & Tech News",
            color=discord.Color.blue(),
            timestamp=datetime.now()
        )
        
        for i, article in enumerate(articles, 1):
            title = article.get('title', 'No title')
            desc = article.get('description', 'No description')
            url = article.get('url', '')
            
            if title:
                embed.add_field(
                    name=f"{i}. {title[:100]}",
                    value=f"{desc[:150]}... [Read more]({url})" if desc else f"[Read more]({url})",
                    inline=False
                )
        
        await channel.send(embed=embed)
        
    except Exception as e:
        logger.error(f"Error fetching gaming news: {e}")

@bot.command()
async def setchannel(ctx):
    """Set the channel for daily news posting"""
    os.environ['CHANNEL_ID'] = str(ctx.channel.id)
    await ctx.send(f"✅ Daily news will be posted in this channel ({ctx.channel.mention}) at 6 AM!\n"
                   f"⚠️ Note: Set CHANNEL_ID environment variable for persistent configuration.")

@bot.command()
async def news(ctx, category='general', *, country='in'):
    category = category.lower()
    news_category = CATEGORIES.get(category, 'top')
    
    try:
        url = f'https://newsdata.io/api/1/latest?apikey={NEWS_API_KEY}&category={news_category}&country=in'
        response = requests.get(url)
        data = response.json()
        
        if data.get('status') != 'success':
            await ctx.send(f"Error: {data.get('message', 'Unknown error')}")
            return
        
        articles = data.get('results', [])[:5]
        
        if not articles:
            await ctx.send(f"No news found for {category}")
            return
        
        embed = discord.Embed(
            title=f"📰 Latest {category.title()} News",
            color=discord.Color.blue(),
            timestamp=datetime.now()
        )
        
        for i, article in enumerate(articles, 1):
            title = article.get('title', 'No title')
            desc = article.get('description', 'No description')
            url = article.get('url', '')
            
            if title:
                embed.add_field(
                    name=f"{i}. {title[:100]}",
                    value=f"{desc[:150]}... [Read more]({url})" if desc else f"[Read more]({url})",
                    inline=False
                )
        
        await ctx.send(embed=embed)
        
    except Exception as e:
        await ctx.send(f"Error fetching news: {str(e)}")

@bot.command()
async def helpnews(ctx):
    embed = discord.Embed(
        title="📱 News Bot Commands",
        color=discord.Color.green()
    )
    embed.add_field(name="!news gaming", value="Get latest gaming/tech news", inline=False)
    embed.add_field(name="!news politics", value="Get latest political news", inline=False)
    embed.add_field(name="!news sports", value="Get latest sports news", inline=False)
    embed.add_field(name="!news business", value="Get latest business news", inline=False)
    embed.add_field(name="!news science", value="Get latest science news", inline=False)
    embed.add_field(name="Available categories", value="gaming, tech, politics, business, science, sports, entertainment", inline=False)
    await ctx.send(embed=embed)

@bot.command()
async def ping(ctx):
    await ctx.send(f'Pong! Latency: {round(bot.latency * 1000)}ms')

@bot.command()
async def testdaily(ctx):
    """Test the daily news posting"""
    await post_gaming_news(ctx.channel)
    await ctx.send("✅ Test daily news posted!")

@bot.command()
async def morningnews(ctx):
    """Get morning gaming/tech news"""
    await post_gaming_news(ctx.channel)

if __name__ == '__main__':
    import threading
    from http.server import HTTPServer, BaseHTTPRequestHandler
    
    class HealthCheckHandler(BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'OK')
        def log_message(self, format, *args):
            pass
    
    def run_server():
        port = int(os.getenv('PORT', 5000))
        server = HTTPServer(('0.0.0.0', port), HealthCheckHandler)
        server.serve_forever()
    
    threading.Thread(target=run_server, daemon=True).start()
    
    TOKEN = os.getenv('DISCORD_BOT_TOKEN')
    if not TOKEN:
        print("Error: DISCORD_BOT_TOKEN not set in environment variables")
        print("Get your token from https://discord.com/developers/applications")
    else:
        bot.run(TOKEN)
