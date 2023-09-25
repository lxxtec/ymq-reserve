# -*- encoding: utf-8 -*-
'''
@File    : reserve.py
@Time    : 2022/11/29 11:28:02
@Author  : lxxtec
@Contact : 631859877@qq.com
@Version : 0.1
@Desc    : None
'''
from deco import timer
from json import dumps
from multiprocessing import Manager, Pool, current_process
from concurrent.futures import ThreadPoolExecutor, as_completed, ProcessPoolExecutor
from pprint import pprint
from pathlib import Path
from pickle import dump, load
from queue import Queue
from time import time, sleep
from urllib.parse import urlencode

from requests import get, post, session
from aiohttp import ClientSession


class ReserveSystem:
    def __init__(self) -> None:
        self.url = "http://yuding.hrbeu.edu.cn/Views/Field/FieldOrder.html?VenueNo=002&FieldTypeNo=YMQ001"
        self.look_url = "http://yuding.hrbeu.edu.cn/Views/Field/FieldOrder"
        self.post_url = "http://yuding.hrbeu.edu.cn/Field/OrderField?"
        self.cook = "_ga=GA1.3.1596515228.1668174336; LoginSource=2; UseCookies=2BF896BD0A1963037F97F3EDDFE620DA799963C0A377FE8E98354F9DC4EAFE1DDFEC7F2C8D177D7A0821D070312CEB734EDB962A5CBF218EC9B364B0211A93A3810AEF45ECF28E937B9B861894864AF93539FE856334403AF1C9DFA68625907B698A7C2BC311BBD8B65DEA1930C0A181820AD893FB592E6BD88F79DDCB70B06C57463CF93B0CC9A142B05CE64E44E70B217EC462A4B1F91F69C928DF7BFB9237835117490B0052D4220C144CA446464A0A21BF633A2CFB145BF6C1E03672A6D58BC5EE5CCC490FD4E3A2F97D1F0D51E624E3186A1281287A439D408AA0A584D35EC2E812AFA6E5617301F857D2F11982; LoginType=1; JWTUserToken=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJuYW1lIjoiMGU1YzgwNTktMGY4Ni00MDg1LTgzNTMtYTMzMjNiMDM3NmU3IiwiZXhwIjoxNjcwMzM5Mjc5LjAsImp0aSI6ImxnIiwiaWF0IjoiMjAyMi0xMS0yOSAxNTowNzo1OSJ9.XhQq0kOJhakCu6TWYyakkYNvpwghzrir-q_FrFkM3dY; UserId=0e5c8059-0f86-4085-8353-a3323b0376e7; ASP.NET_SessionId=vyq50vtynykc4zdpefdc1ekl"

        self.headers = {
            "Accept": "*/*",
            # "Cookie": self.cook,
            "Accept-Encoding": "gzip",
            "Accept-Language": "zh-CN",
            "Connection": "keep-alive",
            "Host": "yuding.hrbeu.edu.cn",
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1 Edg/103.0.5060.114",
            "X-Requested-With": "XMLHttpRequest",
            "Referer": "http://yuding.hrbeu.edu.cn/Views/Field/FieldOrder.html?VenueNo=002&FieldTypeNo=YMQ001"
        }
        # cookie = "_ga=GA1.3.695289157.1627136444; UseCookies=F097971B24CC2FC5C05641980CAA7A86A55DB7B6803C7BEBEEB44BA96E6C780B512DAC9F49D4EEE3DA56E3C201495456DE0D7F90BBBF8B4DDE0BB5D91B6BAA02D51C4DEE4A86B25CFCAC5FC3611F5BC7723F3F049EB1FA6CB559191685029E9FC91780690E108BBB8B736BD81B98EB02D64267C87B6B8AF940FD34D8E04EFC979E9520A27392EB345E5DD77CDA37126592F94F582E11AF2FCE5EC4CC6E0FFBCE5869F9B7A6BAA390C7A86F3FF17A6D84A08740BAA5C7CDA745A72A20CED56CB3E2A3FF9F0F799A9F05D3233611AA0B3AF52B2431EB1A13048FB7EB8F6BB557698743F931B6D15B5671982184740DA00C; ASP.NET_SessionId=qkdgvkdprad14ycsingcp2bp; LoginType=1; JWTUserToken=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJuYW1lIjoiMGU1YzgwNTktMGY4Ni00MDg1LTgzNTMtYTMzMjNiMDM3NmU3IiwiZXhwIjoxNjcwMTcxMjAzLjAsImp0aSI6ImxnIiwiaWF0IjoiMjAyMi0xMS0yNyAxNjoyNjo0MyJ9.DPQ_wF-IkRpWCXQwJ0QMUir0DXGl2Ct_fH32ttKPKwA; UserId=0e5c8059-0f86-4085-8353-a3323b0376e7; LoginSource=1"
        self.cookie_flag = self.checkCookie()

        self.info = Queue(100)
        self.keys = []
        self.urls = []

    def checkCookie(self):
        path = Path('./ycookie.pkl')
        if path.exists():
            with open('./ycookie.pkl', 'rb') as pk:
                self.cookie = load(pk)
            return True
        return False

    def generate_cookie(self, ssr):
        ss = ssr.split(';')
        ss = [s.strip().split('=') for s in ss]
        cooki = {item[0]: item[1] for item in ss}
        self.cookie = cooki
        self.cook = ssr
        with open('./ycookie.pkl', 'wb') as pk:
            dump(cooki, pk)
        self.cookie_flag = True

    def generate_urls(self, field_list, time_list, date_add):
        for field in field_list:
            for time in time_list:
                check_data = {"FieldNo": "{:0>3d}".format(field+5), "FieldTypeNo": "YMQ001", "FieldName": "羽毛球{:0>2d}".format(field),
                              "BeginTime": "{}:00".format(time), "Endtime": "{}:00".format(time+1), "Price": "25.00"}
                ss = str([check_data])
                ss = ss.replace("'", "\"").encode('utf-8')
                # "[{"FieldNo":"007","FieldTypeNo":"YMQ001","FieldName":"羽毛球02","BeginTime":"8:00","Endtime":"9:00","Price":"25.00"}]"
                data = {
                    "checkdata": ss,
                    "dateadd": str(date_add),
                    "VenueNo": "002"
                }

                url = self.post_url + urlencode(data)
                url = url.replace('+', '')
                key = "{}_{}_{}".format(field, time, date_add)
                self.urls.append(url)
                self.keys.append(key)

    def reserve_once(self, key, url):
        # 提交
        sess = session()
        r1 = sess.get(url, cookies=self.cookie,
                      headers=self.headers, timeout=3)
        print("post status: ", r1.status_code)
        r1.encoding = 'utf-8'
        # print(r1.headers)
        # print(r1.text)
        try:
            res = r1.json()
            if res['type'] == 1:
                print('预定成功!!!')
                info = list(map(int, key.split('_')))
                self.info.put([info[0], info[1], info[2]])
            elif res['type'] == 3:
                print('场地已被占用, 预定失败！')
            # print(res)
        except:
            print('err occurred')

    @timer
    def try_reserve(self):
        # 常规遍历
        for k, u in zip(self.keys, self.urls):
            self.reserve_once(k, u)

    @timer
    def try_reserve_async(self):
        # 并发
        print("multi")
        with ThreadPoolExecutor(max_workers=2) as t:
            t.map(self.reserve_once, self.keys, self.urls)


if __name__ == '__main__':

    rer = ReserveSystem()
    rer.generate_cookie("LoginSource=2; UseCookies=FBD0553BAEFF60C64565C9F1E54E6D58ED5339242E45FF9A66DE671358EB970A7F14A4E1ECC23AC39713C4460AF30176FE52E2E68C5D0F94A91A3FE50C211A4AFCA0AABE248FAC9409AD4EE0363087BF14FC420413EF3448017AAF4D7DEBF5B034744E2848D0E2D59572DA7509163E8D828946C9663729F4C5109F031AD9FB12327EE060C2A0EB7650E0F70521936D171A3E8EC30688048F2A5DF7C028B70FD8DACD4289D4E0F0F2EBEB9D58BC8AE355A6C83C615BCE90C409FD7D933BF056295998A5C8A4B6B0F9A4C765F721FC97AF5FF23809FD97D2339D0B61E06A11206F0E8C93FFE5E3C0416EE95F9C69B0C1AC; ASP.NET_SessionId=e1a4egcmtoaokqpaygpxaea5; LoginType=1; JWTUserToken=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJuYW1lIjoiMGU1YzgwNTktMGY4Ni00MDg1LTgzNTMtYTMzMjNiMDM3NmU3IiwiZXhwIjoxNjczNjM2OTEwLjAsImp0aSI6ImxnIiwiaWF0IjoiMjAyMy0wMS0wNiAxOTowODozMCJ9.p1FtsNQoRlbtvIKrlpbKvOsj7ZmF5JjHAYx8dTgOyFo; UserId=0e5c8059-0f86-4085-8353-a3323b0376e7")
    # rint(rer.cookie)

    rer.generate_urls([1], [15], 1)
    print(rer.urls[0])
    # rer.try_reserve(keys, urls)
    # rer.try_reserve_async()
    # get("http://yuding.hrbeu.edu.cn/Field/OrderField?checkdata=%5B%7B%22FieldNo%22%3A%22009%22%2C%22FieldTypeNo%22%3A%22YMQ001%22%2C%22FieldName%22%3A%22%E7%BE%BD%E6%AF%9B%E7%90%8304%22%2C%22BeginTime%22%3A%228%3A00%22%2C%22Endtime%22%3A%229%3A00%22%2C%22Price%22%3A%2225.00%22%7D%5D&dateadd=1&VenueNo=002",
    #     headers=rer.headers)
    # pprint(urls)

# "[{"FieldNo":"008","FieldTypeNo":"YMQ001","FieldName":"羽毛球03","BeginTime":"8:00","Endtime":"9:00","Price":"25.00"}]"
# 请求 URL: http://yuding.hrbeu.edu.cn/Field/OrderField?checkdata=%5B%7B%22FieldNo%22%3A%22008%22%2C%22FieldTypeNo%22%3A%22YMQ001%22%2C%22FieldName%22%3A%22%E7%BE%BD%E6%AF%9B%E7%90%8303%22%2C%22BeginTime%22%3A%228%3A00%22%2C%22Endtime%22%3A%229%3A00%22%2C%22Price%22%3A%2225.00%22%7D%5D&dateadd=1&VenueNo=002
# 响应"{"IsCardPay":null,"MemberNo":null,"Discount":null,"ConType":null,"type":1,"errorcode":0,"message":"","resultdata":"1f244790-c6a5-47a8-99dc-2738c04ce2fd"}"
