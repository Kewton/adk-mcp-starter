import logging
import logging.config
import os
import logging
import logging.config
import time
import inspect
from core.config import settings


# ログセットアップが実行されたかを保持するフラグ
logging_setup_done = False


def setup_logging():
    global logging_setup_done
    if logging_setup_done:
        return  # すでに実行済みなら何もしない
    else:
        print("setup_logging start")

    log_level = settings.LOG_LEVEL
    log_dir = settings.LOG_DIR

    # ディレクトリが存在しない場合は作成
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
        print(f"Directory {log_dir} created.")
    else:
        print(f"Directory {log_dir} already exists.")

    # ログ設定の定義
    log_config = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            '_formatter': {
                'format': '[%(process)d-%(thread)d]-%(asctime)s-%(levelname)s-%(message)s'
            },
        },
        'handlers': {
            'rotatinghandler': {
                'class': 'logging.handlers.RotatingFileHandler',
                'level': log_level,
                'formatter': '_formatter',
                'filename': os.path.join(log_dir, 'app.log'),
                'mode': 'a',
                'maxBytes': 1024 * 1024,
                'backupCount': 5,
                'encoding': 'utf-8',
            },
            'timedrotatinghandler': {
                'class': 'logging.handlers.TimedRotatingFileHandler',
                'level': 'ERROR',
                'formatter': '_formatter',
                'filename': os.path.join(log_dir, 'rotation.log'),
                'when': 'S',  # 秒ごとのローテーション
                'interval': 1,  # ローテーション間隔
                'backupCount': 5,
                'encoding': 'utf-8',
            }
        },
        'loggers': {
            '': {  # root logger
                'level': log_level,
                'handlers': ['rotatinghandler', 'timedrotatinghandler'],
            },
        }
    }
    

    # ログ設定を適用
    logging.config.dictConfig(log_config)
    logging.info("Logging is set up.")
    
    # 実行フラグをTrueに設定
    logging_setup_done = True


def getlogger():
    return logging.getLogger(__name__)


def setfileConfig(_path):
    logging.config.fileConfig(fname=_path)


def declogger(func):
    curframe = inspect.currentframe()
    calframe = inspect.getouterframes(curframe, 3)
    fn = calframe[1][1].split("/")
    filename = fn[len(fn) - 1]
    modulename = fn[len(fn) - 2]
    lineno = calframe[1][2]
    code_context = calframe[1][4]
    funcname = code_context[len(code_context) - 1]
    defaultmessage = "[" + modulename + "." + filename + ":" + str(lineno) + "][" + funcname.strip() + "]:"

    def wrapper(*args, **kwargs):
        sw = StopWatch()
        sw.sw_start()
        _logger = getlogger()
        _logger.debug(defaultmessage + "--- start ---")
        kekka = func(*args, **kwargs)
        syorijikan = f"  *** 処理時間：{sw.sw_stop()} ***"
        _logger.debug(defaultmessage + "---- end ----:" + syorijikan)
        return kekka
    wrapper.__name__ = func.__name__
    return wrapper


def edtmessage(message):
    calframe = inspect.getouterframes(inspect.currentframe(), 2)
    fn = calframe[2][1].split("/")
    filename = fn[len(fn) - 1]
    modulename = fn[len(fn) - 2]
    lineno = calframe[1][2]
    return "[" + modulename + "." + filename + ":" + str(lineno) + "][" + calframe[1][3] + "]:" + str(message)


def writedebuglog(message):
    getlogger().debug(edtmessage(message))
    return


def writeinfolog(message):
    getlogger().info(edtmessage(message))
    return


def writeerrorlog(message):
    getlogger().error(edtmessage(message))
    return


class StopWatch:
    def sw_start(self):
        self.__starttime = time.time()
        return

    def sw_stop(self):
        return time.time() - self.__starttime
