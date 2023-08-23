import time
from typing import List, Tuple

from lxml import etree

from Config import StartPoint
from Config.Config import URL_HOST, API_PATH_UNCENSORED_ACTRESSES, PIC_DIR_ACTRESS_AVATAR, URL_HOST_JP, \
    API_PATH_ACTRESS_MOVIE, URL_HOST_EN, URL_HOST_KR, URL_HOST_CN, JSON_DATA_ACTRESS
from Dao.ActressDao import ActressVo, ActressDao
from GetMovie import get_actress_movie
from LogUtil import LogUtil
from LogUtil.LogUtil import process_log, com_log
from MyUtil.MyUtil import MyThread, write_data_to_file
from MyUtil.XpathUtil import xpath_util
from ReqUtil.ReqUtil import ReqUtil
from ReqUtil.SavePicUtil import SavePicUtil

req_util = ReqUtil()
save_pic_util = SavePicUtil()

actress_dao = ActressDao()


def get_actresses_page(page_num) -> List[ActressVo]:
    actress_list: List[ActressVo] = []
    res = req_util.try_get_req_times(url=f"{URL_HOST}/{API_PATH_UNCENSORED_ACTRESSES}/{page_num}",
                                     msg=f"获取女优列表: 第{page_num}页")
    if res:
        etree_res = etree.HTML(res.text)
        a_actress_list = etree_res.xpath("//a[@class='avatar-box text-center']")
        for i, a_actress in enumerate(a_actress_list):
            LogUtil.LOG_PROCESS_ACTRESS_ORDER = i+1
            LogUtil.LOG_PROCESS_MOVIE_PAGE = 0
            LogUtil.LOG_PROCESS_MOVIE_ORDER = 0
            if StartPoint.START_POINT_ACTRESS_ORDER > 1:
                process_log.process2(f"跳过 获取女优信息: 第{i + 1}个 第{page_num}页")
                StartPoint.START_POINT_ACTRESS_ORDER -= 1
                continue
            process_log.process2(f"获取女优信息: 第{i + 1}个 第{page_num}页 Start")
            id_in_javbus = xpath_util.get_unique(a_actress, './@href').split('/')[-1]

            actress_vo = save_actress(id_in_javbus)
            com_log.info(f"获取到女优: {actress_vo} 第{page_num}页 第{i + 1}个")
            actress_list.append(actress_vo)

            process_log.process2(f"获取女优信息: 第{i + 1}个 第{page_num}页 End")

    return actress_list


def get_actress_nm_lang(url_host_lang, id_in_javbus):

    res = req_util.try_get_req_times(url=f"{url_host_lang}{API_PATH_ACTRESS_MOVIE}/{id_in_javbus}",
                                     msg=f"获取女优多国语言名: url_host_lang: {url_host_lang} 女优ID: {id_in_javbus}")
    if res:
        return etree.HTML(res.text)
        # etree_res = etree.HTML(res.text)
        # xpath_list = etree_res.xpath("//div[@class='avatar-box aave']//span/text()")
        # if xpath_list:
        #     return xpath_list[0]
        # else:
        #     com_log.error(f"获取女优多国语名失败 url_host_lang: {url_host_lang}, id: {id_in_javbus}")


def save_actress(id_in_javbus) -> ActressVo:
    """
    进一步获取并保存女优的信息
    :param actress_vo:
    :return:
    """

    # 获取女优多国语名 ↓↓↓
    t_cn = MyThread(func=get_actress_nm_lang, args=(URL_HOST_CN, id_in_javbus))
    t_jp = MyThread(func=get_actress_nm_lang, args=(URL_HOST_JP, id_in_javbus))
    t_en = MyThread(func=get_actress_nm_lang, args=(URL_HOST_EN, id_in_javbus))
    t_kr = MyThread(func=get_actress_nm_lang, args=(URL_HOST_KR, id_in_javbus))

    t_cn.start()
    t_jp.start()
    t_en.start()
    t_kr.start()

    t_cn.join()
    t_jp.join()
    t_en.join()
    t_kr.join()

    res_cn = t_jp.get_result() if t_jp.get_result() else '女友没有多国语影片页面'
    res_jp = t_jp.get_result() if t_jp.get_result() else '女友没有多国语影片页面'
    res_en = t_en.get_result() if t_en.get_result() else '女友没有多国语影片页面'
    res_kr = t_kr.get_result() if t_kr.get_result() else '女友没有多国语影片页面'

    res_main = res_cn if res_cn else res_jp if res_jp else res_en if res_en else res_kr
    if res_main:
        url_avatar = xpath_util.get_unique(res_main, "//div[@class='avatar-box aave']//img/@src")
        nm_cn = xpath_util.get_unique(res_cn, "//div[@class='avatar-box aave']//span/text()")
        nm_jp = xpath_util.get_unique(res_jp, "//div[@class='avatar-box aave']//span/text()")
        nm_en = xpath_util.get_unique(res_en, "//div[@class='avatar-box aave']//span/text()")
        nm_kr = xpath_util.get_unique(res_kr, "//div[@class='avatar-box aave']//span/text()")

        actress_vo = ActressVo(id_in_javbus=id_in_javbus, url_avatar=url_avatar, nm_cn=nm_cn,
                               nm_jp=nm_jp, nm_en=nm_en, nm_kr=nm_kr)

        actress_vo.nm_jp = nm_jp
        actress_vo.nm_en = nm_en
        actress_vo.nm_kr = nm_kr

        # 获取女优多国语名 ↑↑↑

        # 女优入库并保存JSON ↓↓↓
        insert_result = actress_dao.insert(actress_vo)
        if insert_result:
            write_data_to_file(test_file=JSON_DATA_ACTRESS, data=actress_vo)
        # 女优入库并保存JSON ↑↑↑

        # 保存女优头像 ↓↓↓
        places: List[Tuple[str, str]] = []
        places.append((f"{PIC_DIR_ACTRESS_AVATAR}", f"{actress_vo.id_in_javbus}_{actress_vo.nm_cn}"))
        save_pic_util.save_pic_multi_places(url=f"{URL_HOST}/{actress_vo.url_avatar}", places=places,
                                            msg=f"获取女优头像: 女优{actress_vo}")
        # 保存女优头像 ↑↑↑

        # 获取女优影片信息 ↓↓↓
        get_actress_movie(actress_vo)
        # 获取女优影片信息 ↑↑↑


def start():
    for i in range(1, 500):
        LogUtil.LOG_PROCESS_ACTRESSES_PAGE = i
        LogUtil.LOG_PROCESS_ACTRESS_ORDER = 0
        LogUtil.LOG_PROCESS_MOVIE_PAGE = 0
        LogUtil.LOG_PROCESS_MOVIE_ORDER = 0
        if StartPoint.START_POINT_ACTRESSES_PAGE > 1:
            process_log.process1(f"跳过 获取女优列表: 第{i}页")
            StartPoint.START_POINT_ACTRESSES_PAGE -= 1
            continue
        process_log.process1(f"获取女优列表: 第{i}页 Start")
        actress_list = get_actresses_page(i)
        process_log.process1(f"获取女优列表成功: 第{i}页 结果: {actress_list}")
        process_log.process1(f"获取女优列表: 第{i}页 End")
        if not actress_list:
            process_log.process1(f"获取女优列表第{i}页 结果为空, 不再获取下一页")
            break


# 按间距中的绿色按钮以运行脚本。
def test_save_actress():
    pass


if __name__ == '__main__':
    start_time = time.time()
    # start()
    test_save_actress()
    end_time = time.time()
    duration = end_time - start_time
    duration_minutes = duration / 60
    print("程序持续时间：", duration_minutes, "分钟")
