import inspect
import threading

from Config.Config import JSON_DATA_MOVIE, JSON_DATA_GENRE, JSON_DATA_MAKER, JSON_DATA_LABEL, JSON_DATA_SERIES, \
    JSON_DATA_MAGNET
from LogUtil.LogUtil import ComLog, com_log


class MyThread(threading.Thread):
    def __init__(self, func, args=()):
        super(MyThread, self).__init__()
        self.func = func
        self.args = args

    def run(self):
        self.result = self.func(*self.args)  # 在执行函数的同时，把结果赋值给result,
        # 然后通过get_result函数获取返回的结果

    def get_result(self):
        try:
            return self.result
        except Exception as e:
            return None


def write_data_to_file(test_file, data, msg="", log=com_log):
    try:
        with open(file=test_file, mode='a', encoding="utf-8") as jf:
            jf.write(f"{data}\n")
            log.info(f"json写入文件成功 路径: {test_file} JSON: {data} msg: {msg}")
    except Exception as e:
        log.error(f"json写入文件出现异常 路径: {test_file} JSON: {data} msg: {msg}")


def dict_to_obj(cls, the_dict):
    init_attributes = [key for key, value in inspect.signature(cls).parameters.items() if key != 'self']
    args = [the_dict.get(key) for key in init_attributes]
    entity = cls(*args)
    out_attributes = [attr for attr in dir(cls) if not callable(getattr(cls, attr)) and not attr.startswith('__')] + [
        key for key, value in vars(cls)['__annotations__'].items()]
    for key in out_attributes:
        setattr(entity, key, the_dict.get(key))
    return entity


def dict_to_obj2(cls, the_dict):
    entity = create_empty_obj(cls)
    for key, value in the_dict.items():
        setattr(entity, key, value)
    return entity


def create_empty_obj(cls):
    sig = inspect.signature(cls)
    args = [None] * (len(sig.parameters))
    entity = cls(*args)
    return entity


def create_create_table_sql(cls: type):
    sql = 'CREATE TABLE xxx ('

    init_attribute_list = [key for key, value in inspect.signature(cls).parameters.items() if key != 'self']
    out_attribute_list = [attr for attr in dir(cls) if
                          not callable(getattr(cls, attr)) and not attr.startswith('__')] + [
                             key for key, value in vars(cls)['__annotations__'].items()]


json_file_movie = open(JSON_DATA_MOVIE, 'a', encoding='utf-8')
json_file_genre = open(JSON_DATA_GENRE, 'a', encoding='utf-8')
json_file_maker = open(JSON_DATA_MAKER, 'a', encoding='utf-8')
json_file_label = open(JSON_DATA_LABEL, 'a', encoding='utf-8')
json_file_series = open(JSON_DATA_SERIES, 'a', encoding='utf-8')
json_file_magnet = open(JSON_DATA_MAGNET, 'a', encoding='utf-8')