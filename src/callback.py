import logging
from src import config
from src.mail import Mail

logger = logging.getLogger(__name__)


def qr_callback(uuid, status, qrcode):
    with open(config.QR_PATH, 'wb') as file:
        file.write(qrcode)

    contents = [u"请扫描二维码", config.QR_PATH]
    Mail.send_email(to=config.ACCEPT_EMAIL, title="微信登录二维码扫描", contents=contents)
    logger.info("scan qr")
    return


def login_callback():
    contents = [u"登录成功"]
    Mail.send_email(to=config.ACCEPT_EMAIL, title="微信登录状态", contents=contents)
    logger.info("login success")


def logout_callback():
    contents = [u"退出成功"]
    Mail.send_email(to=config.ACCEPT_EMAIL, title="微信登录状态", contents=contents)
    logger.info("loginout")
