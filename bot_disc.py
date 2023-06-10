import discord
from key import token
from discord.ext import commands, tasks
TOKEN = token.get('TOKEN')

GUILD_ID = 1116672058353516614 # ID DO SERVIDOR
ROLE_ID = 1116702722318684161 # ID DO CARGO - PRETENDENTE


intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(intents=intents, command_prefix="!")


@bot.event
async def on_ready():
    print(f'{bot.user.name} está online')


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    await bot.process_commands(message) #processse todos os comandos

@bot.command(name="ajuda")
# comando para explicação do servidor
async def send_hello(ctx):
    name = ctx.author.name
    response = "Olá " + name + f", me chamo {bot.user.name[0:6]} e preciso que você me forneça o seu e-mail academico" \
                               f" para que possamos verificar se você é aluno de Engenharia de Computação do IFPB de Campina Grande"

    await ctx.send(response)

@bot.event
async def on_member_join(member):
    guild = member.guild
    role = discord.utils.get(guild.roles, name='Pretendente')

    if role is not None:
        await member.add_roles(role)
        print(f'Added role {role.name} to {member.name}')
    else:
        print(f'Role not found in server {guild.name}. Make sure the role exists.')

bot.run(TOKEN)