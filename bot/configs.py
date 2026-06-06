import os

from dotenv import load_dotenv

load_dotenv()

CLIENT_URL: str = str(os.getenv("CLIENT_URL"))
TELEGRAM_BOT_TOKEN: str = str(os.getenv("TELEGRAM_BOT_TOKEN"))
WHITELIST: set = set(str(os.getenv("WHITELIST")).split(","))
PROXY_URL: str = os.getenv("PROXY_URL")

if __name__ == "__main__":
    print(CLIENT_URL)
    print(TELEGRAM_BOT_TOKEN)
    print(WHITELIST)
