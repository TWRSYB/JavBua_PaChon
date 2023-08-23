
from Dao.ComDao import ComVo, ComDao
from LogUtil.LogUtil import com_log


class ActressVo(ComVo):

    def __init__(self, id_in_javbus, url_avatar, nm_cn, nm_jp='', nm_en="", nm_kr=''):
        self.id_in_javbus = id_in_javbus
        self.url_avatar = url_avatar
        self.nm_cn = nm_cn
        self.nm_jp: str = nm_jp
        self.nm_en: str = nm_en
        self.nm_kr: str = nm_kr


class ActressDao(ComDao):
    def __init__(self):
        super().__init__()
        self.table_name = '女优表'

    def insert(self, vo: ActressVo, log=com_log):
        insert_sql = f"""
                INSERT INTO javbus.actress
                    (id_in_javbus, url_avatar, nm_cn, nm_jp, nm_en, nm_kr, 
                    MS_RESUME, MS_DETAIL, RC_RECORD_TIME, RC_RECORDER, RC_LAST_MODIFIED_TIME, RC_LAST_MODIFIER, RC_DATA_STATUS)
                VALUES(%s, %s, %s, %s, %s, %s, 
                    ' ', ' ', CURRENT_TIMESTAMP, '未收录', CURRENT_TIMESTAMP, '未收录', '0');
            """
        insert_data = [vo.id_in_javbus, vo.url_avatar, vo.nm_cn, vo.nm_jp, vo.nm_en, vo.nm_kr]
        exist_verity_sql = f"""
                SELECT 
                    id_in_javbus, url_avatar, nm_cn, nm_jp, nm_en, nm_kr, 
                    MS_RESUME, MS_DETAIL, RC_RECORD_TIME, RC_RECORDER, RC_LAST_MODIFIED_TIME, RC_LAST_MODIFIER, RC_DATA_STATUS
                FROM javbus.actress
                WHERE id_in_javbus = %s
            """
        exist_verity_data = [vo.id_in_javbus]
        return self.try_insert(insert_sql, insert_data, exist_verity_sql, exist_verity_data, vo, log)
