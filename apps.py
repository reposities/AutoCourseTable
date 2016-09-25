#-*- coding: UTF-8 -*- 
#Author: fb.me/jhang.y.wei
#ez to create useful course timetable
#if have any question or bug,please pm author 
import requests
from BeautifulSoup import BeautifulSoup
import json
import getpass

account="d0xxXXXX"
password="XXXXXXXX"



login_url='https://apps.fcu.edu.tw/main/infologin.aspx'
class_url='https://apps.fcu.edu.tw/main/S3202/S3202_timetable_new.aspx/GetCurriculum'
timesetting ={'year': '105', 'smester': '1'}
header_info={
'Accept':'application/json, text/plain, */*',
'Content-Type':'application/json; charset=UTF-8',
}
postdata={}
output={}
#create a new session
s=requests.session()
first=s.get(login_url)
login_page = BeautifulSoup(first.text)
#do get necessary postdata
for element in login_page.findAll('input',{'value': True}):
    postdata[str(element['name'])]=str(element['value'])
del postdata['CancelButton']
postdata['txtUserName']=account
postdata['txtPassword']=password
login_html=s.post(login_url,data=postdata)
login_info = BeautifulSoup(login_html.text)
try:
    #if login fail can print where is wrong
    error=login_info.findAll('span',{'id':'FailureText'})[0]
    error=str(error)[23:len(error)-8]
except:
    #to get course json data
    class_json=s.post(class_url,data=json.dumps(timesetting),headers=header_info)
    class_data=json.loads(class_json.text)
    for each_day in class_data['d']['list']:
        print each_day['week']
        for each_class in each_day['courses']:
            print each_class['course_id']
            #get the course secret key
            secret_key='https://apps.fcu.edu.tw/main/S3202/redirect.aspx?mode=21&code='+str(each_class['course_id'])
            get_secret_date=s.get(secret_key)
            secret_data = BeautifulSoup(get_secret_date.text)

            #use secret key to get more detail like teacher course type
            course_id=str(secret_data.findAll('script',{'type':'text/javascript'})[0]).split('window.sessionStorage.setItem')[1]
            course_id=course_id[15:len(course_id)-5]
            classid={"course_id":""}
            classid['course_id']=course_id

            #course type
            get_class_type=s.post('https://service120-sds.fcu.edu.tw/W3212/action/getdata.aspx/getCourseInfor1',data=json.dumps(classid),headers=header_info)
            class_type= get_class_type.text.split('\"')[14][0:2]
            #teacher name
            get_teacher_name=s.post('https://service120-sds.fcu.edu.tw/W3212/action/getdata.aspx/getCourseInfor2',data=json.dumps(classid),headers=header_info)
            #use 'try catch' to avoid the teacher name is null
            try:
                teacher_name= get_teacher_name.text.split('\"')[6][0:3]
            except:
                print("teacher not found")
                teacher_name="null"
            name=str(each_day['week'])+'-'+str(each_class["period"])
            code='('+each_class['selcode']+')'
            output[name]={}
            output[name]["name"]=code+each_class["title"]
            output[name]["classroom"]=each_class["roomname"]
            output[name]["teacher"]=teacher_name
            if class_type ==u'選修':
                output[name]['status']=0
            else:
                output[name]['status']=1
    #write to a json file for web page
    with open("js/class_info.json", "w") as outfile:
         json.dump(output, outfile, sort_keys = True, indent = 4)
    print 'success'
else:
    print error
