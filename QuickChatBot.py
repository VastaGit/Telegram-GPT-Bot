from api_secret_key import TG_key, GPT_key
import asyncio
import os
import logging
from aiogram import Bot, Dispatcher, types, executor
import openai

openai.api_key = GPT_key
bot = Bot(token=TG_key)
dp = Dispatcher(bot)

# Create a dictionary to store conversation context
conversation_context = {}

# Handle incoming messages
@dp.message_handler()
async def echo_message(message: types.Message):
    # Get the user's message
    user_message = message.text

    # Check if the user has asked multiple questions
    questions = user_message.split('?')

    # Loop through each question and generate a response
    for question in questions:
        # Remove any leading or trailing whitespace
        question = question.strip()

        # Check if this is a follow-up question
        if message.chat.id in conversation_context:
            # Get the previous message's question and answer
            prompt = f"{conversation_context[message.chat.id]['question']}\n{question}"
            response = openai.Completion.create(
                engine="davinci",
                prompt=prompt,
                max_tokens=100,
                n=1,
                stop=None,
                temperature=0.7,
            )
            response_text = response.choices[0].text.strip()

            # Store the current question and answer in the conversation context
            conversation_context[message.chat.id]['question'] = prompt
            conversation_context[message.chat.id]['answer'] = response_text

            # Send the response back to the user
            await message.answer(response_text)
        else:
            # Generate a response using the GPT-3 API
            prompt = question
            response = openai.Completion.create(
                engine="davinci",
                prompt=prompt,
                max_tokens=6,
                n=1,
                stop=None,
                temperature=0.3,
            )
            response_text = response.choices[0].text.strip()

            # Store the current question and answer in the conversation context
            conversation_context[message.chat.id] = {'question': prompt, 'answer': response_text}

            # Send the response back to the user
            await message.answer(response_text)

if __name__ == '__main__':
    # Start the bot
    executor.start_polling(dp, skip_updates=True)
