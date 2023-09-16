'''
Name: Li Xing Liu
Netid: lixiliu
Student Id: 113318331

Name: Andy You
Netid: Andyou
Student Id: 113494190
'''

import sys

def decaf_checker():
    # f = open(sys.argv[1], "r")
    f = open("./hello_world.decaf", "r")
    lines = f.readlines()
    print(lines)

decaf_checker()