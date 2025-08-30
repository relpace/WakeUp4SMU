

def write_schedule(courses_list, date, last_week, term_name):
    with open("export.wakeup_schedule", "w", encoding="utf-8") as f:
        # 固定开头
        f.write(
            '{"courseLen":50,"id":1,"name":"\\u9ed8\\u8ba4","sameBreakLen":false,"sameLen":true,"theBreakLen":10}\n')
        f.write(
            '[{"endTime":"08:50","node":1,"startTime":"08:00","timeTable":1},{"endTime":"09:50","node":2,"startTime":"09:00","timeTable":1},{"endTime":"11:00","node":3,"startTime":"10:10","timeTable":1},{"endTime":"12:00","node":4,"startTime":"11:10","timeTable":1},{"endTime":"14:50","node":5,"startTime":"14:00","timeTable":1},{"endTime":"15:50","node":6,"startTime":"15:00","timeTable":1},{"endTime":"17:00","node":7,"startTime":"16:10","timeTable":1},{"endTime":"18:00","node":8,"startTime":"17:10","timeTable":1},{"endTime":"19:20","node":9,"startTime":"18:30","timeTable":1},{"endTime":"20:20","node":10,"startTime":"19:30","timeTable":1},{"endTime":"21:20","node":11,"startTime":"20:30","timeTable":1},{"endTime":"21:30","node":12,"startTime":"21:25","timeTable":1},{"endTime":"21:40","node":13,"startTime":"21:35","timeTable":1},{"endTime":"21:50","node":14,"startTime":"21:45","timeTable":1},{"endTime":"22:00","node":15,"startTime":"21:55","timeTable":1},{"endTime":"22:10","node":16,"startTime":"22:05","timeTable":1},{"endTime":"22:20","node":17,"startTime":"22:15","timeTable":1},{"endTime":"22:30","node":18,"startTime":"22:25","timeTable":1},{"endTime":"22:40","node":19,"startTime":"22:35","timeTable":1},{"endTime":"22:50","node":20,"startTime":"22:45","timeTable":1},{"endTime":"23:00","node":21,"startTime":"22:55","timeTable":1},{"endTime":"23:10","node":22,"startTime":"23:05","timeTable":1},{"endTime":"23:20","node":23,"startTime":"23:15","timeTable":1},{"endTime":"23:30","node":24,"startTime":"23:25","timeTable":1},{"endTime":"23:40","node":25,"startTime":"23:35","timeTable":1},{"endTime":"23:50","node":26,"startTime":"23:45","timeTable":1},{"endTime":"23:55","node":27,"startTime":"23:51","timeTable":1},{"endTime":"23:59","node":28,"startTime":"23:56","timeTable":1},{"endTime":"00:00","node":29,"startTime":"00:00","timeTable":1},{"endTime":"00:00","node":30,"startTime":"00:00","timeTable":1}]\n')
        # 学期信息
        f.write(
            '{"background":"","courseTextColor":-1,"id":1,"itemAlpha":60,"itemHeight":64,"itemTextSize":12,"maxWeek":' + str(
                last_week) + ',"nodes":11,"showOtherWeekCourse":true,"showSat":true,"showSun":true,"showTime":false,"startDate":"' + date.strftime(
                '%Y-%m-%d') + '","strokeColor":-2130706433,"sundayFirst":false,"tableName":"\\u5357\\u5927' + str(
                term_name.encode("unicode_escape"))[2:-1].replace("\\\\",
                                                                  "\\") + '","textColor":-16777216,"timeTable":1,"type":0,"widgetCourseTextColor":-1,"widgetItemAlpha":60,"widgetItemHeight":64,"widgetItemTextSize":12,"widgetStrokeColor":-2130706433,"widgetTextColor":-16777216}\n')
        # 课程信息
        logging.info("课程总数: " + str(len(courses_list)))
        colors = ["#ff" + ''.join([random.choice('0123456789abcdef') for j in range(6)])
                  for i in range(len(courses_list))]
        # print(colors)

        course_json = []
        cid = 0
        for j in courses_list:
            course_json.append(
                {"color": colors[cid], "courseName": courses_list[j]['name'], "credit": 0.0, "id": cid, "note": j,
                 "tableId": 1})
            courses_list[j]['cid'] = cid
            cid += 1
        f.write(json.dumps(course_json) + "\n")

        # 课程时间信息
        course_time = []
        for j in courses_list:
            for t in courses_list[j]['time']:
                for week in courses_list[j]['time'][t]:
                    course_time.append({
                        "day": t[0],
                        "endTime": "",
                        "endWeek": week,
                        "startWeek": week,
                        "id": courses_list[j]['cid'],
                        "level": 0,
                        "ownTime": False,
                        "room": t[2],
                        "startNode": t[1][0],
                        "startTime": "",
                        "step": len(t[1]),
                        "tableId": 1,
                        "teacher": t[3],
                        "type": 0
                    })
        f.write(json.dumps(course_time) + "\n")
