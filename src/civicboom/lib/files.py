"""
File management utils for uploaded files
"""
import os
import shutil
from pylons import app_globals





def append_filepart(destination_file, data):
    d = open(destination_file,"ab")
    d.write(data)
    d.close()