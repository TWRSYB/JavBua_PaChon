import concurrent.futures
import re
from os import makedirs
from typing import List, Tuple

from lxml import etree

from Config import StartPoint
from Config.Config import URL_HOST, API_PATH_ACTRESS_MOVIE, URL_HOST_CN, URL_HOST_JP, URL_HOST_EN, URL_HOST_KR, \
    JSON_DATA_MAKER, JSON_DATA_LABEL, JSON_DATA_SERIES, JSON_DATA_GENRE, PIC_DIR_MOVIE_COVER_PIC, \
    PIC_DIR_MOVIE_GALLERY_PIC
from Dao.ActressDao import ActressVo
from Dao.GenreDao import GenreVo, GenreDao
from Dao.LabelDao import LabelVo, LabelDao
from Dao.MagnetDao import MagnetVo, MagnetDao
from Dao.MakerDao import MakerVo, MakerDao
from Dao.MovieDao import MovieVo, MovieDao
from Dao.SeriesDao import SeriesVo, SeriesDao
from LogUtil import LogUtil
from LogUtil.LogUtil import com_log, process_log, async_log, save_pic_log
from MyUtil.MyUtil import dict_to_obj2, MyThread, write_data_to_file, json_file_movie, json_file_magnet
from MyUtil.XpathUtil import xpath_util
from ReqUtil.ReqUtil import ReqUtil
from ReqUtil.SavePicUtil import SavePicUtil

req_util = ReqUtil()
save_pic_util = SavePicUtil()


set_maker_id = set()
set_label_id = set()
set_series_id = set()
set_genre_id = set()


def get_movie_info_card_lang(lang_host, id_fanhao, log=com_log, movie_order=0):
    """
    获取影片在不同影片下的页面
    :param movie_order:
    :param log:
    :param lang_host: 语言的基础路径
    :param id_fanhao: 影片番号
    :return:
    """
    res = req_util.try_get_req_times(f"{lang_host}/{id_fanhao}",
                                     msg=f"获取不同语言的影片页面 lang_host: {lang_host}, id_fanhao: {id_fanhao}, movie_order: {movie_order}", log=log)
    return res


# def get_from_multi_lang_page(movie_info_card_list: List, xpath: str):
#     for movie_info_card in movie_info_card_list:
#         result = xpath_util.get_unique(element=movie_info_card, xpath=xpath)
#         if result:
#             return result


def get_movie_detail(id_fanhao, log=com_log, movie_order=0) -> MovieVo:
    # 创建需要的dao, 不使用共享资源, 保证多线程时的线程安全 ↓↓↓
    movie_dao = MovieDao()
    maker_dao = MakerDao()
    label_dao = LabelDao()
    series_dao = SeriesDao()
    genre_dao = GenreDao()
    magnet_dao = MagnetDao()
    # 创建需要的dao, 不使用共享资源, 保证多线程时的线程安全 ↑↑↑

    # 异步获取不同语言的页面 ↓↓↓
    t_cn = MyThread(func=get_movie_info_card_lang, args=(URL_HOST_CN, id_fanhao, log, movie_order))
    t_jp = MyThread(func=get_movie_info_card_lang, args=(URL_HOST_JP, id_fanhao, log, movie_order))
    t_en = MyThread(func=get_movie_info_card_lang, args=(URL_HOST_EN, id_fanhao, log, movie_order))
    t_kr = MyThread(func=get_movie_info_card_lang, args=(URL_HOST_KR, id_fanhao, log, movie_order))
    t_cn.start()
    t_jp.start()
    t_en.start()
    t_kr.start()
    t_cn.join()
    t_jp.join()
    t_en.join()
    t_kr.join()
    res_cn = t_cn.get_result()
    res_jp = t_jp.get_result()
    res_en = t_en.get_result()
    res_kr = t_kr.get_result()
    res_main = res_cn if res_cn else res_jp if res_jp else res_en if res_en else res_kr
    # 异步获取不同语言的页面 ↑↑↑

    if res_main:
        # 解析出不同语言下的影片信息卡片 ↓↓↓
        movie_info_card_cn = etree.HTML(res_cn.text).xpath("//div[@class='container']/div[@class='row movie']")[0] if res_cn else ''
        movie_info_card_jp = etree.HTML(res_jp.text).xpath("//div[@class='container']/div[@class='row movie']")[0] if res_jp else ''
        movie_info_card_en = etree.HTML(res_en.text).xpath("//div[@class='container']/div[@class='row movie']")[0] if res_en else ''
        movie_info_card_kr = etree.HTML(res_kr.text).xpath("//div[@class='container']/div[@class='row movie']")[0] if res_kr else ''
        movie_info_card_main = movie_info_card_cn if movie_info_card_cn else movie_info_card_jp if movie_info_card_jp else movie_info_card_en if movie_info_card_en else movie_info_card_kr
        # 解析出不同语言下的影片信息卡片 ↑↑↑

        # 获取影片信息 ↓↓↓
        # 获取影片封面图 URL 影片名称(多国语言) ↓↓↓
        url_cover_pic = xpath_util.get_unique(movie_info_card_main, xpath=".//a[@class='bigImage']/img/@src")
        nm_cn = xpath_util.get_unique(element=movie_info_card_cn,
                                      xpath=".//a[@class='bigImage']/img/@title") if res_cn else '没有获取到汉语页面'
        nm_jp = xpath_util.get_unique(element=movie_info_card_jp,
                                      xpath=".//a[@class='bigImage']/img/@title") if res_jp else '没有获取到日语页面'
        nm_en = xpath_util.get_unique(element=movie_info_card_en,
                                      xpath=".//a[@class='bigImage']/img/@title") if res_en else '没有获取到英语页面'
        nm_kr = xpath_util.get_unique(element=movie_info_card_kr,
                                      xpath=".//a[@class='bigImage']/img/@title") if res_kr else '没有获取到韩语页面'
        # 获取影片封面图 URL 影片名称(多国语言) ↑↑↑
        # 获取影片时长和发行日期 ↓↓↓
        tags = movie_info_card_main.xpath(".//p/text()")
        duration = ""
        issue_date = ""
        for tag in tags:
            if tag.endswith('分鐘'):
                duration = tag
                break
        for tag in tags:
            match = re.match(r"^.*(\d{4}-\d{2}-\d{2})$", tag)
            if match:
                issue_date = tag
                break
        # 获取影片时长和发行日期 ↑↑↑

        # 获取制片商信息并保存 ↓↓↓
        url_maker = xpath_util.get_unique(movie_info_card_main, xpath=".//p/a[contains(@href,'studio')]/@href")
        maker_nm_cn = ""
        if url_maker:
            maker_id_in_javbus = url_maker.split('/')[-1]
            maker_nm_cn = xpath_util.get_unique(element=movie_info_card_cn,
                                                xpath=".//p/a[contains(@href,'studio')]/text()") if res_cn else '没有获取到汉语页面'
            if maker_id_in_javbus not in set_maker_id:

                maker_nm_jp = xpath_util.get_unique(element=movie_info_card_jp,
                                                    xpath=".//p/a[contains(@href,'studio')]/text()") if res_jp else '没有获取到日语页面'
                maker_nm_en = xpath_util.get_unique(element=movie_info_card_en,
                                                    xpath=".//p/a[contains(@href,'studio')]/text()") if res_en else '没有获取到英语页面'
                maker_nm_kr = xpath_util.get_unique(element=movie_info_card_kr,
                                                    xpath=".//p/a[contains(@href,'studio')]/text()") if res_kr else '没有获取到韩语页面'

                maker_vo = MakerVo(id_in_javbus=maker_id_in_javbus,
                                   nm_cn=maker_nm_cn, nm_jp=maker_nm_jp, nm_en=maker_nm_en, nm_kr=maker_nm_kr)
                log.info(f"获取到制片商信息: {maker_vo}, 影片番号: {id_fanhao}")
                insert_result = maker_dao.insert(maker_vo, log)
                if insert_result:
                    write_data_to_file(test_file=JSON_DATA_MAKER, data=maker_vo)
                    set_maker_id.add(maker_id_in_javbus)

        # 获取制片商信息并保存 ↑↑↑

        # 获取发行商信息并保存 ↓↓↓
        url_label = xpath_util.get_unique(movie_info_card_main, xpath=".//p/a[contains(@href,'label')]/@href")
        label_nm_cn = ""
        if url_label:
            label_id_in_javbus = url_label.split('/')[-1]
            label_nm_cn = xpath_util.get_unique(element=movie_info_card_cn,
                                                xpath=".//p/a[contains(@href,'label')]/text()") if res_cn else '没有获取到汉语页面'
            if label_id_in_javbus not in set_label_id:
                label_nm_jp = xpath_util.get_unique(element=movie_info_card_jp,
                                                    xpath=".//p/a[contains(@href,'label')]/text()") if res_jp else '没有获取到日语页面'
                label_nm_en = xpath_util.get_unique(element=movie_info_card_en,
                                                    xpath=".//p/a[contains(@href,'label')]/text()") if res_en else '没有获取到英语页面'
                label_nm_kr = xpath_util.get_unique(element=movie_info_card_kr,
                                                    xpath=".//p/a[contains(@href,'label')]/text()") if res_kr else '没有获取到韩语页面'

                label_vo = LabelVo(id_maker=maker_nm_cn, id_in_javbus=label_id_in_javbus,
                                   nm_cn=label_nm_cn, nm_jp=label_nm_jp, nm_en=label_nm_en, nm_kr=label_nm_kr)
                log.info(f"获取到发行商信息: {label_vo}, 影片番号: {id_fanhao}")
                insert_result = label_dao.insert(label_vo)
                if insert_result:
                    write_data_to_file(test_file=JSON_DATA_LABEL, data=label_vo)
                    set_label_id.add(label_id_in_javbus)

        # 获取发行商信息并保存 ↑↑↑

        # 获取系列信息并保存 ↓↓↓
        url_series = xpath_util.get_unique(movie_info_card_main, xpath=".//p/a[contains(@href,'series')]/@href")
        series_nm_cn = ""
        if url_series:
            series_id_in_javbus = url_series.split('/')[-1]
            series_nm_cn = xpath_util.get_unique(element=movie_info_card_cn,
                                                 xpath=".//p/a[contains(@href,'series')]/text()") if res_cn else '没有获取到汉语页面'
            if series_id_in_javbus not in set_series_id:
                series_nm_jp = xpath_util.get_unique(element=movie_info_card_jp,
                                                     xpath=".//p/a[contains(@href,'series')]/text()") if res_jp else '没有获取到日语页面'
                series_nm_en = xpath_util.get_unique(element=movie_info_card_en,
                                                     xpath=".//p/a[contains(@href,'series')]/text()") if res_en else '没有获取到英语页面'
                series_nm_kr = xpath_util.get_unique(element=movie_info_card_kr,
                                                     xpath=".//p/a[contains(@href,'series')]/text()") if res_kr else '没有获取到韩语页面'

                series_vo = SeriesVo(id_maker=maker_nm_cn, id_in_javbus=series_id_in_javbus,
                                     nm_cn=series_nm_cn, nm_jp=series_nm_jp, nm_en=series_nm_en, nm_kr=series_nm_kr)
                log.info(f"获取到系列信息: {series_vo}, 影片番号: {id_fanhao}")
                insert_result = series_dao.insert(series_vo)
                if insert_result:
                    write_data_to_file(test_file=JSON_DATA_SERIES, data=series_vo)
                    set_series_id.add(series_id_in_javbus)
        # 获取系列信息并保存 ↑↑↑

        # 获取影片分类并保存 ↓↓↓
        genre_href_list = movie_info_card_main.xpath(".//span[@class='genre']//a[contains(@href,'genre')]/@href")
        genre_nm_cn_list = movie_info_card_main.xpath(".//span[@class='genre']//a[contains(@href,'genre')]/text()")
        genre_nm_jp_list = movie_info_card_jp.xpath(
            ".//span[@class='genre']//a[contains(@href,'genre')]/text()") if res_jp else '没有获取到日语页面'
        genre_nm_en_list = movie_info_card_en.xpath(
            ".//span[@class='genre']//a[contains(@href,'genre')]/text()") if res_en else '没有获取到英语页面'
        genre_nm_kr_list = movie_info_card_kr.xpath(
            ".//span[@class='genre']//a[contains(@href,'genre')]/text()") if res_kr else '没有获取到韩语页面'
        for i in range(len(genre_href_list)):
            genre_id_in_javbus = genre_href_list[i].split('/')[-1]
            genre_nm_cn = genre_nm_cn_list[i] if res_cn else '没有获取到汉语页面'
            if genre_id_in_javbus not in set_genre_id:
                genre_nm_jp = genre_nm_jp_list[i] if res_jp else '没有获取到日语页面'
                genre_nm_en = genre_nm_en_list[i] if res_en else '没有获取到英语页面'
                genre_nm_kr = genre_nm_kr_list[i] if res_kr else '没有获取到韩语页面'
                genre_vo = GenreVo(id_in_javbus=genre_id_in_javbus, nm_cn=genre_nm_cn, nm_jp=genre_nm_jp, nm_en=genre_nm_en,
                                   nm_kr=genre_nm_kr)
                log.info(f"获取到分类信息: {genre_vo}, 影片番号: {id_fanhao}")
                insert_result = genre_dao.insert(genre_vo)
                if insert_result:
                    write_data_to_file(test_file=JSON_DATA_GENRE, data=genre_vo)
                    set_genre_id.add(genre_id_in_javbus)
        genre_list = ','.join(genre_nm_cn_list)
        genre_id_list = ','.join([href.split('/')[-1] for href in genre_href_list])
        log.info(f"获取到影片分类列表: 中文名: {genre_list}, ID: {genre_id_list}, 影片番号: {id_fanhao}")

        # 获取影片分类并保存 ↑↑↑

        # 获取女优列表 ↓↓↓
        actress_href_list = movie_info_card_main.xpath(".//span[@class='genre']//a[contains(@href,'star')]/@href")
        actress_nm_cn_list = movie_info_card_main.xpath(".//span[@class='genre']//a[contains(@href,'star')]/text()")
        actress_list = ','.join(actress_nm_cn_list)
        actress_id_list = ','.join([href.split('/')[-1] for href in actress_href_list])
        log.info(f"获取到影片出演女优列表: {actress_list}, ID: {actress_id_list}, 影片番号: {id_fanhao}")
        # 获取女优列表 ↑↑↑

        # 创建影片对象并保存 ↓↓↓
        movie_vo = MovieVo(id_fanhao=id_fanhao, url_cover_pic=url_cover_pic, nm_cn=nm_cn,
                           nm_jp=nm_jp, nm_en=nm_en, nm_kr=nm_kr,
                           duration=duration, issue_date=issue_date,
                           maker_nm_cn=maker_nm_cn, label_nm_cn=label_nm_cn, series_nm_cn=series_nm_cn,
                           genre_list=genre_list, genre_id_list=genre_id_list,
                           actress_list=actress_list, actress_id_list=actress_id_list)
        insert_result = movie_dao.insert(movie_vo)
        if insert_result:
            try:
                json_file_movie.write(f"{movie_vo}\n")
                log.info(f"json写入文件成功 movie JSON: {movie_vo}")
            except Exception as e:
                log.error(f"json写入文件出现异常 movie JSON: {movie_vo}"
                          f"\n\t异常: {e}")

        # 创建影片对象并保存 ↑↑↑

        # 保存影片封面图 ↓↓↓
        places: List[Tuple[str, str]] = [(PIC_DIR_MOVIE_COVER_PIC, f"{movie_vo.maker_nm_cn}_{movie_vo.id_fanhao}")]
        save_pic_util.save_pic_multi_places(url=f"{URL_HOST}{url_cover_pic}", places=places,
                                            msg=f"影片封面图, 番号: {id_fanhao}, movie_order: {movie_order}", is_async=False,
                                            log=save_pic_log)
        # 保存影片封面图 ↑↑↑

        # 保存影片预览图 ↓↓↓
        sample_waterfall = etree.HTML(res_main.text).xpath("//div[@id='sample-waterfall']")
        if sample_waterfall:
            gallery_href_list = sample_waterfall[0].xpath("./a/@href")
            gallery_href_wrong_then_src_list = sample_waterfall[0].xpath("./a/div/img/@src")
            gallery_small_list = sample_waterfall[0].xpath("./span/div/img/@src")
            gallery_dir = f"{PIC_DIR_MOVIE_GALLERY_PIC}/{movie_vo.maker_nm_cn}_{movie_vo.id_fanhao}"
            if gallery_href_list or gallery_small_list:
                makedirs(gallery_dir, exist_ok=True)

            for i, gallery_href in enumerate(gallery_href_list):

                if gallery_href.startswith('http://www.prestige-av.com'):
                    places3: List[Tuple[str, str]] = [(gallery_dir,
                                                       f"{movie_vo.maker_nm_cn}_{movie_vo.id_fanhao}_{str(i + 1).zfill(3)}_small")]
                    save_pic_util.save_pic_multi_places(url=f"{URL_HOST}{gallery_href_wrong_then_src_list[i]}", places=places3,
                                                        msg=f"影片预览图, 番号: {id_fanhao}, movie_order: {movie_order}",
                                                        is_async=True,
                                                        log=save_pic_log)
                else:
                    places2: List[Tuple[str, str]] = [(gallery_dir,
                                                       f"{movie_vo.maker_nm_cn}_{movie_vo.id_fanhao}_{str(i + 1).zfill(3)}")]
                    save_pic_util.save_pic_multi_places(url=f"{URL_HOST}{gallery_href}", places=places2,
                                                        msg=f"影片预览图, 番号: {id_fanhao}, movie_order: {movie_order}", is_async=True,
                                                        log=save_pic_log)

            for i, gallery_small in enumerate(gallery_small_list):
                places3: List[Tuple[str, str]] = [(gallery_dir,
                                                   f"{movie_vo.maker_nm_cn}_{movie_vo.id_fanhao}_{str(i + 1 + len(gallery_href_list)).zfill(3)}_small")]
                save_pic_util.save_pic_multi_places(url=f"{URL_HOST}{gallery_small}", places=places3,
                                                    msg=f"影片预览图, 番号: {id_fanhao}, movie_order: {movie_order}",
                                                    is_async=True,
                                                    log=save_pic_log)

        # 保存影片预览图 ↑↑↑

        # 保存磁力连接 ↓↓↓
        script_list = etree.HTML(res_main.text).xpath('//script/text()')
        gid = ''
        uc = ''
        img = ''

        search_gid = re.search(r'var gid = (\d+);', script_list[1])
        if search_gid:
            gid = search_gid.group(1)

        search_uc = re.search(r'var uc = (.+);', script_list[1])
        if search_uc:
            uc = search_uc.group(1)

        search_img = re.search(r'var img = (.+);', script_list[1])
        if search_img:
            img = search_img.group(1)

        params = {
            'gid': gid,
            'lang': 'zh',
            'img': img,
            'uc': uc,
            'floor': 178
        }

        res_magnet = req_util.get(url=f'{URL_HOST}/ajax/uncledatoolsbyajax.php', params=params,
                                  msg=f"获取磁力连接, 番号: {id_fanhao}, movie_order: {movie_order}", log=log)
        if res_magnet:
            etree_magnet = etree.HTML(res_magnet.text)
            magnet_tr_list = etree_magnet.xpath("//tr")
            if magnet_tr_list:
                for magnet_tr in magnet_tr_list:
                    magnet_tags = magnet_tr.xpath(".//a/text()")
                    if magnet_tags:
                        nm_resources = magnet_tags[0].strip()
                        size = magnet_tags[1].strip()
                        update_date = magnet_tags[2].strip()
                        lj_magnet = magnet_tr.xpath(".//a/@href")[0]
                        id_hash_code = lj_magnet.split('&')[0].split(':')[-1]
                        magnet_vo = MagnetVo(id_fanhao=id_fanhao, id_hash_code=id_hash_code, nm_resources=nm_resources,
                                             lj_magnet=lj_magnet, size=size, update_date=update_date)
                        insert_result = magnet_dao.insert(magnet_vo, log=log)
                        if insert_result:
                            try:
                                json_file_magnet.write(f"{magnet_vo}\n")
                                log.info(f"json写入文件成功 magnet JSON: {magnet_vo}")
                            except Exception as e:
                                log.error(f"json写入文件出现异常 magnet JSON: {magnet_vo}"
                                          f"\n\t异常: {e}")

        # 保存磁力连接 ↑↑↑

        # 获取影片信息 ↑↑↑

        return movie_vo


def get_movie_detail_async(args):
    id_fanhao, id_in_javbus, page_num, i = args
    process_log.process4(f"获取影片信息: 第{i + 1}个 番号: {id_fanhao} 女优: {id_in_javbus} 第{page_num}页 Start")
    movie_vo = get_movie_detail(id_fanhao, async_log, movie_order=i+1)
    process_log.process4(f"获取影片信息: 第{i + 1}个 番号: {id_fanhao} 女优: {id_in_javbus} 第{page_num}页 End")
    return movie_vo


def get_actress_movie_page(id_in_javbus, page_num) -> (List[MovieVo], bool):
    movie_list: List[MovieVo] = []
    res = req_util.try_get_req_times(url=f"{URL_HOST}{API_PATH_ACTRESS_MOVIE}/{id_in_javbus}/{page_num}",
                                     msg=f"获取女优影片列表: 第{page_num}页 女优: {id_in_javbus}")
    have_next_page = False
    if res:
        etree_res = etree.HTML(res.text)
        url_movie_page_list = etree_res.xpath("//a[@class='movie-box']/@href")
        page_list = etree_res.xpath("//ul[@class='pagination pagination-lg']/li/a/text()")
        if page_list:
            if page_list[-1] == '下一頁':
                have_next_page = True
        id_fanhao_list = [url_movie_page.split('/')[-1] for url_movie_page in url_movie_page_list]

        # 同步获取影片信息
        # for i, id_fanhao in enumerate(id_fanhao_list):
        #     LogUtil.LOG_PROCESS_MOVIE_ORDER = i+1
        #     if StartPoint.START_POINT_MOVIE_ORDER > 1:
        #         process_log.process4(f"跳过 获取影片信息: 第{i + 1}个 女优: {id_in_javbus} 第{page_num}页")
        #         StartPoint.START_POINT_MOVIE_ORDER -= 1
        #         continue
        #     process_log.process4(f"获取影片信息: 第{i + 1}个 女优: {id_in_javbus} 第{page_num}页 Start")
        #     movie_vo = get_movie_detail(id_fanhao)
        #     movie_list.append(movie_vo)
        #     process_log.process4(f"获取影片信息: 第{i + 1}个 女优: {id_in_javbus} 第{page_num}页 End")

        # 创建线程池, 异步多线程获取影片信息(整页开始)
        with concurrent.futures.ThreadPoolExecutor() as executor:
            # 开启多个线程获取影片详情
            futures = [executor.submit(get_movie_detail_async, args=(id_fanhao, id_in_javbus, page_num, i))
                       for i, id_fanhao in enumerate(id_fanhao_list)]
        # 等待所有线程完成并获取结果
        for future in concurrent.futures.as_completed(futures):
            if future.result():
                movie_list.append(future.result())
    return movie_list, have_next_page


def get_actress_movie(id_in_javbus):
    for i in range(1, 100):
        LogUtil.LOG_PROCESS_MOVIE_PAGE = i
        LogUtil.LOG_PROCESS_MOVIE_ORDER = 0
        if StartPoint.START_POINT_MOVIE_PAGE > 1:
            process_log.process3(f"跳过 获取女优影片列表: 第{i}页 女优: {id_in_javbus}")
            StartPoint.START_POINT_MOVIE_PAGE -= 1
            continue
        process_log.process3(f"获取女优影片列表: 第{i}页 女优: {id_in_javbus} Start")
        movie_list, have_next_page = get_actress_movie_page(id_in_javbus, i)
        com_log.info(f"获取女优影片列表完成: 第{i}页 女优: {id_in_javbus} 结果: {movie_list}")
        process_log.process3(f"获取女优影片列表: 第{i}页 女优: {id_in_javbus} End")
        if not have_next_page:
            process_log.process3(f"获取女优影片列表第{i}页完成 没有下一页了")
            break


def test_get_actress_movie():
    # actress_dict = {"id_in_javbus": "lf1", "url_avatar": "/imgs/actress/371.jpg", "nm_cn": "朝桐光",
    #                 "nm_jp": "朝桐光", "nm_en": "Akari Asagiri", "nm_kr": "Akari Asagiri"}
    # actress_vo: ActressVo = dict_to_obj2(ActressVo, actress_dict)
    id_in_javbus = 'lf1'
    get_actress_movie(id_in_javbus)


def test_get_movie_detail():
    get_movie_detail('111417-537')


if __name__ == '__main__':
    test_get_actress_movie()
    # test_get_movie_detail()
