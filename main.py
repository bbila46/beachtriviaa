import discord
from discord.ext import commands
import asyncio
import os

from aiohttp import web

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Minimal web server for uptime services (like Render or Replit)
async def handle(request):
    return web.Response(text="BeachTrivia Bot is running!")

async def start_web_app():
    app = web.Application()
    app.router.add_get("/", handle)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, port=int(os.environ.get("PORT", 8080)))
    await site.start()

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"✅ Logged in as {bot.user}")

async def main():
    async with bot:
        await bot.load_extension("trivia")
        await asyncio.gather(
            bot.start("YOUR_BOT_TOKEN"),  # Replace with your token
            start_web_app()
        )

asyncio.run(main())
