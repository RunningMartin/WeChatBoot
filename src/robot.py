import logging

from wxpy import Bot, embed, Group, TEXT, SHARING, Friend

from src import config
from src.database import DataBase
from src.callback import qr_callback, logout_callback, login_callback
from src.mail import Mail
from src.logger import init_logger
from src.command import master_command, administrator_command

init_logger()
DataBase.init_database()
Mail.init_mail(user=config.EMAIL_USER, password=config.EMAIL_PASSWORD, host=config.EMAIL_HOST, port=config.EMAIL_PORT)
logger = logging.getLogger(__name__)

if config.LOGIN_TYPE == config.MAIL:

    bot = Bot(cache_path=True, qr_callback=qr_callback, login_callback=login_callback, logout_callback=logout_callback)

else:
    bot = Bot(cache_path=True, login_callback=login_callback, logout_callback=logout_callback)

bot.enable_puid()


@bot.register(chats=Group, msg_types=TEXT, except_self=False)
def group_message(msg):
    """
    处理群聊消息
    :param msg:
    :return:
    """
    if not config.IS_LISTEN_GROUP:
        return
    group = msg.chat.name
    sender = msg.member.name

    if group in DataBase.all_listen_group():
        DataBase.save_chat(group, sender, msg.receive_time.strftime("%Y-%m-%d %H:%M:%S"), msg.text)

    return


@bot.register(chats=Group, msg_types=SHARING, except_self=False)
def group_sharing(msg):
    """
    处理群分享
    :param msg:
    :return:
    """
    if not (config.IS_LISTEN_GROUP and config.IS_LISTEN_SHARING):
        return

    group = msg.chat.name
    if group not in DataBase.all_listen_group():
        return

    sender = msg.member.name
    msg.forward(bot.file_helper, prefix='【{0}】：【{1}】群成员【{2}】分享了：'.format(
        msg.receive_time.strftime("%Y-%m-%d %H:%M:%S"), group, sender))
    return


@bot.register(chats=bot.file_helper, msg_types=TEXT, except_self=False)
def master(msg):
    """
    处理文件助手传递过来的命令
    :param msg:
    :return:
    """
    master_command(msg)


@bot.register(chats=Friend, msg_types=TEXT, except_self=False)
def administrator(msg):
    """管理员命令"""
    admins = DataBase.all_admin()
    if msg.sender.puid in admins:
        administrator_command(msg)


embed()
