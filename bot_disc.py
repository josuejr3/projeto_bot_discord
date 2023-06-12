import asyncio
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
###### FUNCAO QUE LIGA O BOT #########
async def on_ready():
    print(f'{bot.user.name} está online')


@bot.event
########## FUNCAO PARA VERIFICAR SE A MENSAGEM NAO É DO PROPRIO BOT ##########
async def on_message(message):
    if message.author == bot.user:
        return



    await bot.process_commands(message) #processse todos os comandos

@bot.command(name="ajuda")
######## COMANDO PARA EXPLICACAO NO SERVIDOR ########
async def send_hello(ctx):
    name = ctx.author.name
    response = "Olá " + name + f", me chamo {bot.user.name[:6]} sou responsavel pelo gerenciamento do servidor do curso de Engenharia de Computação do IFPB - CG." \
                               f" Para que você tenha acesso ao restante dos canais de comunicação é necessário que você seja aluno do curso, para realizar a verificação" \
                               f" digite o comando !verificao no campo de texto abaixo"

    await ctx.send(response)

@bot.event
######## FUNCAO PARA DAR CARGO DE PRETENDENTE #########
async def on_member_join(member):
    guild = member.guild
    role = discord.utils.get(guild.roles, name='Pretendente')

    if role is not None:
        await member.add_roles(role)
        print(f'Added role {role.name} to {member.name}')
    else:
        print(f'Role not found in server {guild.name}. Make sure the role exists.')

########################### VERIFICACAO DE EMAIL #########################
@bot.command(name="verificacao")
# comando de verificao de email
async def verification(ctx):
    await ctx.send('"Ok, para realizar a verificação peço que evie o seu email institucioal abaixo no padrão" \
               " seuemaildealuno@academico.ifpb.edu.br se for estudante ou seuemaildeprofessor@ifpb.edu.br caso seja professor"')

    def check(message):
        return message.author == ctx.author and message.channel == ctx.channel

    tentativas = 0
    email = ""
    while True:
        if tentativas == 3:
            break
        else:
            try:
                resposta = await bot.wait_for('message',  check=check, timeout=30)
                if "@academico.ifpb.edu.br" in resposta.content or "@ifpb.edu.br" in resposta.content:
                    email = resposta.content
                    await ctx.send(f'Ok, irei verificar o e-mail enviado em nosso bando de dados')
                    break
                else:
                    await ctx.send(f'Ocorreu um erro, provavelmente o e-mail informado não consta no nosso banco de dados')
            except asyncio.TimeoutError:
                await ctx.send('Ocorreu um erro, tente novamente!')
            tentativas += 1


bot.run(TOKEN)