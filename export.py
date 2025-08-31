import json
import requests
import models
import timetable
import logging
import random
from models import AggregatedCourse




def write_schedule(courses_list:dict, date, last_week, aggregated_courses: list[AggregatedCourse]):
    with open("export.wakeup_schedule", "w", encoding="utf-8") as f:
        # 固定开头
        f.write(
            '{"courseLen":50,"id":1,"name":"SMU","sameBreakLen":false,"sameLen":true,"theBreakLen":10}\n')
        f.write(
            timetable.TimeTable(int(input("请选择课表时间类别：\n1. 本部课表 2. 顺德课表\n请输入对应数字(1 or 2)\n")))+"\n")
        # 学期信息
        f.write(
            '{"background":"","courseTextColor":-1,"id":1,"itemAlpha":60,"itemHeight":64,"itemTextSize":12,"maxWeek":' + str(
                last_week) + ',"nodes":11,"showOtherWeekCourse":false,"showSat":true,"showSun":true,"showTime":false,"startDate":"' + date + '","strokeColor":-2130706433,"sundayFirst":false,"tableName":"SMU-'+date+'","textColor":-16777216,"timeTable":1,"type":0,"widgetCourseTextColor":-1,"widgetItemAlpha":60,"widgetItemHeight":64,"widgetItemTextSize":12,"widgetStrokeColor":-2130706433,"widgetTextColor":-16777216}\n')
        # 课程信息
        logging.info("课程总数: " + str(len(courses_list)))
        colors = ["#FF6B6B", "#FF9F43", "#FFC048", "#FFD93D", "#6BCB77", "#38A169", "#4ECDC4", "#1ABC9C", "#3498DB",
                  "#2C82C9", "#6A5ACD", "#9B59B6", "#D980FA", "#E84393", "#FF7675", "#FFB8B8", "#A29BFE", "#00B894",
                  "#0984E3", "#2D3436"]
        random.shuffle(colors)

        course_json = []
        cid = 0
        for j in courses_list.keys():
            course_json.append(
                {"color": colors[cid], "courseName": j, "credit": 0.0, "id": courses_list[j], "note": "",
                 "tableId": 1})
            cid += 1
        f.write(json.dumps(course_json) + "\n")

        # 课程时间信息
        course_time = []
        for e in aggregated_courses:
            course_time.append({
                "day": e.xq,
                "endTime": "",
                "endWeek": e.zc[-1],
                "startWeek": e.zc[0],
                "id": courses_list[e.kcmc],
                "level": 0,
                "ownTime": False,
                "room": e.jxcdmc,
                "startNode": e.ps,
                "startTime": "",
                "step": e.pe-e.ps+1,
                "tableId": 1,
                "teacher": e.teaxms,
                "type": 0
            })
        f.write(json.dumps(course_time) + "\n")

def upload_schedule():
    r = requests.post("https://i.wakeup.fun/share_schedule", data={
        "schedule": open("export.wakeup_schedule", "r", encoding="utf-8").read()
    }, headers={
        "version": "180",
        "User-Agent": "okhttp/3.14.9"
    })
    return r
