# bot.py
import os
import replicate

import discord
import discord.gateway
from dotenv import load_dotenv
from pathlib import Path

load_dotenv(Path('.venv\keys.env'))

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

def llm(message_content) -> str:
    input = {
    "top_p": 0.9,
    "prompt": f"Do you think the joke response 'That's what she said!' would be a comedic response to the message: {message_content}. your answer should be one word YES or NO. A response of that's what she said is usually funny when the message relates to size, girth, depth, hardness, wetness, or tightness of an object.",
    "min_tokens": 0,
    "temperature": 0.6,
    "prompt_template": "<|begin_of_text|><|start_header_id|>system<|end_header_id|>\n\nYou are a funny assistant that only replies with YES or NO and gives no context as to why you chose your answer<|eot_id|><|start_header_id|>user<|end_header_id|>\n\n{prompt}<|eot_id|><|start_header_id|>assistant<|end_header_id|>\n\n",
    "presence_penalty": 1.15
    }

    for event in replicate.stream(
        "meta/meta-llama-3-70b-instruct",
        input=input
    ):
        return(str(event))

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.event
async def on_message(message: discord.Message):
    if message.channel.name == 'general' and message.author.name != 'SarahBot':
        print(message.content)
        print(message.author.name)
        a = llm(str(message.content))
        print(a)
        if a.upper() == "YES":
            await message.channel.send("That's what she said!")


discord_key = os.getenv('DISCORD_API_TOKEN')

client.run(discord_key)
