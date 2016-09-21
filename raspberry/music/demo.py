#!/usr/bin/env python
# -*- coding: utf-8 -*-

f = open("./music_list.txt", "r")
con = f.read()
# con = con.lstrip('./')
music_list = con.split('.mp3\n')
music_list.pop()
f.close()
for i in range(0, len(music_list)):
    music_list[i] = unicode(music_list[i], 'utf-8')
    music_list[i] = music_list[i].lstrip('./')
music_list[0], music_list[7] = music_list[7], music_list[0]
for i in range(0, len(music_list)):
    music_list[i] = music_list[i].encode('utf-8')
content = '\n'
content = content.join(music_list)

f = open("./music_list.txt", "w")
f.write(content)
f.close()
print music_list