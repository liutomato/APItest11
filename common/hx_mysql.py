import pymysql
import redis
import common
from collections.abc import Iterable


class RedisUtils:
    def connect_redis(self):
        self.conn = redis.StrictRedis(host='9999.249', port=6379, db=0, decode_responses=True)

    def get_keys(self, key):
        res = self.conn.keys(key)
        for i in res:
            print(i)
        return res

    def rename_key(self, key, new_key):
        self.conn.rename(key, new_key)

    def get_expire_time(self,key):
        expire_time = self.conn.ttl(key)
        print(expire_time)
        return expire_time

    def get_key_value(self, key):
        key_type = self.conn.type(key)

        if key_type == 'none':
            print('key不存在')
            return 0
        if key_type == 'string':
            res = self.conn.get(key)
        elif key_type == 'hash':
            res = self.conn.hgetall(key)
        elif key_type == 'zset':
            print(self.conn.zcard(key))
            res = self.conn.zrange(key, 0, -1, False, True, int)
        elif key_type == 'list':
            res = self.conn.lrange(key, 0, -1)
        elif key_type == 'set':
            res = self.conn.smembers(key)
        else:
            res = None
        print('type:' + key_type)

        if isinstance(res, str):
            print(res)
        elif key_type == 'hash':
            for i in res.items():
                print(i)
        elif isinstance(res, Iterable):
            print(type(res))
            for i in res:
                print(i)
        return res

    def add_string_key(self, key, string):
        self.conn.set(key, string, ex=86400)
        print('添加成功')

    def set_string_value(self, key, string):
        if isinstance(self.conn.type(key), str):
            res = self.conn.getset(key, string)
            print(res, string)
        else:
            print('key不是string类型')

    def set_zset_value(self, key, data):
        # data类型为字典
        self.conn.zadd(key, data)
        print('添加成功')

    def remove_zset_value(self, key, *values):
        self.conn.zrem(key, *values)
        print('删除成功')

    def delete_key(self, key):
        self.conn.delete(key)
        self.conn.close()
        print('删除成功')

    def delete_keys(self, key_list):
        for i in key_list:
            self.get_key_value(i)
            self.delete_key(i)
            print('删除成功')

    def close_connection(self):
        self.conn.close()


class MysqlUtils:
    def connect_database(self, database='kkk'):
        self.db = pymysql.connect(host='89999.202', user='root', password='kkkk', database=database)

    def get_db_data(self, sql):
        key_word = ['insert', 'truncate', 'drop', 'delete', 'update']
        if common.is_kw_exist(key_word, sql):
            return '禁止使用更新删除语句'
        if not common.is_kw_exist(['where', 'limit'], sql):
            return '请尽量避免使用全量查询'
        else:
            cursor = self.db.cursor()
            cursor.execute(sql)
            data = cursor.fetchall()
            cursor.close()
        return data

    def edit_db_data(self, sql):
        key_word = ['select', 'truncate', 'drop']
        if common.is_kw_exist(key_word, sql):
            print('非DML语句')
            return
        if not common.is_kw_exist(['where', 'limit'], sql):
            print('请避免使用全量更新删除')
            return
        else:
            cursor = self.db.cursor()
            cursor.execute(sql)
            cursor.execute('commit')
            cursor.close()

    def close_db(self):
        self.db.close()


if __name__ == '__main__':
    rd = RedisUtils()
    rd.connect_redis()



