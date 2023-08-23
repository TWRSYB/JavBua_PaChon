from Dao.ComDao import ComVo, ComDao
from LogUtil.LogUtil import ComLog, com_log


class SeriesVo(ComVo):
    def __init__(self, id_maker, id_in_javbus, nm_cn, nm_jp, nm_en, nm_kr):
        self.id_maker = id_maker
        self.id_in_javbus = id_in_javbus
        self.nm_cn = nm_cn
        self.nm_jp = nm_jp
        self.nm_en = nm_en
        self.nm_kr = nm_kr


class SeriesDao(ComDao):

    def __init__(self):
        super().__init__()
        self.table_name = '系列表'

    def insert(self, vo: SeriesVo, log=com_log):
        insert_sql = f"""
                INSERT INTO javbus.series
                    (id_maker, id_in_javbus, nm_cn, nm_jp, nm_en, nm_kr, MS_RESUME, MS_DETAIL, RC_RECORD_TIME, RC_RECORDER, RC_LAST_MODIFIED_TIME, RC_LAST_MODIFIER, RC_DATA_STATUS)
                VALUES
                    (%s, %s, %s, %s, %s, %s, 
                    ' ', ' ', CURRENT_TIMESTAMP, '未收录', '0000-00-00 00:00:00', '未收录', '0');
            """
        insert_data = [vo.id_maker, vo.id_in_javbus, vo.nm_cn, vo.nm_jp, vo.nm_en, vo.nm_kr]
        exist_verity_sql = f"""
                SELECT 
                    id_maker, id_in_javbus, nm_cn, nm_jp, nm_en, nm_kr, 
                    MS_RESUME, MS_DETAIL, RC_RECORD_TIME, RC_RECORDER, RC_LAST_MODIFIED_TIME, RC_LAST_MODIFIER, RC_DATA_STATUS
                FROM javbus.series
                WHERE id_maker=%s and id_in_javbus=%s
            """
        exist_verity_data = [vo.id_maker, vo.id_in_javbus]
        return self.try_insert(insert_sql, insert_data, exist_verity_sql, exist_verity_data, vo, log)
