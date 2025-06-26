import discord
from discord.ext import commands
import os
import requests

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

FINMIND_TOKEN = os.getenv("FINMIND_TOKEN")

def get_stock_price(stock_id):
    url = "https://api.finmindtrade.com/api/v4/data"
    params = {
        "dataset": "TaiwanStockPrice",
        "data_id": stock_id,
        "start_date": "2025-06-25",
        "token": FINMIND_TOKEN
    }
    response = requests.get(url, params=params)
    data = response.json()

    if data["status"] != 200 or not data["data"]:
        return f"❌ 查不到 {stock_id} 的資料"

    latest = data["data"][-1]
    return (f"📈 股票代號：{stock_id}\n"
            f"日期：{latest['date']}\n"
            f"收盤價：{latest['close']} 元\n"
            f"漲跌：{latest['change']} 元\n"
            f"開盤：{latest['open']}，最高：{latest['max']}，最低：{latest['min']}")

@bot.event
async def on_ready():
    print(f"🤖 Bot 已上線：{bot.user}")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content.startswith("!"):
        stock_id = message.content[1:]
        result = get_stock_price(stock_id)
        await message.channel.send(result)

    await bot.process_commands(message)

bot.run(os.getenv("DISCORD_TOKEN"))
