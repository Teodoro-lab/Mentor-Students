from dotenv import load_dotenv
import discord
from discord.ext import commands

from constants import USER_HELP_MSG, HELP_MANUAL

import os
import openai

load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')

intent = discord.Intents.default()
intent.message_content = True

bot = commands.Bot(command_prefix='bugo ', intents=intent)


def create_gtp_request() -> str:

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0301",
        messages=[
            {"role": "system", "content": "You are a schedulubg"},
            {"role": "user", "content": "Hello!"}
        ]
    )

    return completion.choices[0].message


@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')


@bot.command(name='helpme')
async def help(ctx):
    await ctx.send('HELP_MESSAGE')


@bot.command(name='msg')
async def send_message_to(ctx, user_id: int):
    print('sending msg')
    await ctx.send('Sending message!')
    user = await bot.fetch_user(user_id)
    await user.send(USER_HELP_MSG)


@bot.command()
async def list(ctx):
    """Display a list of options."""
    items = ['item1', 'item2', 'item3']
    embed = discord.Embed(title='List of items')

    for i, item in enumerate(items):
        embed.add_field(name=f'{i+1}. {item}', value='\u200b', inline=False)
    message = await ctx.send(embed=embed)

    for i in range(len(items)):
        await message.add_reaction(str(i+1)+'\u20e3')

    def check(reaction, user):
        return user == ctx.author and reaction.message == message and str(reaction.emoji) in [str(i+1)+'\u20e3' for i in range(len(items))]

    try:
        reaction, user = await bot.wait_for('reaction_add', timeout=60.0, check=check)
    except:
        await message.clear_reactions()
        return

    index = int(str(reaction.emoji)[0]) - 1
    selected_item = items[index]
    await ctx.send(f'You selected: {selected_item}')


@bot.command(name='checkstatus')
async def check_status(ctx, member: discord.Member):
    if member.status == discord.Status.online:
        await ctx.send(f"{member.name} is currently online.")
    else:
        await ctx.send(f"{member.name} is currently offline.")


bot.run(os.getenv('DISCORD_KEY'))
