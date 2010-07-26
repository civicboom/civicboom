"""
File management utils for uploaded files
"""
#import os
#import shutil



def append_filepart(destination_file, data):
    d = open(destination_file,"ab")
    d.write(data)
    d.close()