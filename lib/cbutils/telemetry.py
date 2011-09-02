#!/usr/bin/python

# todo:
# click on an item to zoom to it
# - have it centered on screen
# - zoom in, but have a max zoom (having a 0ms event filling the screen would be silly)
# full-file navigation
# - telemetry logs can last for hours, but only a minute at a time is sensibly viewable
# close log after appending?
# - holding it open blocks other threads?
# - but it is opened at the start and should never be closed...
# label as image?
# - hopefully images are cropped on bbox change, not scaled?

from __future__ import print_function
from decorator import decorator
import threading
from time import time
from optparse import OptionParser
import sqlite3
import sys


ROW_HEIGHT=140
BLOCK_HEIGHT=20


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
            timestamp float not null,
            thread varchar(32) not null,
            io char(1) not null,
            text text not null
        )
    """)
    for line in open(log_file):
        c.execute("INSERT INTO telemetry VALUES(?, ?, ?, ?)", line.strip().split(" ", 3))
    c.close()
    db.commit()

def get_start(cursor, start_hint=1):
    return list(cursor.execute("SELECT min(timestamp) FROM telemetry WHERE timestamp > ?", [start_hint]))[0][0]

def get_end(cursor, end_hint=0):
    return list(cursor.execute("SELECT max(timestamp) FROM telemetry WHERE timestamp < ?", [end_hint]))[0][0]


#######################################################################
# HTML Out
#######################################################################

def render(database_file, html_file):
    db = sqlite3.connect(database_file)
    c = db.cursor()

    fp = open(html_file, "w")

    render_start = get_start(c, 0)
    render_len = get_end(c, 9999999999) - render_start
    resolution = 1000

    threads = []
    thread_level_starts = []

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


#######################################################################
# GUI Out
#######################################################################

from Tkinter import *
from ttk import *

class App:
    def __control_box(self, master):
        f = Frame(master)

        Label(f, text="  Start ").pack(side="left")
        Spinbox(f, from_=0, to=int(time()), increment=0.1, textvariable=self.render_start).pack(side="left")
        Label(f, text="  Length ").pack(side="left")
        Spinbox(f, from_=0, to=60*1000,     increment=1,   textvariable=self.render_len).pack(side="left")
        Label(f, text="  Zoom ").pack(side="left")
        Spinbox(f, from_=100, to=5000,      increment=100, textvariable=self.scale).pack(side="left")
        #Button(f, text="Render", command=self.render).pack(side="right")

        f.pack()
        return f

    def __init__(self, master, database_file):
        db = sqlite3.connect(database_file)
        self.c = db.cursor()

        self.threads = sorted(n[0] for n in self.c.execute("SELECT DISTINCT thread FROM telemetry"))
        self.render_start = DoubleVar(master, get_start(self.c, 0))
        self.render_len = IntVar(master, 5)
        self.scale = IntVar(master, 1000)

        self.render_start.trace_variable("w", self.update)
        self.render_len.trace_variable("w", self.update)
        self.scale.trace_variable("w", self.render)

        self.h = Scrollbar(master, orient=HORIZONTAL)
        self.v = Scrollbar(master, orient=VERTICAL)
        self.canvas = Canvas(
            master,
            width=800, height=600,
            background="white",
            xscrollcommand=self.h.set,
            yscrollcommand=self.v.set,
        )
        self.h['command'] = self.canvas.xview
        self.v['command'] = self.canvas.yview

        self.controls = self.__control_box(master)
        self.grip = Sizegrip(master)

        master.grid_columnconfigure(0, weight=1)
        master.grid_rowconfigure(1, weight=1)
        self.controls.grid(column=0, row=0, sticky=(W,E))
        self.canvas.grid(  column=0, row=1, sticky=(N, W, E, S))
        self.v.grid(       column=1, row=1, sticky=(N,S))
        self.h.grid(       column=0, row=2, sticky=(W,E))
        self.grip.grid(    column=1, row=2, sticky=(S,E))

        hard_scale = """
        def _modify_scale(e, n):
            old = self.scale.get()
            new = max(old + n, 100)
            if old != new:
                # figure out where the mouse was pointing (in terms of scrollbar position)
                # eg the middle of the screen will be pointing to "the beginning of the scrollbar block plus half the width of the block"
                _xv = self.canvas.xview()
                left_edge = _xv[0]
                width = (_xv[1]-_xv[0])
                width_fraction = float(e.x)/self.canvas.winfo_width()
                x_pos = left_edge + width * width_fraction
                # scale the display
                self.scale.set(new)
                self.render()
                # scroll the canvas so that the mouse still points to the same place
                _xv = self.canvas.xview()
                new_width = (_xv[1]-_xv[0])
                self.canvas.xview_moveto(x_pos - new_width*width_fraction)

        self.canvas.bind("<4>", lambda e: _modify_scale(e, +100))
        self.canvas.bind("<5>", lambda e: _modify_scale(e, -100))
        """

        def _scale(e, n):
            # get the old pos
            _xv = self.canvas.xview()
            left_edge = _xv[0]
            width = (_xv[1]-_xv[0])
            width_fraction = float(e.x)/self.canvas.winfo_width()
            x_pos = left_edge + width * width_fraction
            # scale
            self.canvas.scale(ALL, 0, 0, n, 1)
            self.canvas.configure(scrollregion=self.canvas.bbox(ALL))
            # scroll the canvas so that the mouse still points to the same place
            _xv = self.canvas.xview()
            new_width = (_xv[1]-_xv[0])
            self.canvas.xview_moveto(x_pos - new_width*width_fraction)

        self.canvas.bind("<4>", lambda e: _scale(e, 1.0*1.1))
        self.canvas.bind("<5>", lambda e: _scale(e, 1.0/1.1))

        drag_move = """
        def _sm(e):
            self.st = self.render_start.get()
            self.sx = e.x
            self.sy = e.y
        def _cm(e):
            self.render_start.set(self.st + float(self.sx - e.x)/self.scale.get())
            self.render()
        self.canvas.bind("<1>", _sm)
        self.canvas.bind("<B1-Motion>", _cm)
        """

        self.update()

    def update(self, *args):
        """
        Data settings changed, get new data and re-render
        """
        s = self.render_start.get()-1
        e = self.render_start.get()+self.render_len.get()+1
        self.data = list(self.c.execute("SELECT * FROM telemetry WHERE timestamp BETWEEN ? AND ?", (s, e)))
        self.render()

    def render(self, *args):
        """
        Render settings changed, re-render with existing data
        """
        self.render_clear()
        self.render_base()
        self.render_data()

    def render_clear(self):
        self.canvas.delete(ALL)
        self.canvas.configure(scrollregion=(
            0, 0,
            self.render_len.get()*self.scale.get(),
            len(self.threads)*ROW_HEIGHT+20
        ))

    def render_base(self):
        """
        Render grid lines and markers
        """
        _rs = self.render_start.get()
        _rl = self.render_len.get()
        _sc = self.scale.get()

        rs_px = int(_rl * _sc)
        rl_px = int(_rl * _sc)

        for n in range(rs_px, rs_px+rl_px, 100):
            label = "+%.3f" % (float(n)/_sc-_rl)
            self.canvas.create_line(n-rs_px, 0, n-rs_px, 20+len(self.threads)*ROW_HEIGHT, fill="#CCC")
            self.canvas.create_text(n-rs_px+5, 5, text=label, anchor="nw")

        for n in range(0, len(self.threads)):
            self.canvas.create_line(0, 20+ROW_HEIGHT*n, rl_px, 20+ROW_HEIGHT*n)
            self.canvas.create_text(5, 20+ROW_HEIGHT*n+5, text=self.threads[n], anchor="nw")

    def render_data(self):
        _rs = self.render_start.get()
        _rl = self.render_len.get()
        _sc = self.scale.get()

        threads = self.threads
        thread_level_starts = [[], ] * len(self.threads)

        for row in self.data:
            (_time, _thread, _io, _text) = row
            _time = float(_time)
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
                    #print("offset:%f start:%f end:%f" % (self.render_start, event_start-self.render_start, event_end-self.render_start))
                    if event_start < _rs + _rl:
                        start_px  = (event_start-_rs) * _sc
                        end_px    = (event_end-_rs) * _sc
                        length_px = end_px - start_px
                        stack_len = len(thread_level_starts[thread_idx])
                        self.show(int(start_px), int(length_px), thread_idx, stack_len, _text)

    def show(self, start, length, thread, level, text):
        tip = "%dms @%dms:\n%s" % (float(length)/self.scale.get()*1000, float(start)/self.scale.get()*1000, text)

        r = self.canvas.create_rectangle(
            start,        20+thread*ROW_HEIGHT+level*BLOCK_HEIGHT,
            start+length, 20+thread*ROW_HEIGHT+level*BLOCK_HEIGHT+BLOCK_HEIGHT,
            fill="#CFC", outline="#484",
        )
        t = self.canvas.create_text(
            start+3, 20+thread*ROW_HEIGHT+level*BLOCK_HEIGHT+3,
            text=text, tags="event_label", anchor="nw",
            state="disabled",
        )
        self.canvas.tag_raise(r)
        self.canvas.tag_raise(t)

        r2 = self.canvas.create_rectangle(
            start,                  20+thread*ROW_HEIGHT+level*BLOCK_HEIGHT+BLOCK_HEIGHT+2,
            start+max(length, 200), 20+thread*ROW_HEIGHT+level*BLOCK_HEIGHT+BLOCK_HEIGHT*6+2,
            state="hidden",
            fill="white")
        t2 = self.canvas.create_text(
            start+2, 20+thread*ROW_HEIGHT+level*BLOCK_HEIGHT+BLOCK_HEIGHT+2,
            text=tip, width=max(length, 200), tags="event_label", anchor="nw", justify="left",
            state="hidden"
        )

        def ttip_show():
            self.canvas.itemconfigure(r2, state="disabled")
            self.canvas.itemconfigure(t2, state="disabled")
            self.canvas.tag_raise(r2)
            self.canvas.tag_raise(t2)
        def ttip_hide():
            self.canvas.itemconfigure(r2, state="hidden")
            self.canvas.itemconfigure(t2, state="hidden")

        #self.canvas.tag_bind(t, "<Enter>", lambda e: ttip_show())
        self.canvas.tag_bind(r, "<Enter>", lambda e: ttip_show())
        #self.canvas.tag_bind(t, "<Leave>", lambda e: ttip_hide())
        self.canvas.tag_bind(r, "<Leave>", lambda e: ttip_hide())
        #self.canvas.tag_bind(t, "<Enter>", lambda e: self.update_tip(tip))
        #self.canvas.tag_bind(r, "<Leave>", lambda e: self.update_tip("Hover over an item to see the full name"))


def _center(root):
    w=800
    h=600
    ws = root.winfo_screenwidth()
    hs = root.winfo_screenheight()
    x = (ws/2) - (w/2)
    y = (hs/2) - (h/2)
    root.geometry('%dx%d+%d+%d' % (w, h, x, y))


def display(database_file):
    root = Tk()
    root.title("Civicboom Telemetry Viewer")
    #root.state("zoomed")
    #_center(root)
    App(root, database_file)
    root.mainloop()
    return 0


def main(argv):
    parser = OptionParser()
    parser.add_option("-c", "--compile", dest="log_file", default="telemetry.log",
            help="compile log file to database", metavar="FILE")
    parser.add_option("-d", "--database", dest="database", default="telemetry.db",
            help="database file to use", metavar="DB")
    parser.add_option("-r", "--render", dest="output_file", default="telemetry.html",
            help="render the database contents to a web page")
    parser.add_option("-g", "--gui", action="store_true", default=False,
            help="display a GUI")
    (options, args) = parser.parse_args(argv)

    if options.gui and options.database:
        display(options.database)
        return 0

    if options.log_file and options.database:
        compile_log(options.log_file, options.database)

    if options.database and options.output_file:
        render(options.database, options.output_file)


if __name__ == "__main__":
    sys.exit(main(sys.argv))
