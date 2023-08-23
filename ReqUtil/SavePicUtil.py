import re
import threading
from typing import List, Tuple

import requests
from requests import Session

from LogUtil.LogUtil import com_log


class SavePicUtil:
    def __init__(self, session: Session = None, test_times: int = 5):
        if session:
            self.session = session
        else:
            self.session = requests.Session()
            self.session.mount('https://', requests.adapters.HTTPAdapter(pool_connections=15, pool_maxsize=100))
        self.test_times = test_times

    def save_pic(self, url, save_dir, save_name, msg='', is_async=False, log=com_log):
        places: List[Tuple[str, str]] = [(save_dir, save_name)]
        self.save_pic_multi_places(url, places, msg, is_async, log)

    def save_pic_multi_places(self, url, places: List[Tuple[str, str]], msg='', is_async=False, log=com_log):
        if is_async:
            threading.Thread(target=self.__get_then_save_pic, args=(url, places, msg, log)).start()
        else:
            self.__get_then_save_pic(url, places, msg, log)

    def __get_then_save_pic(self, url: str, places, msg, log):

        invalid_url_list = []
        if url in invalid_url_list:
            log.warning(f"图片连接无效: url: {url}, msg: {msg}")
            return
        if url.startswith('https://www.javbus.comhttps://i.imgur.com/'):
            url = url.replace('https://www.javbus.comhttps://i.imgur.com/', 'https://i.imgur.com/')

        res = self.try_get_pic_times(url=url, msg=msg, log=log)

        # 图片获取失败, 尝试别的一些办法
        if not res:

            # 尝试替换https为http
            if url.startswith('https:'):
                test_url = url.replace('https:', 'http:')
                log.error(f"图片请求失败, 尝试https-->http重试 url: {url}"
                          f"\n\ttest_url: {test_url}")
                res = self.try_get_pic_times(url=test_url, msg=msg, log=log)
                if res:
                    log.error(f"图片使用http请求成功: test_url: {test_url}")

        if res:
            try:
                suffix = url.split('.')[-1]
                for place in places:
                    chars_cant_in_filename = r'[\\/:"*?<>|]+'
                    pic_path = f"{place[0]}/{re.sub(chars_cant_in_filename, '-', place[1])}.{suffix}"
                    with open(pic_path, 'wb') as pic:
                        pic.write(res.content)
                    log.info(f"保存图片成功: {pic_path}, msg: {msg}, url:{url}")
            except Exception as e:
                log.error(f"保存图片发生异常: msg: {msg}"
                          f"\n\t异常: {e}"
                          f"\n\turl:{url}")

    def try_get_pic_times(self, url, params=None, msg="", log=com_log):
        for i in range(self.test_times):
            res = None
            try:
                res = self.session.get(url=url, params=params)
                if res.status_code == 200:
                    log.info(f"get图片成功: {msg}, url: {url}, params: {params}")
                    return res
                if i < self.test_times - 1:
                    log.warning(f"get图片响应错误: 第{i + 1}次 msg: {msg} {f'code: {res.status_code}' if res else ''}"
                                f"\n\turl: {url}, params: {params}")
                else:
                    log.error(f"get图片响应错误!!! 第{i + 1}次 msg: {msg} {f'code: {res.status_code}' if res else ''}"
                              f"\n\turl: {url}, params: {params}")
            except Exception as e:
                if i < self.test_times - 1:
                    log.warning(f"get图片出现异常: 第{i + 1}次 msg: {msg} {f'code: {res.status_code}' if res else ''}"
                                f"\n\t异常: {e}"
                                f"\n\turl: {url}, params: {params}")
                else:
                    log.error(f"get图片出现异常!!! 第{i + 1}次 msg: {msg} {f'code: {res.status_code}' if res else ''}"
                              f"\n\t异常: {e}"
                              f"\n\turl: {url}, params: {params}")
