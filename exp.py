#!/usr/bin/env python
# -*-coding:utf-8-*-
import requests
import re
import json
import time
import sys


class bilibili:
    cookies = ""

    def __init__(self, cookies):
        self.cookies = cookies

    def start(self):
        detail = self.getDetail()
        if detail["coins_av"] == 50:
            print("Feed complete")
            return
        else:
            left = (50 - detail["coins_av"]) / 10
            av = self.getAV()
            print(av)
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

    def feed(self, av):
        url = "https://www.bilibili.com/plus/comment.php"
        head = {
            "Cookie": self.cookies,
            "Referer": "https://www.bilibili.com/video/" + av + "/",
        }
        csrf = re.findall("bili_jct=(.*?);", self.cookies, re.S)[0]
        print(csrf)
        param = {
            "aid": av,
            "rating": "100",
            "player": "1",
            "multiply": "1",
            "csrf": csrf
        }
        html = requests.post(url, headers=head, data=param)
        return html.text

    def getAV(self):
        url = "https://www.bilibili.com/newlist.html"
        html = requests.get(url).text
        result = re.findall("<ul class=\"vd_list\">(.*?)</ul>", html, re.S)[0]
        av = re.findall('<a href="/video/av(.*?)/" target="_blank"', result, re.S)
        return list(set(av))

    def getDetail(self):
        url = "https://account.bilibili.com/home/reward"
        head = {
            "Cookie": self.cookies,
        }
        result = {}
        try:
            result = json.loads(requests.get(url, headers=head).text)
        except:
            exit("Access error")
        if result["code"] != 0:
            exit("Cookies error")
        else:
            return result["data"]


while True:
    if len(sys.argv) == 1:
        exit("please pass cookies as command-line arguments")
    else:
        b = bilibili(sys.argv[1])
        b.start()
        time.sleep(3600 * 24)
