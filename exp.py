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
            print("本日已投币完成")
            return
        else:
            left = (50 - detail["coins_av"]) / 10
            self.__getAvNum(left)

    def __getAvNum(self, left):
        url = "http://api.bilibili.com/x/feed/pull?callback=jQuery17203775818979021903_1479630274810&jsonp=jsonp&ps=10&type=1&_=1479630274907"
        self.headers["host"] = "api.bilibili.com"
        self.headers["refer"] = "http://www.bilibili.com/account/dynamic"
        self.headers.update()
        result = requests.get(url, headers=self.headers)
        av = re.findall("\"add_id\":(.*?),", result.text, re.S)
        self.getDetail()
        print("当前经验%d" % self.getDetail()["level_info"]["current_exp"])
        for i in range(0, int(left)):
            try:
                print("对视频AV" + av[i] + "投币结果：" + self.feed(av[i]))
                print("当前经验%s" % self.getDetail()["level_info"]["current_exp"])
            except:
                exit("也许无关注用户")

    def getDetail(self):
        url = "https://account.bilibili.com/home/reward"
        self.headers["host"] = "account.bilibili.com"
        try:
            result = json.loads(requests.get(url, headers=self.headers).text)
        except:
            exit("error")
        if result["code"] != 0:
            exit("cookies有误")
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


b = BiliBili("cookies")
b.auto()
