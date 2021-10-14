import sys
from loguru import logger
import logging
import click

kLOGLEVEL = 25


class __loguruFlaskHandler(logging.Handler):
    def emit(self, record):
        # Retrieve context where the logging call occurred, this happens to be in the 6th frame upward
        logger_opt = logger.opt(depth=6, exception=record.exc_info)
        msg = click.unstyle((record.getMessage().strip(" * ").rstrip(' -')))
        if ' - - ' in msg:
            logger_opt.log("FLASK_ERR" if record.exc_info else "FLASK",
                           '{} {}'.format(msg[0:msg.find(' - - ')], msg[msg.find('"'):]))
        else:
            logger_opt.log("FLASK_ERR" if record.exc_info else "FLASK", msg)


def setupLogger(logfilePath='logs/events.log',
                level='DEBUG',
                flaskApp=None):

    termFormat = "[<fg 248>{time:YYYY-MM-DD HH:mm:ss.SSS}</fg 248>] "\
                 "[<level>{level}</level>]\t"\
                 "<fg 222>{name}</fg 222>:<fg 222>{function}</fg 222>:<fg 222>{line}</fg 222> "\
                 "<level>{message}</level>"

    fileFormat = click.unstyle(termFormat)

    logger.remove()

    # logger.add(sys.stdout, format=termFormat, level=kLOGLEVEL)
    logger.add(sys.stderr, format=termFormat, level=kLOGLEVEL)

    logger.add(
        logfilePath,
        level=kLOGLEVEL,
        format=fileFormat,
        backtrace=False,
        rotation='1 MB',
        retention="1 week"
    )

    if flaskApp:
        logger.level("FLASK", 11, color="<fg 252><bold>")
        logger.level("FLASK_ERR", 41, color="<red><bold>")
        flaskApp.logger.addHandler(__loguruFlaskHandler())
        logging.basicConfig(handlers=[__loguruFlaskHandler()], level=kLOGLEVEL)

    return logger
