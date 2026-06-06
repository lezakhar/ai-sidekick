import aiohttp

from collections import defaultdict
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.client.session.aiohttp import AiohttpSession

import configs


class TelegramBot:
    def __init__(self):
        self.bot = Bot(
            token=configs.TELEGRAM_BOT_TOKEN,
            session=AiohttpSession(proxy=configs.PROXY_URL if configs.PROXY_URL else None),
        )
        self.dp = Dispatcher()
        self.user_processing: dict = defaultdict(bool)

    async def user_allowed(self, user_name: str) -> bool:
        if user_name in configs.WHITELIST:
            return True

        return False

    async def api_request(
        self,
        endpoint: str,
        user_id: int,
        user_name: str,
        user_query: str,
    ) -> dict:
        if not await self.user_allowed(user_name):
            return {"answer": "Please contact your administrator for access."}

        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{configs.CLIENT_URL}{endpoint}",
                json={
                    "user_id": user_id,
                    "user_query": user_query,
                },
            ) as resp:
                return await resp.json()

    async def get_answer(
        self,
        user_id: int,
        user_name: str,
        user_query: str,
    ) -> str:
        result = await self.api_request(
            endpoint="/chat",
            user_id=user_id,
            user_name=user_name,
            user_query=user_query,
        )
        answer = result.get("answer", "Error processing request")

        return answer

    async def clear_context(self, user_id: int, user_name: str) -> str:
        result = await self.api_request(
            endpoint="/clear_context",
            user_id=user_id,
            user_name=user_name,
            user_query="",
        )
        return result.get("answer", "Error clearing context")

    async def handle_clear_context(self, message: types.Message):
        user_id = message.from_user.id
        user_name = message.from_user.username

        answer = await self.clear_context(user_id, user_name)
        await message.answer(answer)

    async def handle_message(self, message: types.Message):
        user_id = message.from_user.id
        user_name = message.from_user.username

        if self.user_processing[user_id]:
            await message.answer("Please wait while I process a previous request😊")
            return

        self.user_processing[user_id] = True

        try:
            answer = await self.get_answer(
                user_id=user_id,
                user_name=user_name,
                user_query=str(message.text),
            )
            await message.answer(
                answer,
                parse_mode=None,
            )
        finally:
            self.user_processing[user_id] = False

    def setup_handlers(self):
        self.dp.message.register(self.handle_clear_context, Command("clear_context"))
        self.dp.message.register(self.handle_message)

    async def start_polling(self):
        self.setup_handlers()
        await self.dp.start_polling(self.bot)


async def main():
    bot_instance = TelegramBot()
    await bot_instance.start_polling()


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
