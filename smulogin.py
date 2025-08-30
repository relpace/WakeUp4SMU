import time
from io import BytesIO
from PIL import Image
from bs4 import BeautifulSoup
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

captcha_url = "https://zhjw.smu.edu.cn/yzm?d="
login_url = "https://zhjw.smu.edu.cn/new/login"
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


def encrypt_password(password, verifycode):
    key = (verifycode * 4).encode('utf-8')
    cipher = AES.new(key, AES.MODE_ECB)
    encrypted = cipher.encrypt(pad(password.encode('utf-8'), AES.block_size))
    return encrypted.hex()

def login( account, password, session):
    captcha = get_captcha(session)
    sendlogin(account, password, captcha, session)

def get_captcha(session):
    captcha_response = session.get(captcha_url + str(int(time.time() * 1000)), headers=headers)
    img = Image.open(BytesIO(captcha_response.content))
    img.show()
    captcha = input("请输入验证码: ")
    return captcha

def sendlogin(account, password, captcha, session):
    encrypted_password = encrypt_password(password, captcha)
    data = {
        "account": account,
        "pwd": encrypted_password,
        "verifycode": captcha
    }
    response = session.post(login_url, data=data, headers=headers)
    if response.status_code == 200 and "成功" in response.text:
        print("登录成功")
        print(response.url)

    else:
        print("登录失败，原因：", response.text)

