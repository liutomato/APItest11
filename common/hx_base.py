import requests
from websocket import create_connection
from common.hx_mysql import RedisUtils, MysqlUtils
import json
import hashlib
import common


class KBase:
    def __init__(self):  # common的构造函数
        self.redis = RedisUtils()
        self.db = MysqlUtils()
        self.session = requests.session()
        self.headers = {
            'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36'
        }
        self.param = {}

    def get(self, url, params=''):
        url = url
        res = self.session.get(url, headers=self.headers, params=params, verify=False)  # 通过get请求访问对应地址
        res.encoding = "uft-8"
        return res  # 返回request的Response结果，类型为requests的Response类型

    def post(self, url, params=None, data=None):
        res = self.session.post(url, headers=self.headers, params=params, data=data, verify=False)
        res.encoding = "uft-8"
        return res

    @staticmethod
    def delete(url, params=None):
        """
        封装Delete方法，如果没有参数，默认为空
        :param url: 访问路由
        :param params: 传递参数，string类型，默认为None
        :return: 此次访问的response
        """
        res = requests.delete(url, data=params, verify=False)
        return res

    @staticmethod
    def send(url, params):
        """
        :param url: 接口链接
        :param params: websocket接口的参数
        :return: 访问接口的返回值
        """
        ws = create_connection(url)
        ws.send(params)  # 发送参数
        res = ws.recv()  # 接收返回数据
        ws.close()  # 关闭 WebSocket 长链接
        return res

    def admin_user_login(self, username='雨夜归鸿'):
        """
            调用登录接口登录后更新cookie值供其他接口测试使用
        """
        url = "https://.K.com/login_action"
        param = {
            "username": username,
            "password": "123456",
            "password2": "",
        }
        self.session.post(url, headers=self.headers, data=param, verify=False, allow_redirects=True)


    def pc_user_login(self, username='狗头护'):
        """
            调用登录接口登录后更新cookie值供其他接口测试使用
        """
        url = "https://test-kkk"
        param = {
            "username": username,
            "password": "123456"
        }

        self.session.post(url, headers=self.headers, data=param, verify=False, allow_redirects=True)


    def get_app_sign(self, uid=None):
        url = 'https://t-apikkkk'
        s = 'hx_test_generate_sign'
        s = s.encode(encoding='utf-8')
        st = hashlib.md5(s).hexdigest()
        payload = {'sign': st, 'uid': uid}
        res = self.post(url, data=payload).text
        data = json.loads(res)['data']
        return data

    @staticmethod
    def get_testcase_version():
        version = common.get_trace(3)
        return common.get_single_word(version, -1)


if __name__ == '__main__':

