import email.message
import smtplib


def enviar_email(destinatario, sequencia):
    # Configuracoes do servidor de e-mail
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    smtp_username = 'gustavosymoons@gmail.com'
    smtp_password = 'agqgxkvjelcwvgky'
    remetente = 'gustavosymoons@gmail.com'

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
