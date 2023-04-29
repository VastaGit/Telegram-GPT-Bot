import asyncio
import os
import logging
import openai
from aiogram import Bot, Dispatcher, types, executor
from openai import api_key, Completion
from api_secret_key import TG_key, GPT_key

bot = Bot(token=TG_key)
dp = Dispatcher(bot)

openai.api_key = GPT_key

@dp.message_handler()
async def echo_message(message: types.Message):
    user_message = message.text

    prompt = user_message
    response = Completion.create(
        engine="text-davinci-001",
        prompt=prompt,
        max_tokens=100,
        stop=None,
    )
    response_text = response.choices[0].text.strip()

    await message.answer(response_text)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
