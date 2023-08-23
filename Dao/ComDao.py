import json

import pymysql
from pymysql import Connection

from LogUtil.LogUtil import com_log


class ComVo:
    def __str__(self):
        return json.dumps(self.__dict__, ensure_ascii=False)


class ComDao:
    def __init__(self):
        self.conn = Connection(
            host='localhost',
            port=3306,
            user='root',
            password='123456',
            db='JavBus',
            autocommit=True
        )
        self.table_name = ""

    def try_insert(self, insert_sql, insert_data=None, exist_verity_sql='', exist_verity_data=None,
                   vo=None, log=com_log):
        cursor = self.conn.cursor()
        try:
            cursor.execute(insert_sql, insert_data)
            log.info(f"插入数据库成功: {self.table_name} vo:{vo}")
            return True
        except pymysql.err.IntegrityError as e:
            try:
                cursor.execute(exist_verity_sql, exist_verity_data)
                exist_verity_result = cursor.fetchall()
                if len(exist_verity_result) > 0:
                    log.warning(f"插入数据库失败, 数据已存在: {self.table_name} vo:{vo}")
                else:
                    log.error(f"插入数据库失败, 且数据不存在: {self.table_name} vo:{vo}"
                              f"\n\t异常: {e}"
                              f"\n\tInsert: {insert_sql} Data: {insert_data}"
                              f"\n\tExistVerity: {exist_verity_sql} Data: {exist_verity_data}")
            except Exception as e:
                log.error(f"插入数据库失败, 验证存在出现异常: {self.table_name} vo:{vo}"
                          f"\n\t异常: {e}"
                          f"\n\tInsert: {insert_sql} Data: {insert_data}"
                          f"\n\tExistVerity: {exist_verity_sql} Data: {exist_verity_data}")
        except Exception as e:
            log.error(f"插入数据库失败, 插入出现异常: {self.table_name} vo:{vo}"
                      f"\n\t异常: {e}"
                      f"\n\tInsert: {insert_sql} Data: {insert_data}")
        finally:
            cursor.close()

    def select_by_id(self, select_sql, select_data, vo):
        cursor = self.conn.cursor()
        select_result = ()
        try:
            cursor.execute(select_sql, select_data)
            select_result = cursor.fetchall()
            if len(select_result) > 0:
                com_log.info(f"通过ID查找, 得到数据: {self.table_name} 结果: {select_result}")
                return select_result
            else:
                com_log.info(f"通过ID查找, 得到数据: {self.table_name} 结果: {select_result}"
                             f"\n\tselect_sql: {select_sql} select_data: {select_data}")
        except Exception as e:
            com_log.error(f"通过ID查找发生异常: {self.table_name}"
                          f"\n\t异常: {e}"
                          f"\n\tselect_sql: {select_sql} select_data: {select_data}")
        finally:
            cursor.close()
        return select_result
