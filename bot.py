import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import requests
import alpaca_trade_api as tradeapi

# -------------------------------
# ✅ Dummy API Keys (Replace later)
# -------------------------------
TELEGRAM_BOT_TOKEN = "8426287194:AAHdEzNJxgKNDZi4WT0k_KQ2t3x4jN3T6h4"
DEEPSEEK_API_KEY = "sk-cfcc27a39e5a4532bb049f2d144f4aca"
GEMINI_API_KEY = "AIzaSyAuDIbx-iiSnmeXtg0aflEScsZkkxm8u1M"
ALPACA_API_KEY = "PKTCVID12REA0E3KLS75"
ALPACA_SECRET_KEY = "icJP7KOumrWrh8LtMOhfD0nSeYfLv2jYwJuSGtbJ"
NEWSAPI_KEY = "92190bea-849c-4e45-913a-0c530537e71d"
BINANCE_API_KEY = "R7mMRIlpD6jVKemPMPDglZWV8cDCPoHT5J3o9svkJWolE9YjQwIZmlZF97ElCGVG"
BINANCE_SECRET_KEY = "2IDbEfEpTqkrgFxYq6ZUD8niFOpreO3oB9yftYFFzrkaZQFDEIJojn2ExggHZnWd"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# -------------------------------
# ✅ Basic Telegram Commands
# -------------------------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖 Hello! I am your Crypto AI Trading Bot. Use /news or /price BTC.")

async def news(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = f"https://newsapi.org/v2/everything?q=crypto&apiKey={NEWSAPI_KEY}"
    response = requests.get(url).json()
    if "articles" in response and response["articles"]:
        headlines = [a["title"] for a in response["articles"][:5]]
        await update.message.reply_text("📰 Top News:\n" + "\n".join(headlines))
    else:
        await update.message.reply_text("No news found.")

async def price(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) == 0:
        await update.message.reply_text("Usage: /price BTC")
        return
    symbol = context.args[0].upper()
    url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}USDT"
    response = requests.get(url).json()
    if "price" in response:
        await update.message.reply_text(f"💰 {symbol} Price: {response['price']} USDT")
    else:
        await update.message.reply_text("Invalid symbol or API error.")

# -------------------------------
# ✅ Main function
# -------------------------------
def main():
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("news", news))
    app.add_handler(CommandHandler("price", price))
    app.run_polling()

if __name__ == "__main__":
    main()
