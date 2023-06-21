import discord
import pandas
import pandas as pd
import email.message
import smtplib
import asyncio


def funcao_le_arquivos(x: str, y: str, z: str):
    """
    :param x: nome da planilha que será lida
    :param y: nome da coluna
    :param z: valor a encontrar
    :return:
    """
    planilha = pd.read_csv(x)

    esta_presente = z in planilha[y].values

    if esta_presente:
        return True
    else:
        return False


############################
def enviar_email(destinatario, sequencia):
    # Configuracoes do servidor de e-mail
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    smtp_username = 'projeto.bot.discord.ifpb@gmail.com'
    smtp_password = 'ppjwpxvpprurppek'
    remetente = 'projeto.bot.discord.ifpb@gmail.com'

    # Cria o objeto de e-mail
    mensagem = 'Olá, \n\nSua sequência de verificação é: {}'.format(sequencia)

    # Conexão ao servidor do Gmail
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(smtp_username, smtp_password)

    # Envio do e-mail
    server.sendmail(remetente, destinatario, mensagem.encode('utf-8'))
    print('Email enviado com sucesso!')

    # Encerra a conexão ao servidor
    server.quit()


async def bane_usuario(member):
    usuario_id = member.id

    tempo_banimento = 60  # 1minuto

    mensagem = 'Opa! Infelizmente você tomou banimento do nosso servidor.\n' \
               'Nossos meios de contato:\n' \
               'E-mail: ccec.cg@ifpb.edu.br\n' \
               'Telefone: (83) 0000-0000\n' \
               'Presencial: Bloco X, Sala Y\n' \
               'Horários de atendimento: 8-11h e 14-17h'

    embed = discord.Embed(title='Vixe, tomou ban!',
                          description='Provavelmente você chegou ao limite de tentativas e por isso foi banido',
                          colour=65280)

    embed.add_field(name='Outros meios de contato', value='E-mail da coordenação: ccec.cg@ifpb.edu.br\nTelefone: '
                                                          '(83) 0000-0000\nPresencial: Bloco X, Sala Y\n'
                                                          'Horários de atendimento: 8-11h e 14-17h')

    if member is not None:
        await member.send(embed=embed)
        await member.guild.ban(member, reason='tempo limite')
        print(f'Usuario banido por {tempo_banimento} tempo')

        await asyncio.sleep(tempo_banimento)
        await member.guild.unban(member)
    else:
        print('Usuario nao encontrado')


async def distribui_cargos(member, email):
    guild = member.guild
    role_pretendente = discord.utils.get(guild.roles, name='Pretendente')
    if "@academico.ifpb.edu.br" in email:
        role = discord.utils.get(guild.roles, name='Aluno')
        if role is not None:
            # adiciona cargo de aluno
            await member.add_roles(role)
            await member.remove_roles(role_pretendente)
        else:
            print('cargo vazio')
    elif "@ifpb.edu.br" in email:
        role = discord.utils.get(guild.roles, name='Professor')
        if role is not None:
            # adiciona cargo de professor
            await member.add_roles(role)
            await member.remove_roles(role_pretendente)
        else:
            print('cargo vazio')



############### ASYNC OU NAO ASYNC ############## ?
def encontra_nome_planilha(email, planilha):
    tabela = pd.read_csv(planilha)

    # Colunas de Interesse
    c1 = ''
    if planilha == 'alunos.csv':
        c1 = 'E-mail academico'
    elif planilha == 'professores.csv':
        c1 = 'E-mail'
    c2 = 'Nome'

    email_conhecido = email
    nomes_coluna2 = tabela.loc[tabela[c1] == email_conhecido, c2].tolist()

    return nomes_coluna2[0]


async def altera_apelido(member, novo_apelido):
    try:
        await member.edit(nick=novo_apelido)
    except discord.Forbidden:
        print('Nao tenho permissao para alterar o apelido')
    except discord.HTTPException:
        print('Ocorreu um erro ao tentar alterar apelido')