import requests
from bs4 import BeautifulSoup
import smulogin
import re
import models
headers = smulogin.headers


def get_xnxqdm(session):
    main_url = "https://zhjw.smu.edu.cn/new/student/xsgrkb/main.page"
    response = session.get(main_url, headers=headers)
    soup = BeautifulSoup(response.text, features="html.parser")
    scripts = soup.find_all("script")
    xnxqdm = None
    for script in scripts:
        if script.string:
            match = re.search(r"xnxqdm=(\d+)", script.string)
            if match:
                xnxqdm = match.group(1)
                break
    return xnxqdm

def fetch_week_event(session,  startweek:int, endweek:int):
    xnxqdm = get_xnxqdm(session)
    url = "https://zhjw.smu.edu.cn/new/student/xsgrkb/getCalendarWeekDatas"
    for week in range(startweek, endweek+1):
        payload = {
            "xnxqdm": xnxqdm,
            "zc": week
        }
        response = session.post(url, data=payload, headers=headers)
        resp_json = response.json()
        if resp_json["data"]:
            for i in resp_json["data"]:
                event = models.SingleEvent(i["kcmc"], i["jxcdmc"], i["jxhjmc"],
                                           i["teaxms"], i["xq"], i["xs"],
                                           i["qssj"][:-3], i["jssj"][:-3], int(i["ps"]),
                                           int(i["pe"]), int(i["zc"]))
                yield event
