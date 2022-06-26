from icecream import ic
from dotenv import load_dotenv
from pathlib import Path
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class Config(object):
    LOG_LEVEL = ''
    SMTP_HOST = ''
    SMTP_USERNAME = ''
    SMTP_PASSWORD = ''


def read_config() -> Config:
    load_dotenv()
    env_path = Path('.')/'.env'
    load_dotenv(dotenv_path=env_path)

    config = Config()
    config.LOG_LEVEL = os.getenv("LOG_LEVEL")
    config.SMTP_HOST = os.getenv("SMTP_HOST")
    config.SMTP_USERNAME = os.getenv("SMTP_USERNAME")
    config.SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")

    return config


config = read_config()

if config.LOG_LEVEL != 'DEBUG':
    ic.disable()


def get_messages() -> list:
    # TODO: Тут можно дописать чтение из файла JSON
    messages = list()
    messages = [
        {
            "name": 'Артем',
            "email": 'root.of.system@gmail.com',
            "result": 24.50
        },
    ]
    return messages


def send_email(from_email: str = '', to: str = '', subject: str = '', message: str = '') -> int:

    global config

    if len(from_email) < 1:
        from_email = config.SMTP_USERNAME

    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = from_email
    msg['To'] = to
    msg.attach(MIMEText(message, 'plain'))

    server = smtplib.SMTP(config.SMTP_HOST)
    server.starttls()
    server.login(config.SMTP_USERNAME, config.SMTP_PASSWORD)

    server.sendmail(msg['From'], msg['To'], msg.as_string())

    server.quit()

    return 0


if __name__ == "__main__":

    messages = get_messages()

    for msg in messages:
        ic(msg)
        subject = 'codereview task#2'
        message_text = f"Привет, {msg['name']}, твой результат {msg['result']}"
        try:
            send_email(to=msg['email'], subject=subject, message=message_text)
            ic(f"Successfully sent email message to {msg['email']}")
        except(RuntimeError, TypeError, NameError):
            print("Oops!  Что-то пошло не так")
