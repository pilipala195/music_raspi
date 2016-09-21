# -*- coding: utf-8 -*-  
import re
from flask import Flask, jsonify, render_template, request
  
app = Flask(__name__) 

cmd = 0
flag = 0
lastone = 1
t = 0

fr = open("music_list.txt", "r")  
names = {}
i = 0

while True:
    line = fr.readline()  
    if line:  
        i = i + 1
        name = line.lstrip('./')
        corname = unicode(name,"utf-8")
        names[corname] = i
    else:  
        break
fr.close()

@app.route("/")  
def index():  
    fr = open("now_music.txt","r")
    num = int(fr.readline())
    getindex = num
    print num
    print type(num)
    fr.close()
    
    templateData = {
        'getindex' : getindex
        }

    return render_template("index.html", **templateData)  
  

@app.route("/<change>")
def change(change):
    global lastone
    global t

    getname = change[:-4]
    print getname
    cmd = u'搜索' + getname
    for name in names:
       if re.search(getname,name) :
           print "hello"
           #print names[name]
           if (names[name] == (lastone+1)) or ((names[name]+8) == (lastone+1)):
           	cmd = u'下一首'
           if (names[name] == (lastone-1)) or ((names[name]-8) == (lastone-1)):
           	cmd = u'上一首'
           if names[name] == lastone:
               if t == 0:
                   cmd = u'停止'
                   t = 1
               else:
                   cmd = u'播放'
                   t = 0
           else:
               t = 0
           lastone = names[name]
    if cmd != 0:
        fw = open("cmd.txt","w")   
        fw.write(cmd.encode('utf-8'))
        fw.close()
    print

    return render_template("index.html")
     
if __name__=="__main__":  
    app.run(host="0.0.0.0", port=1024, debug=True)
