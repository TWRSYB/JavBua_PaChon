import logging

from Config.Config import OUTPUT_DIR

LOG_PATH_GLOBAL = f'{OUTPUT_DIR}/logs/Global_log.log'

LOG_PATH_PROCESS = f'{OUTPUT_DIR}/logs/Process_log.log'

LOG_PATH_COM_DEBUG = f'{OUTPUT_DIR}/logs/Com_debug.log'
LOG_PATH_COM_INFO = f'{OUTPUT_DIR}/logs/Com_info.log'
LOG_PATH_COM_WARNING = f'{OUTPUT_DIR}/logs/Com_warning.log'
LOG_PATH_COM_ERROR = f'{OUTPUT_DIR}/logs/Com_error.log'

LOG_PATH_PIC_DEBUG = f'{OUTPUT_DIR}/logs/Pic_debug.log'
LOG_PATH_PIC_INFO = f'{OUTPUT_DIR}/logs/Pic_info.log'
LOG_PATH_PIC_WARNING = f'{OUTPUT_DIR}/logs/Pic_warning.log'
LOG_PATH_PIC_ERROR = f'{OUTPUT_DIR}/logs/Pic_error.log'

LOG_PATH_ASYNC_DEBUG = f'{OUTPUT_DIR}/logs/Async_debug.log'
LOG_PATH_ASYNC_INFO = f'{OUTPUT_DIR}/logs/Async_info.log'
LOG_PATH_ASYNC_WARNING = f'{OUTPUT_DIR}/logs/Async_warning.log'
LOG_PATH_ASYNC_ERROR = f'{OUTPUT_DIR}/logs/Async_error.log'

LOG_PROCESS_ACTRESSES_PAGE = 0
LOG_PROCESS_ACTRESS_ORDER = 0
LOG_PROCESS_MOVIE_PAGE = 0
LOG_PROCESS_MOVIE_ORDER = 0


# 自定义日志参数赋值
class _FormatterWithSelfAttr(logging.Formatter):
    def format(self, record):
        record.process = f"{LOG_PROCESS_ACTRESSES_PAGE}-{LOG_PROCESS_ACTRESS_ORDER}-{LOG_PROCESS_MOVIE_PAGE}-{LOG_PROCESS_MOVIE_ORDER}"
        return super(_FormatterWithSelfAttr, self).format(record)


formatter_with_process = _FormatterWithSelfAttr(fmt="%(asctime)s - %(process)s - %(levelname)s - %(message)s")
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")


# 全局日志配置
logging.basicConfig(format="%(asctime)s - %(process)s - %(levelname)s - %(message)s", level=logging.DEBUG)
logging.Formatter = _FormatterWithSelfAttr


# 全局日志对象设置
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename=LOG_PATH_GLOBAL, encoding='utf-8')
handler.setLevel(logging.DEBUG)
handler.setFormatter(formatter_with_process)
logger.addHandler(handler)


# def msg_add_process(msg):
#     return f"{LOG_PROCESS_ACTRESSES_PAGE}-{LOG_PROCESS_ACTRESS_ORDER}-{LOG_PROCESS_MOVIE_PAGE}-{LOG_PROCESS_MOVIE_ORDER} - {msg}"


class ComLog:
    # 获取日志对象
    logger_com = logging.getLogger('logger_com')
    logger_com.setLevel(logging.DEBUG)

    # 创建日志文件处理器
    handler_debug = logging.FileHandler(filename=LOG_PATH_COM_DEBUG, encoding='utf-8')
    handler_info = logging.FileHandler(filename=LOG_PATH_COM_INFO, encoding='utf-8')
    handler_warning = logging.FileHandler(filename=LOG_PATH_COM_WARNING, encoding='utf-8')
    handler_error = logging.FileHandler(filename=LOG_PATH_COM_ERROR, encoding='utf-8')
    # 为处理器设置级别
    handler_debug.setLevel(logging.DEBUG)
    handler_info.setLevel(logging.INFO)
    handler_warning.setLevel(logging.WARNING)
    handler_error.setLevel(logging.ERROR)
    # 为处理器设置格式
    handler_debug.setFormatter(formatter_with_process)
    handler_info.setFormatter(formatter_with_process)
    handler_warning.setFormatter(formatter_with_process)
    handler_error.setFormatter(formatter_with_process)
    # 将处理器添加到日志对象中
    logger_com.addHandler(handler_debug)
    logger_com.addHandler(handler_info)
    logger_com.addHandler(handler_warning)
    logger_com.addHandler(handler_error)

    def debug(self, msg):
        self.logger_com.debug(msg)

    def info(self, msg):
        self.logger_com.info(msg)

    def warning(self, msg):
        self.logger_com.warning(msg)

    def error(self, msg):
        self.logger_com.error(msg)


class SavePicLog:
    # 获取日志对象
    logger_pic = logging.getLogger('logger_pic')
    logger_pic.setLevel(logging.DEBUG)

    # 创建日志文件处理器
    handler_debug = logging.FileHandler(filename=LOG_PATH_PIC_DEBUG, encoding='utf-8')
    handler_info = logging.FileHandler(filename=LOG_PATH_PIC_INFO, encoding='utf-8')
    handler_warning = logging.FileHandler(filename=LOG_PATH_PIC_WARNING, encoding='utf-8')
    handler_error = logging.FileHandler(filename=LOG_PATH_PIC_ERROR, encoding='utf-8')
    # 为处理器设置级别
    handler_debug.setLevel(logging.DEBUG)
    handler_info.setLevel(logging.INFO)
    handler_warning.setLevel(logging.WARNING)
    handler_error.setLevel(logging.ERROR)
    # 为处理器设置格式
    handler_debug.setFormatter(formatter)
    handler_info.setFormatter(formatter)
    handler_warning.setFormatter(formatter)
    handler_error.setFormatter(formatter)
    # 将处理器添加到日志对象中
    logger_pic.addHandler(handler_debug)
    logger_pic.addHandler(handler_info)
    logger_pic.addHandler(handler_warning)
    logger_pic.addHandler(handler_error)

    def debug(self, msg):
        self.logger_pic.debug(msg)

    def info(self, msg):
        self.logger_pic.info(msg)

    def warning(self, msg):
        self.logger_pic.warning(msg)

    def error(self, msg):
        self.logger_pic.error(msg)


class ProcessLog:
    # 获取进度日志对象
    logger_process_1 = logging.getLogger('logger_process_1')
    logger_process_2 = logging.getLogger('logger_process_2')
    logger_process_3 = logging.getLogger('logger_process_3')
    logger_process_4 = logging.getLogger('logger_process_4')
    logger_process_5 = logging.getLogger('logger_process_5')

    logger_process_1.setLevel(logging.DEBUG)
    logger_process_2.setLevel(logging.DEBUG)
    logger_process_3.setLevel(logging.DEBUG)
    logger_process_4.setLevel(logging.DEBUG)
    logger_process_5.setLevel(logging.DEBUG)

    # 创建日志文件处理器
    handler_1 = logging.FileHandler(filename=LOG_PATH_PROCESS, encoding='utf-8')
    handler_2 = logging.FileHandler(filename=LOG_PATH_PROCESS, encoding='utf-8')
    handler_3 = logging.FileHandler(filename=LOG_PATH_PROCESS, encoding='utf-8')
    handler_4 = logging.FileHandler(filename=LOG_PATH_PROCESS, encoding='utf-8')
    handler_5 = logging.FileHandler(filename=LOG_PATH_PROCESS, encoding='utf-8')

    # 为处理器设置级别
    handler_1.setLevel(logging.DEBUG)
    handler_2.setLevel(logging.DEBUG)
    handler_3.setLevel(logging.DEBUG)
    handler_4.setLevel(logging.DEBUG)
    handler_5.setLevel(logging.DEBUG)

    # 为处理器设置格式
    handler_1.setFormatter(
        logging.Formatter('%(asctime)s - %(process)s - %(levelname)s - %(message)s'))
    handler_2.setFormatter(
        logging.Formatter('\t%(asctime)s - %(process)s - %(levelname)s - %(message)s'))
    handler_3.setFormatter(
        logging.Formatter('\t\t%(asctime)s - %(process)s - %(levelname)s - %(message)s'))
    handler_4.setFormatter(
        logging.Formatter('\t\t\t%(asctime)s - %(process)s - %(levelname)s - %(message)s'))
    handler_5.setFormatter(
        logging.Formatter('\t\t\t\t%(asctime)s - %(process)s - %(levelname)s - %(message)s'))

    # 将处理器添加到日志对象中
    logger_process_1.addHandler(handler_1)
    logger_process_2.addHandler(handler_2)
    logger_process_3.addHandler(handler_3)
    logger_process_4.addHandler(handler_4)
    logger_process_5.addHandler(handler_5)

    def process1(self, msg):
        self.logger_process_1.info(msg)

    def process2(self, msg):
        self.logger_process_2.info(msg)

    def process3(self, msg):
        self.logger_process_3.info(msg)

    def process4(self, msg):
        self.logger_process_4.info(msg)

    def process5(self, msg):
        self.logger_process_5.info(msg)


class AsyncLog:
    # 获取日志对象
    logger = logging.getLogger('logger_async')
    logger.setLevel(logging.DEBUG)

    # 创建不同级别日志文件对象处理器
    handler_debug = logging.FileHandler(filename=LOG_PATH_ASYNC_DEBUG, encoding='utf-8')
    handler_info = logging.FileHandler(filename=LOG_PATH_ASYNC_INFO, encoding='utf-8')
    handler_warning = logging.FileHandler(filename=LOG_PATH_ASYNC_WARNING, encoding='utf-8')
    handler_error = logging.FileHandler(filename=LOG_PATH_ASYNC_ERROR, encoding='utf-8')
    # 为处理器设置级别
    handler_debug.setLevel(logging.DEBUG)
    handler_info.setLevel(logging.INFO)
    handler_warning.setLevel(logging.WARNING)
    handler_error.setLevel(logging.ERROR)
    # 为处理器设置格式
    handler_debug.setFormatter(formatter_with_process)
    handler_info.setFormatter(formatter_with_process)
    handler_warning.setFormatter(formatter_with_process)
    handler_error.setFormatter(formatter_with_process)
    # 将处理器添加到日志对象中
    logger.addHandler(handler_debug)
    logger.addHandler(handler_info)
    logger.addHandler(handler_warning)
    logger.addHandler(handler_error)

    def debug(self, msg):
        self.logger.debug(msg)

    def info(self, msg):
        self.logger.info(msg)

    def warning(self, msg):
        self.logger.warning(msg)

    def error(self, msg):
        self.logger.error(msg)


com_log = ComLog()
process_log = ProcessLog()
async_log = AsyncLog()
save_pic_log = SavePicLog()
