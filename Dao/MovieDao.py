from Dao.ComDao import ComVo, ComDao
from LogUtil.LogUtil import ComLog, com_log


class MovieVo(ComVo):
    def __init__(self, id_fanhao, url_cover_pic, nm_cn, nm_jp, nm_en, nm_kr,
                 duration, issue_date, maker_nm_cn, label_nm_cn, series_nm_cn,
                 genre_list, genre_id_list, actress_list, actress_id_list):
        self.id_fanhao = id_fanhao
        self.url_cover_pic = url_cover_pic
        self.nm_cn = nm_cn
        self.nm_jp = nm_jp
        self.nm_en = nm_en
        self.nm_kr = nm_kr
        self.duration = duration
        self.issue_date = issue_date
        self.maker_nm_cn = maker_nm_cn
        self.label_nm_cn = label_nm_cn
        self.series_nm_cn = series_nm_cn
        self.genre_list = genre_list
        self.genre_id_list = genre_id_list
        self.actress_list = actress_list
        self.actress_id_list = actress_id_list


class MovieDao(ComDao):

    def __init__(self):
        super().__init__()
        self.table_name = '影片表'

    def insert(self, vo: MovieVo, log=com_log):
        insert_sql = f"""
                INSERT INTO javbus.movie
                    (id_fanhao, url_cover_pic, 
                    nm_cn, nm_jp, nm_en, nm_kr, 
                    duration, issue_date, 
                    maker_nm_cn, label_nm_cn, series_nm_cn, 
                    genre_list, genre_id_list, actress_list, actress_id_list, 
                    MS_RESUME, MS_DETAIL, RC_RECORD_TIME, RC_RECORDER, RC_LAST_MODIFIED_TIME, RC_LAST_MODIFIER, RC_DATA_STATUS)
                VALUES
                    (%s, %s,
                     %s, %s, %s, %s, 
                     %s, %s, 
                     %s, %s, %s, 
                     %s, %s, %s, %s, 
                    ' ', ' ', CURRENT_TIMESTAMP, '未收录', '0000-00-00 00:00:00', '未收录', '0');
            """
        insert_data = [vo.id_fanhao, vo.url_cover_pic,
                       vo.nm_cn, vo.nm_jp, vo.nm_en, vo.nm_kr,
                       vo.duration, vo.issue_date,
                       vo.maker_nm_cn, vo.label_nm_cn, vo.series_nm_cn,
                       vo.genre_list, vo.genre_id_list, vo.actress_list, vo.actress_id_list]
        exist_verity_sql = f"""
                SELECT 
                    id_fanhao, url_cover_pic, 
                    nm_cn, nm_jp, nm_en, nm_kr, 
                    duration, issue_date, 
                    maker_nm_cn, label_nm_cn, series_nm_cn, 
                    genre_list, genre_id_list, actress_list, actress_id_list, 
                    MS_RESUME, MS_DETAIL, RC_RECORD_TIME, RC_RECORDER, RC_LAST_MODIFIED_TIME, RC_LAST_MODIFIER, RC_DATA_STATUS
                FROM javbus.movie
                WHERE id_fanhao=%s;
            """
        exist_verity_data = [vo.id_fanhao]
        return self.try_insert(insert_sql, insert_data, exist_verity_sql, exist_verity_data, vo, log)
