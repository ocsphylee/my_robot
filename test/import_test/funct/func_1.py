# coding = utf-8
# /usr/bin/env/ python

'''
Author:Ocsphy
Date:2020/2/1 16:43
'''

import sys
sys.path.append('../')

from mod import mod_1


def print_func():
    mod = mod_1.print_mod()
    print('successfully import mod')

print_func()