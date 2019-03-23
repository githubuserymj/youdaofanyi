from tkinter import *
import urllib
import json
import urllib.parse
import urllib.request
from tkinter import filedialog
import random


#ua库
USER_AGENTS = [
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
    "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
    # "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
    # "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
    "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
    "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
    "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
    "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
]

header = random.choice(USER_AGENTS)

#翻译函数
def translate(word):
    url = 'http://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule&smartresult=ugc&sessionFrom=null'
    head = {}
    head['Referer'] = 'http://fanyi.youdao.com'
    head['User-Agent'] = header
    data = {}
    data['i'] = word
    data['doctype'] = 'json'
    data = urllib.parse.urlencode(data).encode('utf-8')
    rep = urllib.request.Request(url, data, head)  # Requsest有一个header参数，修改ua
    response = urllib.request.urlopen(rep)
    html = response.read().decode('utf-8')
    target = json.loads(html)
    result = ''
    for each_row in target['translateResult']:
        for each in each_row:
            result += each['tgt']
        result += '\n   '
    return result

def trans():
    text2.delete(1.0, END)
    old_words = text1.get(1.0, END)
    print('原文：' + '\n' + old_words)
    try:
        new_words = translate(old_words)
    except urllib.error.HTTPError:
        print("网络出错")
    text2.insert(INSERT, new_words)
    print('译文：' + '\n' + new_words)

def clear():
    text1.delete(1.0,END)
    text2.delete(1.0,END)

def open_file():
    file_path = filedialog.askopenfilename(title = '选择文本',filetypes = [("Text file", "*.txt*")])
    with open(file_path) as file:
        text1.insert(INSERT, file.read())

def save_file():
    untranslate_text = text1.get(1.0,END)
    translated_text = text2.get(1.0,END)
    file_path = filedialog.asksaveasfilename(title = '保存文本',filetypes = [("Text file", "*.txt*")])
    if untranslate_text != '' and translated_text != '':
        with open(file_path+'.txt','w') as file:
            file.write('原文：\n' +untranslate_text + '\n译文：\n' + translated_text)

def exit():
    root.quit()

def check_ua():
    top = Toplevel()
    top.title("UA库")
    ua_lists = ''
    for ua in USER_AGENTS:
        ua_lists += ua + '\n\n'
    msg = Message(top,text = ua_lists)
    msg.pack()

def check_ip():
    pass

root = Tk()
root.geometry('905x450+250+150')
root.resizable(width = False, height = False)
root.title("小鱼翻译")
root.iconbitmap("C:\\Users\\YMJ\Desktop\\实用软件\\tubiao.ico")

#创建菜单
menubar = Menu(root)

file_menu = Menu(menubar,tearoff = False)
file_menu.add_command(label = '打开',command = open_file)
file_menu.add_command(label = '保存',command = save_file)
file_menu.add_separator()
file_menu.add_command(label = '退出',command = exit)
menubar.add_cascade(label = '文件',menu = file_menu)

option_menu = Menu(menubar,tearoff = False)

ua_menu = Menu(menubar,tearoff = False)
ua_menu.add_command(label = 'UA库',command = check_ua)
option_menu.add_cascade(label = 'UA选项',menu = ua_menu)

ip_menu = Menu(menubar,tearoff = False)
ip_menu.add_command(label = 'IP搜索')
ip_menu.add_command(label = 'IP库',command = check_ip)
option_menu.add_cascade(label = 'IP选项',menu = ip_menu)

menubar.add_cascade(label = '功能',menu = option_menu)

frame1 = Frame(root,width = 130,height = 10)
frame2 = Frame(root,width = 60,height = 30)
frame3 = Frame(root,width = 20,height = 30)
frame4 = Frame(root,width = 60,height = 30)
frame5 = Frame(root,width = 130,height = 10)

#滑动条组件Scrollbar
scr1 = Scrollbar(frame2)
scr2 = Scrollbar(frame4)

titleLabel = Label(frame1,text = "有道翻译",font = ('宋体',25))
titleLabel.grid(row = 0,column = 1,sticky = W)

#组件Label
label1 = Label(frame2,text = '原文',font = ('宋体',15),compound = CENTER)
label2 = Label(frame4,text = '译文',font = ('宋体',15),compound = CENTER)

#组件Text
text1 = Text(frame2,width = 51,height = 20,yscrollcommand = scr1.set,font = ('宋体',12))
scr1.config(command = text1.yview)
text2 = Text(frame4,width = 51,height = 20,yscrollcommand = scr2.set,fg = 'blue',font = ('宋体',12))
scr2.config(command = text2.yview)

#Buuton组件
button1 = Button(frame3,text = '翻译',command = trans)
button2 = Button(frame3,text = '清除',command = clear)

#显示UA及IP的Lable组件
Label(frame5,text = 'IP:255.255.255.255:8888',font = ('宋体',7),justify = LEFT).grid(row = 3,pady = 1)
Label(frame5,text = 'UA:'+ header,font = ('宋体',7)).grid(row = 4,pady = 1)

#布局frame
frame1.grid(columnspan = 3)
frame2.grid(row = 1,column = 0)
frame3.grid(row = 1,column = 1)
frame4.grid(row = 1,column = 2)
frame5.grid(columnspan = 3)

#布局组件
label1.grid(row = 1,column = 0,sticky = N)
label2.grid(row = 1,column = 2,sticky = N)

#布局文本框
text1.grid(row = 2,column = 0,padx = 10)
text2.grid(row = 2,column = 2,padx = 10)

#布局Button
button1.grid(row = 2,column = 1,pady = 10)
button2.grid(row = 3,column = 1,pady = 10)

#布局Scrollbar
scr1.grid(row = 2,column = 0,sticky = N+S+E)
scr2.grid(row = 2,column = 2,sticky = N+S+E)

#显示菜单
root.config(menu = menubar)

mainloop()