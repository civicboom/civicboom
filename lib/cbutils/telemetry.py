#!/usr/bin/python

from __future__ import print_function
from decorator import decorator
import threading
from time import time
from optparse import OptionParser
import sqlite3
import sys


ROW_HEIGHT=100
BLOCK_HEIGHT=14


#######################################################################
# Library API
#######################################################################

_output = None

def set_log(fn):
    global _output
    _output = open(fn, "a", 1)


def log_msg(text, io):
    tn = threading.current_thread().name.replace(" ", "-")
    if _output:
        print("%f %s %s %s" % (time(), tn, io, text), file=_output)


def log_start(text):
    log_msg(text, "+")


def log_end(text):
    log_msg(text, "-")


def log(text):
    @decorator
    def _log(function, *args, **kwargs):
        if callable(text):
            _text = text(function, args, kwargs)
        else:
            _text = text
        # _text = function.func_name+":"+_text
        try:
            log_start(_text)
            return function(*args, **kwargs)
        finally:
            log_end(_text)
    return _log


#######################################################################
# Application API
#######################################################################

def compile_log(log_file, database_file):
    db = sqlite3.connect(database_file)
    c = db.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS telemetry(
            timestamp int not null,
            thread varchar(32) not null,
            io char(1) not null,
            text text not null
        )
    """)
    for line in open("telemetry.log"):
        c.execute("INSERT INTO telemetry VALUES(?, ?, ?, ?)", line.strip().split(" ", 3))
    c.close()
    db.commit()


def render(database_file, html_file):
    db = sqlite3.connect(database_file)
    c = db.cursor()

    fp = open(html_file, "w")

    render_start = 0
    render_len = 5000
    resolution = 1000

    threads = []
    thread_level_starts = []
    # if we don't have a defined start and end, guess them
    if render_start == 0:
        render_start = float(open("telemetry.log").readline().strip().split(" ")[0])

    print_header(fp)
    for row in c.execute("SELECT * FROM telemetry WHERE timestamp BETWEEN ? AND ?", (render_start, render_start+render_len)):
        (_time, _thread, _io, _text) = row
        _time = float(_time)

        # allocate a position to any new threads
        if _thread not in threads:
            threads.append(_thread)
            thread_level_starts.append([])
            print("<div class='thread' style='top: %dpx'></div>" % (20+(len(threads)-1)*ROW_HEIGHT, ), file=fp)
        thread_idx = threads.index(_thread)

        # when an event starts, take note of the start time
        if _io == "+":
            thread_level_starts[thread_idx].append(_time)

        # when the event ends, render it
        else:
            # if we start rendering mid-file, we may see the ends of events that haven't started yet
            if len(thread_level_starts[thread_idx]):
                event_start = thread_level_starts[thread_idx].pop()
                event_end = _time
                #print("offset:%f start:%f end:%f" % (render_start, event_start-render_start, event_end-render_start))
                if event_start < render_start + render_len:
                    start_px  = (event_start-render_start) * resolution
                    end_px    = (event_end-render_start) * resolution
                    length_px = end_px - start_px
                    stack_len = len(thread_level_starts[thread_idx])
                    show(int(start_px), int(length_px), thread_idx, stack_len, _text, fp)
    print_footer(fp)


def main(argv):
    parser = OptionParser()
    parser.add_option("-c", "--compile", dest="log_file", default="telemetry.log",
            help="compile log file to database", metavar="FILE")
    parser.add_option("-d", "--database", dest="database", default="telemetry.db",
            help="database file to use", metavar="DIR")
    parser.add_option("-r", "--render", dest="output_file", default="telemetry.html",
            help="extract files")
    (options, args) = parser.parse_args(argv)

    if options.log_file and options.database:
        compile_log(options.log_file, options.database)

    if options.database and options.output_file:
        render(options.database, options.output_file)


def print_header(fp):
    print("""<html>
    <head>
        <title>Civicboom Telemetry Viewer</title>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
        <style>
.marker {
    position: absolute;
    border-left: 1px solid #CCC;
    height: 1000px;
    top: 0px;
    padding: 5px;
    font-size: 0.75em;
    z-index: -1;
}

.thread {
    position: absolute;
    left: 0px;
    width: 100%;
    height: """+str(ROW_HEIGHT-1)+"""px;
    background: #EFE;
    border-top: 1px solid black;
    border-bottom: 1px solid black;
    z-index: -2;
}
/*
.thread:nth-child(odd) {
    background: #DFD;
}
*/

.event {
    position: absolute;
    overflow: hidden;
    background: #CFC;
    border: 1px solid #484;
    height: """+str(BLOCK_HEIGHT-1)+"""px; /* other box model would be handy... */
    font-size: 0.65em;
    text-align: center;
}
        </style>
    </head>
    <body>
    """, file=fp)
    for n in range(0, 2000, 100):
        print(
            "<div class='marker' style='left: %dpx'>%dms</div>" % (n, n),
            file=fp
        )


def show(start, length, thread, level, text, fp):
    print(
        ("<div class='event' "+
        "style='top: %(level)d; left: %(time)d; width: %(length)d;' "+
        "title='%(length)sms @%(time)sms -- %(text)s'>%(text)s</div>") %
        {
            "level": 20+thread*ROW_HEIGHT+level*BLOCK_HEIGHT,
            "time": start,
            "length": length,
            "text": text.replace("'", '"')
        },
        file=fp
    )


def print_footer(fp):
    print("""    </body>\n</html>""", file=fp)


if __name__ == "__main__":
    sys.exit(main(sys.argv))
