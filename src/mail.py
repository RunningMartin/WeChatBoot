#!/usr/bin/python
# -*- coding: UTF-8 -*-
import logging

import yagmail

logger = logging.getLogger(__name__)


class Mail(object):
    mail = None

    def __init__(self, user, password, host, port):
        self._host = host
        self._port = port
        self._user = user
        self._password = password
        self._mail = yagmail.SMTP(user=self._user, password=self._password, host=self._host, port=self._port)

    def send(self, to, title, contents):
        self._mail.send(to=to, subject=title, contents=contents)

    @classmethod
    def init_mail(cls, user, password, host, port):
        logger.info("init mail config")
        logger.info("user:{0}".format(user))
        logger.info("host:{0}".format(host))
        logger.info("port:{0}".format(port))

        cls.mail = Mail(user=user, password=password, host=host, port=port)

    @classmethod
    def send_email(cls, to, title, contents):
        logger.info("send email")
        logger.info("to:{0}".format(to))
        logger.info("title:{0}".format(title))
        logger.info("contents:{0}".format(contents))

        cls.mail.send(to, title, contents)
