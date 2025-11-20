import requests
import pyperclip
from smulogin import login
from fetcher import fetch_week_event
from aggregate import aggregate
from export import write_schedule, upload_schedule, export_to_ics
from maskpass import askpass
import datetime

def notice():
    print('''
    ============================================================
                      使用须知 Notice
    ============================================================
    本项目已在 GitHub 开源：
      https://github.com/relpace/WakeUp4SMU
    
    脚本在运行后不会储存您的任何个人信息。
    您的教务账号与密码仅会被发送到南方医科大学官方教务系统。
    
    请确保您运行的是未经修改的程序副本。
    
    为保障账号安全，建议从 Release 页面下载最新版本：
      https://github.com/relpace/WakeUp4SMU/releases/latest
    ============================================================
    '''
          )
    q()

def q():
    ans = input("是否继续运行？ (y/n):")
    if ans == "y":
        return 0
    elif ans == "n":
        exit(0)
    else:
        q()




def main():
    notice()
    account = input("请输入教务账号")
    password = askpass(prompt="请输入密码",mask="●")
    weeks = int(input("请输入学期周数"))
    start_date = input("请输入学期起始日期（YYYY-M-D，如:2025-9-1）")
    session = requests.Session()
    login(account, password, session)
    se = list(fetch_week_event(session,1,weeks))
    course, aggregated_course = aggregate(se)
    
    print("请选择导出方式：")
    print("1. 导入到 WakeUp ")
    print("2. 导出为 ICS 文件 (日历)")
    print("3. 同时导出")
    choice = input("请输入选项 (1/2/3): ")
    
    if choice in ["1", "3"]:
        write_schedule(course, start_date, weeks, aggregated_course)
        r = upload_schedule()
        print(">>>>>>>>>>请将以下内容发送到手机在WakeUp软件内导入（已复制至剪贴板）<<<<<<<<<<")
        shareinfo= "这是来自「WakeUp课程表」的课表分享，30分钟内有效哦，如果失效请朋友再分享一遍叭。为了保护隐私我们选择不监听你的剪贴板，请复制这条消息后，打开App的主界面，右上角第二个按钮 -> 从分享口令导入，按操作提示即可完成导入~分享口令为「" + r.json()['data'] + "」"
        pyperclip.copy(shareinfo)
        print(shareinfo)
        
    if choice in ["2", "3"]:
        try:
            y, m, d = map(int, start_date.split('-'))
            s_date = datetime.date(y, m, d)
            ics_content = export_to_ics(se, s_date)
            with open("schedule.ics", "w", encoding="utf-8") as f:
                f.write(ics_content)
            print("ICS 文件已导出为 schedule.ics")
        except ValueError:
            print("日期格式错误，无法导出 ICS")

    input("按回车键退出...")
if __name__ == "__main__":
    main()


