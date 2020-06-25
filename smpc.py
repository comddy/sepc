import requests
import json
import re
import json,re
from tkinter import *
from tkinter import messagebox
tokens = ""
vertify = 0
def login():
	global tokens,vertify
	user = "你的用户名"
	password = "你的密码"
	print('正在登陆中...请稍等！')
	url0='https://app.51xuexiaoyi.com/api/v1/login'
	data0 = {
	    "username":user,
	    "password":password
	         }
	headers0 = {
	    'platform':'android',
	    'app-version':'1.0.6',
	    'content-type':"application/json; charset=utf-8",
	    'accept-encoding':'gzip',
	    'user-agent':'okhttp/3.11.0'
	}
	denglu=requests.post(url0, headers=headers0,json=data0).text.encode('utf-8').decode('unicode_escape')
	if '登录成功' in denglu:
	    print("登录成功！")
	    vertify = 1
	    tokens=re.search(r'"api_token":"(.*)","userid"',denglu).group(1)
	else:
		messagebox.showwarning("警告","登录失败！")
def GetQues(ques):
	url = 'https://app.51xuexiaoyi.com/api/v1/searchQuestion'
	data = {
	    'keyword': ques
	}
	headers = {
	    'token': tokens,
	    'device': '',
	    'platform': 'android',
	    'User-Agent': 'okhttp/3.11.0',
	    'app-version': '1.0.6',

	    'Content-Type': "application/x-www-form-urlencoded; charset=UTF-8",
	    'Accept-Encoding': "gzip, deflate, br"
	}
	r = requests.post(url, headers=headers, data=data)

	html1_str = json.dumps(r.json(),sort_keys = True, indent = 4, separators = (',', ':'))
	str =html1_str.encode('utf-8').decode('unicode_escape')
	data = re.sub(r'"ey(.*)",',' ', str)
	res_answer = re.findall(r'"a":"(.*?)"',data,re.S)
	res_question = re.findall(r'"q":"(.*?)"',data,re.S)

	for i in range(len(res_question)):
		list_box.insert("end",res_question[i]+"\n\n")
		list_box.insert("end",res_answer[i]+"\n")
		list_box.insert("end","-------------------------------------------------------------------------------------\n")
r = Tk()
r.title("学小易PC版查题 --by小白")
r.geometry("750x650")
# r.resizable(False,True)
l = Label(r,text="请输入问题：").grid(row=0,column=0,ipadx=5,pady=20,sticky='w')
e = Entry(r,width=80)
e.grid(row=0,column=1,sticky='w')
def search():
	print(vertify)
	if vertify:
		list_box.delete(0.0,'end')
		question = e.get()
		if(len(question)<=5):
			messagebox.showwarning("警告","最少输入6个字")	
		else:
			GetQues(question)
login()
b1 = Button(r,text="查询",width=10,command=search).grid(row=0,column=2,sticky='w')
list_box = Text(r,fg="red",width=105,height=44)
scroll_bar = Scrollbar(r)
list_box.configure(yscrollcommand=scroll_bar.set)
scroll_bar['command'] = list_box.yview
list_box.grid(row=1,column=0,columnspan=3,padx=5)
r.mainloop()
