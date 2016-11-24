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
        result = requests.get(url, headers=self.headers)
        av = re.findall("\"add_id\":(.*?),", result.text, re.S)
        self.getDetail()
        print("当前经验%d" % self.getDetail()["level_info"]["current_exp"])
        suc = 0
        for i in range(0, len(av)):
            try:
                feedresult = self.feed(av[i])
                if feedresult == "OK":
                    suc += 1
                    if suc == int(left):
                        break
                print("对视频AV" + av[i] + "投币结果：" + feedresult)
                print("当前经验%d" % self.getDetail()["level_info"]["current_exp"])
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


b = BiliBili(
    "fts=1479541115; pgv_pvi=3784498176; buvid3=FDE06719-A15D-47C7-8689-B4965A4E47BA19753infoc; DedeUserID=7336071; DedeUserID__ckMd5=ebb9df7cdf51b2e3; SESSDATA=ae657326%2C1487404998%2C1259bef7; ck_pv=9G91DO; SSID=wtz2_aj6WnBI0rAtUvTTNg2OLkL0yF02VJ0Sf2VKpK1uGGpRAdCb8RsmxH6fRcaWxv7WPZc18k3rAPE3sSbNGqZdeSFu_bLgpk8tjcmvvBdpY_c; _ver=1; sid=d12mfkqd; _cnt_dyn=null; _cnt_pm=0; _cnt_notify=30; uTZ=-480; _dfcaptcha=d5ff3e2168b696ddd41b3e717cf8384c; pgv_si=s7209502720; CNZZDATA2724999=cnzz_eid%3D1824815920-1479541114-null%26ntime%3D1479716935")
b.auto()
