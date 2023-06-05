import PySimpleGUI as sg
import pyautogui
import sql_database as sql
import time
from datetime import datetime
from datetime import date
import smtplib
from email.message import EmailMessage
def email_alert(suject,body,to):
    msg=EmailMessage()
    msg.set_content(body)
    msg['subject']=suject
    msg['to']=to
    user="remainderproject@gmail.com"
    msg['from']=user
    password="gemacrpnvkbyixdb"
    server = smtplib.SMTP("smtp.gmail.com",587)
    server.starttls()
    server.login(user,password)
    server.send_message(msg)
    server.quit()

now = datetime.now()

current_time = now.strftime("%H:%M")
my_window=pyautogui.size()
width=my_window[0]
height=my_window[1]

headings=["Name","Description","Date Time"]
color="RED"
rem_data=sql.retrive()
rem_list=[]
for i in rem_data:
    j=list(i)
    rem_list.append(j)

print(rem_list)
show_column = [[sg.Text("                All Remainders",font="helvitica 35",text_color="red")],
    [sg.Table(headings=headings,values=rem_list,
                  expand_x=True,expand_y=True,hide_vertical_scroll=False,max_col_width=80,
                  key="-table-",num_rows=8,enable_events=True,display_row_numbers=True,
                  row_height=80,justification="center",sbar_width=20,size=(1000,750)),
                sg.Text("",font="helvitica 45")]]

data_column = [[sg.Text("            Remainder Entry",font="helvitica 35",text_color="red")],
               [sg.Text(" ",font="fds 35")],
               [sg.Text(" ",font="fds 25")],
               [sg.Text("Name          "),sg.Input(key="-name-")],
               [sg.Text("Description "),sg.Multiline(key="-desc-",size=(45,10))],
               [sg.Text("Date Time  "),sg.Input(key="-date-"),sg.CalendarButton("calender")]]
try:
    initial_email=sql.retrive_email()[0][0]
except:
    initial_email=" "

def d_to_time(datetime):
    t=datetime[-8:-3:1]
    return t
def pop_def(message):
    sg.set_options(font=("Courier New", 24))
    bg = '#add123'
    layout = [[sg.Text(message, background_color=bg, pad=(0, 0))]]
    win = sg.Window('title', layout, no_titlebar=True, keep_on_top=True,
        location=(1000, 200), transparent_color=bg, margins=(0, 0),
        return_keyboard_events=True)
    win.read(timeout=3000, close=True)
    return


layout = [
    [sg.Column(show_column,size=(1000,750)),
     sg.Column(data_column)],[sg.Text("Plz enter your email"),sg.Input(key="-email-"),sg.Button("CHANGE",key="-change-")],
    [sg.Text("Your email : "),sg.Text(f"{initial_email}",key="-show-email-"),sg.Button("Clear Email",key="-clear-email-")],
    [sg.Text("                      ",font="helvitica 70"),sg.Button("MODIFY",key="-modify-"),sg.Button("DELETE",key="-delete-"),
     sg.Button("INSERT",key="-set-"),sg.Button("CLEAR",key="-clear-")]
]

window = sg.Window("REMAINDER APP",layout,size=(1920,1080),finalize=True,font="helvitica 14",element_justification="l")
selected_row=None
h_ref=False
while True:
    event,values=window.read(timeout=10)
    my_obj=datetime.now()

    for i in rem_list:

        if my_obj.hour==int(d_to_time(i[2])[0:2])and my_obj.minute==int(d_to_time(i[2])[3:]) and str(date.today())==i[2][:10]:

            print("sending email ... ...")
            email_alert("ALERT!",f"{i[0]} : {i[1]}",initial_email)
            sg.popup("REMINDER ALERT", auto_close=True, auto_close_duration=2)
            sg.popup("EMAIL SENT ",auto_close=True,auto_close_duration=2)
            time.sleep(60)
            print("time done")


    if event=="" or event==sg.WIN_CLOSED:
        break
    if event=="-clear-":

        window["-name-"].update("")
        window["-desc-"].update("")
        window["-date-"].update("")

    if event=="-set-":
        rem_list.append([values["-name-"],values["-desc-"],values["-date-"]])
        sql.insert(values["-name-"],values["-desc-"],values["-date-"])
        window["-table-"].update(values=rem_list)
        window["-name-"].update("")
        window["-desc-"].update("")
        window["-date-"].update("")
    if event=="-table-":
        selected_row=values["-table-"][0]

    if event=="-delete-":
        try:
            sql.delete(rem_list[selected_row][0])
            rem_data = sql.retrive()
            rem_list = []
            for i in rem_data:
                j = list(i)
                rem_list.append(j)
            window["-table-"].update(values=rem_list)
        except:
            sg.popup("PLZ SELECT A ROW")
    if event=="-modify-":
        try:
            val=rem_list[selected_row]
            window["-name-"].update(val[0])
            window["-desc-"].update(val[1])
            window["-date-"].update(val[2])
            sql.delete(rem_list[selected_row][0])
            rem_data = sql.retrive()
            rem_list = []
            for i in rem_data:
                j = list(i)
                rem_list.append(j)
            window["-table-"].update(values=rem_list)
        except:
            sg.popup("PLZ SELECT A ROW")
    if event=="-change-":
        if values["-email-"]=="":
            sg.popup("ENTER THE EMAIL ",auto_close=True,auto_close_duration=5)

        else:
            sql.clear_email()
            sql.insert_email(values["-email-"])
            initial_email=values['-email-']
            window['-show-email-'].update(values["-email-"])
    if event=="-clear-email-":
        sql.clear_email()
        window['-show-email-'].update(" ")

window.close()
