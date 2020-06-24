from DBUtils.PooledDB import PooledDB
import pymysql

POOL = PooledDB(
    creator=pymysql,
    maxconnections=6,
    mincached=2,
    maxcached=5,
    blocking=True,
    maxusage=None,
    setsession=[],
    ping=0,
    host='127.0.0.1',
    port=3306,
    user='jacob',
    password='jacob',
    database='flask_sql',
    charset='utf8'
)

class SQLHelper(object):

    @staticmethod
    def fetch_one(sql, args):
        conn = POOL.connection()
        cursor = conn.cursor()
        cursor.execute(sql, args)
        result = cursor.fetchone()
        conn.close()
        return result



# result = SQLHelper.fetch_one('''CREATE TABLE `config_info` (
#   `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT 'id',PRIMARY KEY (`id`))''',())
# print(result)