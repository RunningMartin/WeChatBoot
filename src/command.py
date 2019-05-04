import logging
from datetime import datetime

from src import config
from src.database import DataBase

logger = logging.getLogger(__name__)


def master_command(msg):
    """拥有者指令"""
    cmd = msg.text.split(config.INTERNAL)[0]
    if config.ADD_GROUP_ADMIN == cmd:
        add_group_admin(msg)
    if config.REMOVE_GROUP_ADMIN == cmd:
        remove_group_admin(msg)
    if config.ADD_LISTEN_GROUP == cmd:
        add_listen_group(msg)
    if config.REMOVE_LISTEN_GROUP == cmd:
        remove_listen_group(msg)
    administrator_command(msg)


def administrator_command(msg):
    """管理员指令"""
    cmd = msg.text.split(config.INTERNAL)[0]
    if config.COUNT_MEMBER_BY_DATA == cmd:
        count_member_by_data(msg)


def count_member_by_data(msg):
    """
    按日期统计发言成员
    命令格式:按日期统计发言成员 群组 起始日期 结束日期
    日期格式：2018-01-01
    :param msg:
    :return:
    """
    info = msg.text.split(config.INTERNAL)
    group = info[1]
    start = datetime.strptime(info[2], "%Y-%m-%d")
    end = datetime.strptime(info[3], "%Y-%m-%d")
    users = config.INTERNAL.join(DataBase.count_member_by_date(group, start, end))
    logger.info("统计群：{0} 从{1} 到 {2}期间发言的成员：{3}".format(group, start, end, users))

    msg.reply(users)


def add_listen_group(msg):
    """
    添加群组监听
    命令格式：添加群监听 群组名
    :param msg:
    :return:
    """
    info = msg.text.split(config.INTERNAL)
    group = msg.bot.groups().search(info[1])[0]
    logger.info("监听群：{0}".format(group.name))
    DataBase.add_listen_group(group.puid, group.name)
    msg.reply("监听群：{0}成功".format(group.name))


def remove_listen_group(msg):
    """
    移除群组监听
    命令格式：移除群监听 群组名
    :param msg:
    :return:
    """
    info = msg.text.split(config.INTERNAL)
    group = msg.bot.groups().search(info[1])[0]
    logger.info("移除群监听：{0}".format(group.name))
    DataBase.delete_listen_group(group.puid)
    msg.reply("移除群监听：{0}成功".format(group.name))


def add_group_admin(msg):
    """
    添加群管理员
    命令格式：添加群管理员 群名 管理员
    :param msg:
    :return:
    """
    info = msg.text.split(config.INTERNAL)
    chat_group = info[1]
    friend = msg.bot.friends().search(info[2])[0]
    logger.info("将{0}设置为群：{1}的群管理员".format(friend.name, chat_group))
    DataBase.add_admin(friend.puid, chat_group, friend.name)
    msg.reply("将{0}设置为群：{1}的群管理员 成功".format(friend.name, chat_group))


def remove_group_admin(msg):
    """
    删除群管理员
    命令格式：删除群管理员 群名 管理员
    :param msg:
    :return:
    """
    info = msg.text.split(config.INTERNAL)
    chat_group = info[1]
    friend = msg.bot.friends().search(info[2])[0]
    logger.info("从群：{0}移除{1}的群管理员权限".format(chat_group, friend.name))
    DataBase.delete_admin(friend.puid, chat_group)
    msg.reply("从群：{0}移除{1}的群管理员权限 成功".format(chat_group, friend.name))
