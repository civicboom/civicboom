#!/usr/bin/env python

import sys
import re

# try and read dependencies from setup.py
# this is full of magic because grep sucks at handling newline characters
# the aim is to input setup.py, and output eg --> "Mako>=0.3.4" "gp.fileupload" "GeoFormAlchemy"
if sys.argv[1] == "find_packages":
    setup_data = file('../src/setup.py').read()
    requires   = re.match('.*install_requires=\[([^]]*)\].*', setup_data, re.DOTALL).group(1)
    print re.sub('[ \n]', '', requires).replace(',', ' ')


if sys.argv[1] == "list_all_css" or sys.argv[1] == "list_local_css":
    header_data = file('../src/civicboom/templates/web/html_header.mako').read()
    styles      = re.findall('/styles/.*\.css', header_data)
    for style in styles:
        if "_combined" not in style:
            print "../src/civicboom/public" + style

if sys.argv[1] == "list_all_css" or sys.argv[1] == "list_remote_css":
    header_data = file('../src/civicboom/templates/web/html_header.mako').read()
    styles      = re.findall('http://.*\.css', header_data)
    for style in styles:
        print style


if sys.argv[1] == "list_all_js" or sys.argv[1] == "list_local_js":
    header_data = file('../src/civicboom/templates/web/html_header.mako').read()
    scripts      = re.findall('/javascript/.*\.js', header_data)
    for script in scripts:
        if "_combined" not in script:
            print "../src/civicboom/public" + script

if sys.argv[1] == "list_all_js" or sys.argv[1] == "list_remote_js":
    header_data = file('../src/civicboom/templates/web/html_header.mako').read()
    scripts      = re.findall('http://.*\.js', header_data)
    for script in scripts:
        print script

