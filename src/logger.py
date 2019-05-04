import logging


def init_logger():
    logging.basicConfig(level=logging.DEBUG,
                        filename='WeChat.log',
                        datefmt='%Y-%m-%d %H:%M:%S',
                        format='%(asctime)s - %(name)s - %(levelname)s - %(lineno)d - %(module)s - %(message)s')


