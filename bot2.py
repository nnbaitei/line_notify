import pandas as pd
import datetime
import requests
import time
import schedule

def readfile():
    global df
    df = pd.read_csv('schedule_edit.csv')
    # Convert day and start time to datetime for easier comparison
    df['start_datetime'] = pd.to_datetime(df['day'] + ' ' + df['time'].str.split('-').str[0], format='%a %H:%M', errors='coerce')
    df['end_datetime'] = pd.to_datetime(df['day'] + ' ' + df['time'].str.split('-').str[1], format='%a %H:%M', errors='coerce')
    return df

def line_notify(message):
    url = 'https://notify-api.line.me/api/notify'
    token = 'JmQNU87WwUp8Gb291dYueYJBIAaOqVoLCVlUoxhvsOD'
    headers = {'content-type':'application/x-www-form-urlencoded','Authorization':'Bearer '+token}
    r = requests.post(url, headers=headers, data = {'message':message})
    print(r.text)

def find_next_class(df, now):
    future_classes = df[df['start_datetime'] > now]
    if not future_classes.empty:
        next_class = future_classes.iloc[0]
        message = f"คาบเรียนถัดไป\nวิชา {next_class['class']}\nเวลา {next_class['time']}\nสถานที่ {next_class['room']}\nอาจารย์ผู้สอน {next_class['teacher']}."
    else:
        message = "No more classes today."
    print(message)
    line_notify(message)

def check_current_class(df, now):
    current_class = df[(df['start_datetime'] <= now) & (df['end_datetime'] > now)]
    if not current_class.empty:
        current_class = current_class.iloc[0]
        message = f"คาบเรียนปัจจุบัน\nวิชา {current_class['class']}\nเวลา {current_class['time']}\nสถานที่ {current_class['room']}\nอาจารย์ผู้สอน {current_class['teacher']}."
    else:
        message = "No class at the moment."
    print(message)
    line_notify(message)

# def notify_for_classes(df):
#     now = datetime.datetime.now()
#     today_classes = df[df['start_datetime'].dt.date == now.date()]
#     for _, class_row in today_classes.iterrows():
#         if 0 <= (class_row['start_datetime'] - now).total_seconds() / 60 <= 15:
#             message = f"Class starting soon: {class_row['class']} at {class_row['time']} in room {class_row['room']} with {class_row['teacher']}."
#             print(message)
#             line_notify(message)

def find_previous_class(df, now):
    past_classes = df[df['end_datetime'] < now]
    if not past_classes.empty:
        previous_class = past_classes.iloc[-1]  # Get the last class that ended
        message = f"คาบเรียนก่อนหน้า\nวิชา {previous_class['class']}\nเวลา {previous_class['time']}\nสถานที่ {previous_class['room']}\nอาจารย์ผู้สอน {previous_class['teacher']}."
    else:
        message = "No previous classes today."
    print(message)
    line_notify(message)

def all_class(df):
    message = ['คาบเรียนทั้งหมด\n']
    for i in range(len(df)):
        # print(df['class'][i])
        text = f"วิชา {df['class'][i]}\nเวลา {df['day'][i]} {df['time'][i]}\nสถานที่ {df['room'][i]}\nอาจารย์ผู้สอน {df['teacher'][i]}\n\n"
        message.append(text)
    # print(message)
    print(''.join(message))
    line_notify(''.join(message))

def find_class(df, day):
    t = []
    day_time = df[df['day'] == day]['time'].index
    for i in range(len(day_time)):
        select_time = str([day_time[i]]) + ' ' + df[df['day'] == day]['time'][day_time[i]]
        t.append(select_time)
    for i in (t):
        print(i)
    time_input = input('กดหมายเลขตามเวลาที่ต้องการ: ')  
    text = f"วัน {df['day'][int(time_input)]} เวลา {df['time'][int(time_input)]}\nวิชา {df['class'][int(time_input)]}\nสถานที่ {df['room'][int(time_input)]}\nอาจารย์ผู้สอน {df['teacher'][int(time_input)]}"
    return text

def select_class(df):
    day = input("เลือกวัน\nกด 'm' คาบวันจันทร์\nกด 't' คาบวันอังคาร\nกด 'w' คาบวันพุธ\nกด 'th' คาบวันพฤหัส\nกด 'f' คาบวันศุกร์\n")
    if day == 'm':
        day = 'Mon'
    if day == 't':
        day = 'Tue'
    if day == 'w':
        day = 'Wed'
    if day == 'th':
        day = 'Thu'
    if day == 'f':
        day = 'Fri'
    message = find_class(df, day)
    print(message)
    line_notify(message)

def job():
    curr_day = datetime.datetime.now().strftime("%a")
    df_day_index = df[df['day'] == curr_day].index
    df_day = df[df['day'] == curr_day]
    for i in df_day_index:
        message = f"วัน {df_day['day'][i]} เวลา {df_day['time'][i]}\nวิชา {df_day['class'][i]}\nสถานที่ {df_day['room'][i]}\nอาจารย์ผู้สอน {df_day['teacher'][i]}"
        print(message)
        line_notify(message)
    time.sleep(60)

def main():
    df = readfile()
    while True:
        schedule.run_pending()
        now = datetime.datetime.now()
        user_input = input("กด 'x' เพื่อดูคาบเรียนถัดไป\nกด 'y' คาบเรียนปัจจุบัน\nกด 'o' คาบเรียนก่อนหน้า\nกด 'a' แสดงตารางทั้งหมด\nกด 'p' เลือกวัน และเวลา\nกด 'e' ออกจากโปรแกรม\n").lower()
        if user_input == 'x':
            find_next_class(df, now)
        elif user_input == 'y':
            check_current_class(df, now)
        elif user_input == 'o':
            find_previous_class(df, now)
        # elif user_input == 'n':
        #     notify_for_classes(df)
        elif user_input == 'a':
            all_class(df)
        elif user_input == 'p':
            select_class(df)
        elif user_input == 'e':
            print("Exiting program.")
            break
        else:
            print("Invalid input. Please try again.")
        time.sleep(1)  # Add delay to avoid spamming

if __name__ == "__main__":
    schedule.every().day.at("08:00").do(job)
    main()