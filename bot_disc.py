import discord
from key import token
from discord.ext import commands, tasks
TOKEN = token.get('TOKEN')

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(intents=intents, command_prefix="!")

@bot.event
async def on_redy():
    print(f'{bot.user} está online')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return


    await bot.process_commands(message) # processe todos os comandos

@bot.command(name="ajuda")
# COMANDO PARA EXPLICAÇÃO
async def send_hello(ctx):
    name = ctx.author.name
    response = "Olá " + name + f", me chamo {bot.user.name[0:6]} e preciso que me forneça seu e-mail academico" \
                               f" para que possamos verificar se você é aluno de Engenharia da Computação do IFPB de Campina Grande"

    await ctx.send(response)

bot.run(TOKEN)