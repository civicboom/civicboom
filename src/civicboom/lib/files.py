"""
File management utils for uploaded files
"""
import os
import shutil
from pylons import app_globals



def form_upload_file_relocate(form_temp_file, destination_path=app_globals.path['temp'], destination_filename=None):
    """
    Relocate a file from temp upload path to another path
    Reference: Definative Guide to Pylons - pg99
    """
    if not destination_filename:
        destination_filename = temp_file.filename
    
    permanent_file = open(
        os.path.join(
            destination_path,
            destination_filename.replace(os.sep, '_')
        ),
        'wb'
    )
    shutil.copyfileobj(form_temp_file.file, permanent_file)
    form_temp_file.file.close()
    permanent_file.close()
    return permanent_file.name

def append_filepart(destination_file, data):
    d = open(destination_file,"ab")
    d.write(data)
    d.close()