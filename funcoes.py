import pandas
import pandas as pd
import email.message
import smtplib

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
