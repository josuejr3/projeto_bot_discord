import asyncio
import discord
from key import token
from discord.ext import commands, tasks
import pandas
import pandas as pd
import openpyxl
import random
from funcoes.enviar_email import enviar_email
from funcoes.encontra_nome import encontra_nome

TOKEN = token.get('TOKEN')


CANAL_ID = 1116925952031719435 # ID DO CANAL DE AUTENTICAÇÃO
GUILD_ID = 1116672058353516614 # ID DO SERVIDOR
ROLE_ID = 1116702722318684161 # ID DO CARGO - PRETENDENTE


intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(intents=intents, command_prefix="!")


class VerificacaoState:
    def __init__(self, email):
        self.email = email
        self.codigo = None

@bot.event
###### FUNCAO QUE LIGA O BOT #########
async def on_ready():
    print(f'{bot.user.name} está online')


@bot.event
########## FUNCAO PARA VERIFICAR SE A MENSAGEM NAO É DO PROPRIO BOT ##########
async def on_message(message):
    if message.author == bot.user:
        return

    if message.channel.id == CANAL_ID:
        await bot.process_commands(message) #processse todos os comandos


@bot.event
######## FUNCAO PARA DAR CARGO DE PRETENDENTE #########
async def on_member_join(member):
    guild = member.guild
    role = discord.utils.get(guild.roles, name='Pretendente')
    channel = discord.utils.get(guild.channels, name='canal-de-autenticação')
    usuario = member.name
    mensagem = f'Olá {usuario}, me chamo {bot.user.name[:6]} e sou responsavel pelo gerenciamento do sevidor do curso de Engenharia de Computação do IFPB - CG aqui no Discord.\n' \
               f'Para que você tenha acesso ao restante de nossos canais de comunicação é necessário que você esteja vinculado ao curso e a Instituição, para realizar sua verificação ' \
               f'basta digitar no campo de texto abaixo "!verificacao" que faremos todo o passo a passo :)'
    await channel.send(mensagem)


    if role is not None:
        await member.add_roles(role)
        print(f'Added role {role.name} to {member.name}')
    else:
        print(f'Role not found in server {guild.name}. Make sure the role exists.')



########################### VERIFICACAO DE EMAIL #########################
@bot.command(name="verificacao")
# comando de verificao de email
async def verification(ctx):
    await ctx.send('Ok, para realizarmos a verificação preciso que você digite o seu e-mail acadêmico nos seguintes modelos\n'
                   'Para alunos: exemplo@academico.ifpb.edu.br\nPara professores: exemplo@ifpb.edu.br')

    def check(message):
        return message.author == ctx.author and message.channel == ctx.channel

    tentativas = 0
    email = ""
    while True:
        if tentativas == 3:
            break
        else:
            try:
                resposta = await bot.wait_for('message',  check=check, timeout=300)
                if "@academico.ifpb.edu.br" in resposta.content or "@ifpb.edu.br" in resposta.content:
                    email = resposta.content
                    await ctx.send(f'Ok, irei verificar o e-mail enviado em nosso banco de dados')

                    lista_alunos = pd.read_excel('alunos.xlsx')
                    lista_professores = pd.read_excel('professores.xlsx')
                    codigo_verificacao = {}

                    email_a_verificar = str(email)

                    verificacao = email_a_verificar in lista_alunos['E-mail academico'].values or email_a_verificar in lista_professores['E-mail'].values

                    if verificacao == True:

                        # GERA UM CODIGO DE VERIFICAÇÃO DE 6 DIGITOS
                        sequencia = ''.join(random.choices('0123456789', k=6))

                        # ENVIA O CÓDIGO DE VERIFICACAO PARA O E-MAIL
                        enviar_email(email_a_verificar, sequencia)

                        # SALVA O CÓDIGO DE AUTENTICAÇÃO E O E-MAIL
                        codigo_verificacao[email] = VerificacaoState(email)
                        codigo_verificacao[email].codigo = sequencia


                        # ENVIA MENSAGEM NO DISCORD INFORMANDO QUE O CODIGO FOI ENVIADO PARA O EMAIL.
                        mensagem_enviada_email = f"O código de autenticação foi enviado para o E-mail: {email_a_verificar}. Insira o código abaixo para verificação"
                        await ctx.send(mensagem_enviada_email)

                        # FUNÇÃO QUE VERIFICA MENSAGEM

                        def verificar_mensagem(m):
                            return m.author == ctx.author and m.channel == ctx.channel



                        # Tentativas de verificação
                        try:
                            # Espera de resposta do usuário com o código de autenticação, tempo limite de dois minutos
                            mensagem_a_confirmar = await bot.wait_for('message', check=verificar_mensagem, timeout=60)
                        except asyncio.TimeoutError:
                            mensagem = "Tempo limite excedido. Verificação cancelada."
                            await ctx.send(mensagem)
                            return


                        # Codigo recebido no chat
                        codigo = mensagem_a_confirmar.content


                        # Verificação do código recebido

                        if codigo_verificacao[email].codigo == codigo:
                            mensagem = f"Autenticação bem sucedida para o e-mail {email}"
                            del codigo_verificacao[email]
                            break
                        else:
                            mensagem = f'Código incorreto, autenticação falha para o e-mail {email}'

                        await ctx.send(mensagem)
                        return
                    else:
                        print('Ocorreu um erro, e-mail não existe ou foi digitado de forma incorreta, tente novamente.')


                else:
                    await ctx.send(f'Ocorreu um erro, provavelmente o e-mail informado não consta no nosso banco de dados')
            except asyncio.TimeoutError:
                await ctx.send('Ocorreu um erro, tente novamente!')
        tentativas += 1

    async def remover_cargo(ctx, emails):
        guild = ctx.guild
        role = discord.utils.get(guild.roles, id=ROLE_ID)
        member = ctx.author

        if role is not None:
            await member.remove_roles(role)

    async def add_cargo_definitivo(ctx, emails, id_cargo):
        guild = ctx.guild
        role = discord.utils.get(guild.roles, id=id_cargo)
        member = ctx.author

        if role is not None:
            await member.add_roles(role)



    # Envia mensagem no privado
    async def envia_msg_pv(ctx):
        usuario_id = ctx.author.id

        usuario = bot.get_user(usuario_id)

        if usuario is None:
            print('Nao foi possivel encontrar usuario')
        else:
            await usuario.send('Infelizmente você ultrapassou o limite de tentativas para verificação.\n'
                               'Por esse motivo você foi banido do servidor. Para resolver o problema entre em contato com a coordenação do curso\n'
                               'Telefone: (83) 0000-0000\n'
                               'E-mail: ccec.cg@ifpb.edu.br\n'
                               'Presencial: Bloco X, Sala Y\n'
                               'Horários de atendimento: 7-11h e 14-17h')


    async def bane_usuario(ctx):
        usuario_id = ctx.author.id
        try:
            user = await bot.fetch_user(usuario_id)
            await ctx.guild.ban(user, reason='tempo limite')
        except discord.NotFound:
            print('Usuario nao encontrado')



    async def altera_apelido(ctx, member: discord.Member, *, novo_apelido):
        try:
            await member.edit(nick=novo_apelido)
        except discord.Forbidden:
            print('Nao tenho permissao para alterar o apelido')
        except discord.HTTPException:
            print('Ocorreu um erro ao tentar alterar apelido')


    if tentativas == 3:
        # enviar msg no privado colocando dados da coordenação para entrar em contato
        await envia_msg_pv(ctx)
        await bane_usuario(ctx)
        print('ban')
    else:
        await remover_cargo(ctx, email)
        planilha = ''
        if "@academico.ifpb.edu.br" in email:
            id_aluno = 1116710660894638182 # id cargo do aluno
            planilha = 'alunos.xlsx'
            await add_cargo_definitivo(ctx, email, id_aluno)
        elif "@ifpb.edu.br" in email:
            id_professor = 1116709968045940797
            planilha = 'professores.xlsx' # id cargo do professor
            await add_cargo_definitivo(ctx, email, id_professor)
        nome = encontra_nome(email, planilha)
        member = ctx.author
        await altera_apelido(ctx, member, novo_apelido=nome)


bot.run(TOKEN)