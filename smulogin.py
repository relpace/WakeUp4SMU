import time
from io import BytesIO
from PIL import Image
from hashlib import md5
import json

captcha_url = "https://uis.smu.edu.cn/imageServlet.do"
login_url = "https://uis.smu.edu.cn/login/login.do"

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Connection": "keep-alive",
    "Host": "zhjw.smu.edu.cn",
    "Referer": "https://zhjw.smu.edu.cn/",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
}


def login( account, password, session):
    captcha = get_captcha(session)
    ticket = sendlogin(account, password, captcha, session)
    redirect_login(session, ticket)


def get_captcha(session):
    headers_captcha = {
    'Accept': 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br, zstd',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    'Host': 'uis.smu.edu.cn',
    'Referer': 'https://uis.smu.edu.cn/login.jsp?outLine=0',
    'Sec-Fetch-Dest': 'image',
    'Sec-Fetch-Mode': 'no-cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Chromium";v="140", "Not=A?Brand";v="24", "Google Chrome";v="140"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"'
    }
    captcha_response = session.get(captcha_url, headers=headers_captcha)
    img = Image.open(BytesIO(captcha_response.content))
    img.show()
    captcha = input("请输入验证码: ")
    return captcha

def sendlogin(account, password, captcha, session):
    password_md5 = md5(password.encode()).hexdigest()
    headers = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Content-Length': '234',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Host': 'uis.smu.edu.cn',
        'Origin': 'https://uis.smu.edu.cn',
        'Referer': 'https://uis.smu.edu.cn/login.jsp?redirect=https%3A%2F%2Fzhjw.smu.edu.cn%2Fnew%2FssoLogin',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36',
        'X-KL-kis-Ajax-Request': 'Ajax_Request',
        'X-Requested-With': 'XMLHttpRequest',
        'sec-ch-ua': '"Chromium";v="140", "Not=A?Brand";v="24", "Google Chrome";v="140"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"'
    }
    data = {
        "loginName": account,
        "password": password_md5,
        "randcodekey": captcha,
        "locationBrowser": "谷歌浏览器[Chrome]",
        "appid": "3550176",
        "redirect": "https://zhjw.smu.edu.cn/new/ssoLogin",
        "strength": 3
    }
    response = session.post(login_url, data=data, headers=headers)
    if response.status_code == 200 and "成功" in response.text:
        resp_json = json.loads(response.text)
        print("登录成功")
        ticket = resp_json["ticket"]
        return ticket
    else:
        print("登录失败，原因：", response.text)

def redirect_login(session, ticket):
    url = "https://zhjw.smu.edu.cn/new/ssoLogin"
    params = {
        "ticket": ticket,
    }
    resp = session.get(url, headers=headers, params=params)
    print(resp.status_code)

