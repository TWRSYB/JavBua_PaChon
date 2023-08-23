from Dao.ComDao import ComVo, ComDao
from LogUtil.LogUtil import ComLog, com_log


class MagnetVo(ComVo):
    def __init__(self, id_fanhao, id_hash_code, nm_resources, lj_magnet, size, update_date):
        self.id_fanhao = id_fanhao
        self.id_hash_code = id_hash_code
        self.nm_resources = nm_resources
        self.lj_magnet = lj_magnet
        self.size = size
        self.update_date = update_date


class MagnetDao(ComDao):

    def __init__(self):
        super().__init__()
        self.table_name = '磁力连接表'

    def insert(self, vo: MagnetVo, log=com_log):
        insert_sql = f"""
                INSERT INTO javbus.magnet
                    (id_fanhao, id_hash_code, nm_resources, lj_magnet, `size`, update_date, 
                    MS_RESUME, MS_DETAIL, RC_RECORD_TIME, RC_RECORDER, RC_LAST_MODIFIED_TIME, RC_LAST_MODIFIER, RC_DATA_STATUS)
                VALUES
                    (%s,  %s,  %s,  %s,  %s,  %s,  
                    ' ', ' ', CURRENT_TIMESTAMP, '未收录', CURRENT_TIMESTAMP, '未收录', '0');
            """
        insert_data = [vo.id_fanhao, vo.id_hash_code, vo.nm_resources, vo.lj_magnet, vo.size, vo.update_date]
        exist_verity_sql = f"""
                SELECT 
                    id_fanhao, id_hash_code, nm_resources, lj_magnet, `size`, update_date, 
                    MS_RESUME, MS_DETAIL, RC_RECORD_TIME, RC_RECORDER, RC_LAST_MODIFIED_TIME, RC_LAST_MODIFIER, RC_DATA_STATUS
                FROM javbus.magnet
                WHERE id_fanhao=%s and id_hash_code=%s;
            """
        exist_verity_data = [vo.id_fanhao, vo.id_hash_code]
        return self.try_insert(insert_sql, insert_data, exist_verity_sql, exist_verity_data, vo, log)
