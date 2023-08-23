# import logging
#
# # 创建一个记录器
# logger = logging.getLogger()
#
# # 创建一个格式化字符串，包含要添加的变量
# formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - '
#                               'LOG_PROCESS_ACTRESSES_PAGE=%(process_actresses_page)d '
#                               'LOG_PROCESS_ACTRESS_ORDER=%(process_actress_order)d '
#                               'LOG_PROCESS_MOVIE_PAGE=%(process_movie_page)d '
#                               'LOG_PROCESS_MOVIE_ORDER=%(process_movie_order)d '
#                               '- %(message)s')
#
# # 创建一个处理程序，并将格式化程序添加到它
# handler = logging.StreamHandler()
# handler.setFormatter(formatter)
#
# # 将处理程序添加到记录器
# logger.addHandler(handler)
#
# # 定义要添加到日志记录中的全局数据
# global_data = {
#     'process_actresses_page': 0,
#     'process_actress_order': 0,
#     'process_movie_page': 0,
#     'process_movie_order': 0
# }
#
# # 创建一个LoggerAdapter对象，将全局数据作为参数传递
# logger = logging.LoggerAdapter(logger, extra=global_data)
#
# # 记录一条消息，不需要显式传递全局数据
# logger.info('Some message')
# A custom formatter to add the timestamp from the simulated clock.
import logging
from turtledemo import clock


LOG_PROCESS_ACTRESSES_PAGE = 0
LOG_PROCESS_ACTRESS_ORDER = 0
LOG_PROCESS_MOVIE_PAGE = 0
LOG_PROCESS_MOVIE_ORDER = 0

class _Formatter(logging.Formatter):
    def format(self, record):
        record.simulated_clock = LOG_PROCESS_ACTRESSES_PAGE
        return super(_Formatter, self).format(record)


# Creates a logger object.
def _create_logger():
    logger = logging.getLogger("simulation")
    logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    formatter = _Formatter("%(simulated_clock)s - %(levelname)s - %(message)s")
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    return logger


logger1 = _create_logger()

logger1.info(444)
LOG_PROCESS_ACTRESSES_PAGE = 100

logger1.info(444)
