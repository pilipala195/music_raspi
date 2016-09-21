#!/usr/bin/env python
# -*- coding: utf-8 -*-

from subprocess import *
from shlex import split
from time import sleep
from virtkey import *
import os

if __name__ == '__main__':
    # command = "mpg123 -C -@ music_list.txt"
    # args = split(command)
    # print args
    # p = Popen(args, stdin=PIPE, stdout=PIPE, stderr=STDOUT)
    # sleep(2)
    # # p.communicate(b'f')[0]
    # p.stdin.write('f')
    os.system("mpg123 -C -@ music_list.txt")
    sleep(2)
    os.write('f')