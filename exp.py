#!/usr/bin/env python
# -*-coding:utf-8-*-
import requests
import re
import json


class BiliBili:
    headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, sdch",
        "Accept-Language": "zh-CN,zh;q=0.8",
        "Cache-Control": "max-age=0",
        "Connection": "keep-alive",
        "Cookie": "",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36"
    }

    def __init__(self, cookies):
        self.headers["Cookie"] = cookies

    def auto(self):
        detail = self.getDetail()
        if detail["coins_av"] == 50:
            print("Feed complete")
            return
        else:
            left = (50 - detail["coins_av"]) / 10
            av = self.__getAvNum()
            suc = 0
            for i in range(0, len(av)):
                try:
                    feedresult = self.feed(av[i])
                    if feedresult == "OK":
                        suc += 1
                    print("Feeding AV" + av[i] + "result:" + feedresult)
                    print("Current exp:%d" % self.getDetail()["level_info"]["current_exp"])
                    if suc == left:
                        break
                except:
                    exit("Feed error")

    def __getAvNum(self):
        url = "http://www.bilibili.com/newlist.html"
        html = requests.get(url).text
        result = re.findall("<ul class=\"vd_list\">(.*?)</ul>", html, re.S)[0]
        av = re.findall('<a href="/video/av(.*?)/" target="_blank"', result, re.S)
        return list(set(av))

    def getDetail(self):
        url = "https://account.bilibili.com/home/reward"
        self.headers["host"] = "account.bilibili.com"
        try:
            result = json.loads(requests.get(url, headers=self.headers).text)
        except:
            exit("Access error")
        if result["code"] != 0:
            exit("Cookies error")
        else:
            return result["data"]

    def feed(self, av):
        url = "http://www.bilibili.com/plus/comment.php"
        self.headers["refer"] = "http://www.bilibili.com/video/av" + av + "/"
        self.headers["host"] = "www.bilibili.com"
        self.headers["Origin"] = "http://www.bilibili.com"
        param = {
            "aid": av,
            "rating": "100",
            "player": "1",
            "multiply": "1"
        }
        result = requests.post(url, headers=self.headers, params=param).text
        return result


b = BiliBili("")
b.auto()
