import pandas as pd
import datetime
import requests
import time

def readfile():
    df = pd.read_csv('schedule_edit.csv')
    return df

def line_notify(code, sub, room, teacher):
    url = 'https://notify-api.line.me/api/notify'
    token = 'JTNnHKrSHvOMlp47LOw3Wsg7dHtFvT24zlsS64PScFD'
    headers = {'content-type':'application/x-www-form-urlencoded','Authorization':'Bearer '+token}
    msg = f"\nรหัสวิชา: {code}\nวิชา: {sub}\nห้องเรียน: {room}\nอาจารย์ผู้สอน: {teacher}"
    r = requests.post(url, headers=headers, data = {'message':msg})
    print (r.text)

def mon(curr_hr, curr_min):
    df = readfile()
    t_hr = 13
    if curr_hr - t_hr == -1 and curr_min == 45:
        df = df[df['time'] == '13:00-18:00']
        df = df[df['day'] == 'Mon']
        code = df['code'].values[0]
        sub = df['class'].values[0]
        room = df['room'].values[0]
        teacher = df['teacher'].values[0]
        line_notify(code, sub, room, teacher)

def tue(curr_hr, curr_min):
    df = readfile()
    t1_hr = 8
    t2_hr = 16
    if curr_hr - t1_hr == -1 and curr_min == 45:
        df = df[df['time'] == '8:00-11:00']
        df = df[df['day'] == 'Tue']
        code = df['code'].values[0]
        sub = df['class'].values[0]
        room = df['room'].values[0]
        teacher = df['teacher'].values[0]
        line_notify(code, sub, room, teacher)
        
    if curr_hr - t2_hr == -1 and curr_min == 45:
        df = df[df['time'] == '16:00-19:00']
        df = df[df['day'] == 'Tue']
        code = df['code'].values[0]
        sub = df['class'].values[0]
        room = df['room'].values[0]
        teacher = df['teacher'].values[0]
        line_notify(code, sub, room, teacher)

def wed(curr_hr, curr_min):
    df = readfile()
    t1_hr = 8
    t2_hr = 13
    if curr_hr - t1_hr == -1 and curr_min == 45:
        df = df[df['time'] == '8:00-11:00']
        df = df[df['day'] == 'Wed']
        code = df['code'].values[0]
        sub = df['class'].values[0]
        room = df['room'].values[0]
        teacher = df['teacher'].values[0]
        line_notify(code, sub, room, teacher)
        
    if curr_hr - t2_hr == -1 and curr_min == 45:
        df = df[df['time'] == '13:00-17:00']
        df = df[df['day'] == 'Wed']
        code = df['code'].values[0]
        sub = df['class'].values[0]
        room = df['room'].values[0]
        teacher = df['teacher'].values[0]
        line_notify(code, sub, room, teacher)
        

def thu(curr_hr, curr_min):
    df = readfile()
    t_hr = 8
    if curr_hr - t_hr == -1 and curr_min == 45:
        df = df[df['time'] == '8:00-11:00']
        df = df[df['day'] == 'Thu']
        code = df['code'].values[0]
        sub = df['class'].values[0]
        room = df['room'].values[0]
        teacher = df['teacher'].values[0]
        line_notify(code, sub, room, teacher)
        

def fri(curr_hr, curr_min):
    df = readfile()
    t_hr = 8
    if curr_hr - t_hr == -1 and curr_min == 45:
        df = df[df['time'] == '8:00-11:00']
        df = df[df['day'] == 'Fri']
        code = df['code'].values[0]
        sub = df['class'].values[0]
        room = df['room'].values[0]
        teacher = df['teacher'].values[0]
        line_notify(code, sub, room, teacher)
        time.sleep(60)
        
    
while True:
    curr_day = datetime.datetime.now().strftime("%a")
    curr_hr = int(datetime.datetime.now().strftime("%H"))
    curr_min = int(datetime.datetime.now().strftime("%M"))

    if curr_day == "Mon":
        mon(curr_hr, curr_min)
    if curr_day == "Tue":
        tue(curr_hr, curr_min)
    if curr_day == "Wed":
        wed(curr_hr, curr_min)
    if curr_day == "Thu":
        thu(curr_hr, curr_min)
    if curr_day == "Fri":
        fri(curr_hr, curr_min)

