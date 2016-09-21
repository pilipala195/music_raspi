#!/usr/bin/env python
# -*- coding: utf-8 -*-

from voice import *
from recoder import *
from subprocess import Popen
from time import sleep
import os, pty, sys
import re
import serial


now_music = 0

def i_volume():
	p = Popen(["amixer", "sset", "PCM", "80%"])


def d_volume():
	p = Popen(["amixer", "sset", "PCM", "40%"])


def openfile():
    f = open("./music/music_list.txt", "r")
    music_list = f.read().split('.mp3\n')
    f.close()

    for i in range(0, len(music_list)):
        music_list[i] = unicode(music_list[i], 'utf-8')
    return music_list


def check(music_list, music):
    for i in range(0, len(music_list)):
        if re.search(music, music_list[i]):
            return i

    return None


def save_file(now_music):
    fp = open("now_music.txt", 'w')
    fp.write(now_music.encode('utf-8'))
    fp.close()




if __name__ == '__main__':
    rec = recoder()
    wavname = 'voice.wav'
    cmd1 = u"播放"
    cmd2 = u"暂停"
    cmd3 = u"上一首"
    cmd4 = u"下一首"
    cmd5 = u"音量加"
    cmd6 = u"音量减"
    cmd7 = u"搜索"

    ser = serial.Serial("/dev/ttyAMA0", 115200)

    music_list = openfile()
    now_music = 0

    pid, fd = os.forkpty()
    if pid:
        while True:
            bufToRead = ser.inWaiting()
            buf = ser.read(bufToRead)
            leap = 0
            if re.search('e', buf):
            	leap = 1
            elif re.search('f', buf):
            	leap = 2
            elif re.search('b', buf):
            	leap = 3
            elif re.search('a', buf):
            	leap = 4
            elif re.search('d', buf):
            	leap = 5
            elif re.search('c', buf):
            	leap = 6

            if os.path.isfile('initial.wav'):
            	p = Popen(["sox", "initial.wav", "-r", "8000", "voice.wav"])
                if os.path.isfile('voice.wav'):
                    text = getResult()
                    p.terminate()
                    os.remove('voice.wav')
                    os.remove('initial.wav')
            else:
                text = u'呵'

            if os.path.isfile("cmd.txt"):
                fp = open("cmd.txt", 'r')
                text = fp.read()
                text = unicode(text, 'utf-8')
                fp.close()
                os.remove("cmd.txt")

            if leap or text:
                if re.search(cmd1, text) or re.search(cmd2, text) or leap == 1:
                    os.write(fd, 's')

                if leap == 2:
                    os.write(fd, 'q')

                if re.search(cmd3, text) or leap == 3:
                    os.write(fd, 'd')
                    if now_music:
                        now_music -= 1
                        save_file(now_music)

                if re.search(cmd4, text) or leap == 4:
                    os.write(fd, 'f')
                    if now_music < 7:
                        now_music += 1
                        save_file(now_music)

                if re.search(cmd6, text) or leap == 5:
                    d_volume()

                if re.search(cmd5, text) or leap == 6:
                    i_volume()

                if re.search(cmd7, text):
                    pos = re.search(cmd7, text).regs[0][1]
                    music = text[pos:-1]
                    num = check(music_list, music)
                    if not(num == None):
                        if num < now_music:
                            for i in range(num, now_music):
                                os.write(fd, 'd')
                                sleep(0.12)
                            now_music = num
                            save_file(now_music)
                        elif num > now_music:
                            for i in range(now_music, num):
                                os.write(fd, 'f')
                                sleep(0.12)
                            now_music = num
                            save_file(now_music)

    else:
        os.spawnl(os.P_WAIT, '/usr/bin/mpg123', '/usr/bin/mpg123', '-C', '-@', './music/music_list.txt') 


