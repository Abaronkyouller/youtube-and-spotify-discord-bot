import aiosqlite
import discord
from discord.ext import commands
import os
from commands import buy_stock
from database import seed_stocks, setup_database
from test_youtube import find_youtube_links
from dotenv import load_dotenv
load_dotenv()
from discord.ext import commands

from discord.ext import tasks
from market import update_market
import asyncio
from datetime import datetime, timedelta


TOKEN = os.getenv("DISCORD_BOT_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!!", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.command()
async def play(ctx, *, args):
    links = find_youtube_links(args)
    result = "\n".join(links)
    await ctx.send(result)

@bot.command()
async def dm(ctx, user:  discord.Member, text: str):
    await user.send(text)


@bot.command()
async def mdm(ctx, users: commands.Greedy[discord.Member], text: str):
    for user in users:
        await user.send(text)

@bot.command()
async def adm(ctx, user:  discord.Member,  time_str: str, *, text: str):

    # parse HH:MM
    target_time = datetime.strptime(time_str, "%H:%M").time()

    now = datetime.now()

    send_time = now.replace(
        hour=target_time.hour,
        minute=target_time.minute,
        second=0,
        microsecond=0
    )

    # if time already passed today -> tomorrow
    if send_time < now:
        send_time += timedelta(days=1)

    wait_seconds = (send_time - now).total_seconds()

    await ctx.send(f"Message scheduled for {send_time}")

    await asyncio.sleep(wait_seconds)

    await user.send(text)

@tasks.loop(minutes=60)
async def market_loop():
    await update_market()

@bot.command()
async def stock(ctx, users: commands.Greedy[discord.Member]):
    await setup_database()
    await seed_stocks()
    market_loop.start()

@bot.command()
async def buy(ctx, stock_name: str, amount: int):

    result = await buy_stock(
        ctx.author.id,
        stock_name.upper(),
        amount
    )

    await ctx.send(result)

@bot.command()
async def portfolio(ctx):

    async with aiosqlite.connect("stocks.db") as db:

        cursor = await db.execute("""
        SELECT stock_name, shares
        FROM portfolio
        WHERE user_id = ?
        """, (ctx.author.id,))

        items = await cursor.fetchall()

        if not items:
            await ctx.send("You own no stocks.")
            return

        text = ""

        for stock, shares in items:
            text += f"{stock}: {shares} shares\n"

        await ctx.send(text)

bot.run(TOKEN)