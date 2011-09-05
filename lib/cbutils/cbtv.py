#!/usr/bin/python

# todo:
# click on an item to zoom to it
# - zoom in, but have a max zoom (having a 0ms event filling the screen
#   would be silly)
# full-file navigation
# - cbtv_events logs can last for hours, but only a minute at a time is
#   sensibly viewable
# close log after appending?
# - holding it open blocks other threads?
# - but it is opened at the start and should never be closed...

from __future__ import print_function
from decorator import decorator
import threading
from time import time
from optparse import OptionParser
import sqlite3
import sys


NAME = "Civicboom TV"
ROW_HEIGHT = 140
BLOCK_HEIGHT = 20


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


def log_bookmark(text):
    log_msg(text, "!")


def log_start(text):
    log_msg(text, "+")


def log_end(text):
    log_msg(text, "-")


def log(text, bookmark=False):
    @decorator
    def _log(function, *args, **kwargs):
        if callable(text):
            _text = text(function, args, kwargs)
        else:
            _text = text
        # _text = function.func_name+":"+_text
        try:
            if bookmark:
                log_bookmark(_text)
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
        CREATE TABLE IF NOT EXISTS cbtv_events(
            timestamp float not null,
            thread varchar(32) not null,
            type char(1) not null,
            text text not null
        )
    """)
    for line in open(log_file):
        c.execute(
            "INSERT INTO cbtv_events VALUES(?, ?, ?, ?)",
            line.strip().split(" ", 3)
        )
    c.close()
    db.commit()


def get_start(cursor, start_hint=1, io="+"):
    return list(cursor.execute(
        "SELECT min(timestamp) FROM cbtv_events WHERE timestamp > ? AND type = ?",
        [start_hint, io]
    ))[0][0]


def get_end(cursor, end_hint=0, io="-"):
    return list(cursor.execute(
        "SELECT max(timestamp) FROM cbtv_events WHERE timestamp < ? AND type = ?",
        [end_hint, io]
    ))[0][0]


#######################################################################
# GUI Out
#######################################################################

from Tkinter import *
from ttk import *


class App:
    def __control_box(self, master):
        f = Frame(master)

        def _la(t):
            Label(f,
                text=t
            ).pack(side="left")

        def _sp(f, t, i, v):
            Spinbox(f,
                from_=f, to=t, increment=i,
                textvariable=v
            ).pack(side="left")

        def _bu(t, c):
            Button(f,
                text=t, command=c
            ).pack(side="right")

        _la(f, "  Start ")
        _sp(f, 0, int(time()), 10, self.render_start)
        _la(f, "  Length ")
        _sp(f, 1, 60, 1, self.render_len)
        _la(f, "  Zoom ")
        _sp(f, 100, 5000, 100, self.scale)

        _bu("End", self.end_event)
        _bu("Next Bookmark", self.next_event)
        _bu("Prev Bookmark", self.prev_event)
        _bu("Start", self.start_event)

        f.pack()
        return f

    def __init__(self, master, database_file):
        self.master = master
        self.char_w = -1

        db = sqlite3.connect(database_file)
        self.c = db.cursor()

        self.threads = sorted(n[0] for n in self.c.execute("SELECT DISTINCT thread FROM cbtv_events"))
        self.render_start = DoubleVar(master, get_start(self.c, 0))
        self.render_len = IntVar(master, 30)
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
        self.controls.grid(column=0, row=0, sticky=(W, E))
        self.canvas.grid(  column=0, row=1, sticky=(N, W, E, S))
        self.v.grid(       column=1, row=1, sticky=(N, S))
        self.h.grid(       column=0, row=2, sticky=(W, E))
        self.grip.grid(    column=1, row=2, sticky=(S, E))

        self.canvas.bind("<4>", lambda e: self.scale_view(e, 1.0 * 1.1))
        self.canvas.bind("<5>", lambda e: self.scale_view(e, 1.0 / 1.1))

        # in windows, mouse wheel events always go to the root window o_O
        self.master.bind("<MouseWheel>", lambda e: self.scale_view(e,
            ((1.0 * 1.1) if e.delta < 0 else (1.0 / 1.1))
        ))

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

    def end_event(self):
        next_ts = get_end(self.c, sys.maxint, "!")
        if next_ts:
            self.render_start.set(next_ts)
        self.canvas.xview_moveto(0)

    def next_event(self):
        next_ts = get_start(self.c, self.render_start.get(), "!")
        if next_ts:
            self.render_start.set(next_ts)
        self.canvas.xview_moveto(0)

    def prev_event(self):
        prev_ts = get_end(self.c, self.render_start.get(), "!")
        if prev_ts:
            self.render_start.set(prev_ts)
        self.canvas.xview_moveto(0)

    def start_event(self):
        next_ts = get_start(self.c, 0, "!")
        if next_ts:
            self.render_start.set(next_ts)
        self.canvas.xview_moveto(0)

    def scale_view(self, e=None, n=1):
        # get the old pos
        if e:
            _xv = self.canvas.xview()
            left_edge = _xv[0]
            width = _xv[1] - _xv[0]
            width_fraction = float(e.x) / self.canvas.winfo_width()
            x_pos = left_edge + width * width_fraction
        # scale
        if n != 1:
            self.canvas.scale(ALL, 0, 0, n, 1)
            for t in self.canvas.find_withtag("event_tip"):
                self.canvas.itemconfigure(t, width=float(self.canvas.itemcget(t, 'width'))*n)  # this seems slow? sure something similar was faster...
            for t in self.canvas.find_withtag("event_label"):
                self.canvas.itemconfigure(t, width=float(self.canvas.itemcget(t, 'width'))*n)  # this seems slow? sure something similar was faster...
                w = int(self.canvas.itemcget(t, 'width'))
                tx = self.truncate_text(self.original_texts[t], w)
                self.canvas.itemconfigure(t, text=tx)  # this seems slow? sure something similar was faster...
            self.canvas.configure(scrollregion=self.canvas.bbox(ALL))
        # scroll the canvas so that the mouse still points to the same place
        if e:
            _xv = self.canvas.xview()
            new_width = _xv[1] - _xv[0]
            self.canvas.xview_moveto(x_pos - new_width * width_fraction)

    def truncate_text(self, text, w):
        return text[:w / self.char_w]

    def update(self, *args):
        """
        Data settings changed, get new data and re-render
        """
        s = self.render_start.get() - 1
        e = self.render_start.get() + self.render_len.get() + 1
        self.data = list(self.c.execute("SELECT * FROM cbtv_events WHERE timestamp BETWEEN ? AND ?", (s, e)))
        self.render()

    def render(self, *args):
        """
        Render settings changed, re-render with existing data
        """
        self.render_clear()
        self.render_base()
        self.render_data()

    def render_clear(self):
        """
        clear the canvas and any cached variables
        """
        self.canvas.delete(ALL)
        self.original_texts = {}
        self.canvas.configure(scrollregion=(
            0, 0,
            self.render_len.get() * self.scale.get(),
            len(self.threads)*ROW_HEIGHT+20
        ))
        if self.char_w == -1:
            t = self.canvas.create_text(0, 0, font="TkFixedFont", text="_", anchor=NW)
            bb = self.canvas.bbox(t)
            # [2]-[0]=10, but trying by hand, 8px looks better on win7
            # 7px looks right on linux, not sure what [2]-[0] is there,
            # hopefully 9px, so "-2" always helps?
            self.char_w = bb[2] - bb[0] - 2
            self.canvas.delete(t)

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
            label = " +%.3f" % (float(n) / _sc - _rl)
            self.canvas.create_line(n-rs_px, 0, n-rs_px, 20+len(self.threads)*ROW_HEIGHT, fill="#CCC")
            self.canvas.create_text(n-rs_px, 5, text=label, anchor="nw")

        for n in range(0, len(self.threads)):
            self.canvas.create_line(0, 20+ROW_HEIGHT*n, rl_px, 20+ROW_HEIGHT*n)
            self.canvas.create_text(0, 20+ROW_HEIGHT*n+5, text=" "+self.threads[n], anchor="nw")

    def render_data(self):
        """
        add the event rectangles
        """
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
            elif _io == "-":
                # if we start rendering mid-file, we may see the ends
                # of events that haven't started yet
                if len(thread_level_starts[thread_idx]):
                    event_start = thread_level_starts[thread_idx].pop()
                    event_end = _time
                    if event_start < _rs + _rl:
                        start_px  = (event_start - _rs) * _sc
                        end_px    = (event_end - _rs) * _sc
                        length_px = end_px - start_px
                        stack_len = len(thread_level_starts[thread_idx])
                        self.show(int(start_px), int(length_px), thread_idx, stack_len, _text)

            elif _io == "!":
                pass  # render bookmark

    def show(self, start, length, thread, level, text):
        text = " " + text
        _time_mult = float(self.scale.get()) / 1000.0
        tip = "%dms @%dms:\n%s" % (float(length) / _time_mult, float(start) / _time_mult, text)

        r = self.canvas.create_rectangle(
            start,        20+thread*ROW_HEIGHT+level*BLOCK_HEIGHT,
            start+length, 20+thread*ROW_HEIGHT+level*BLOCK_HEIGHT+BLOCK_HEIGHT,
            fill="#CFC", outline="#484",
        )
        t = self.canvas.create_text(
            start, 20+thread*ROW_HEIGHT+level*BLOCK_HEIGHT+3,
            text=self.truncate_text(text, length), tags="event_label", anchor="nw", width=length,
            font="TkFixedFont",
            state="disabled",
        )
        self.canvas.tag_raise(r)
        self.canvas.tag_raise(t)

        self.original_texts[t] = text

        r2 = self.canvas.create_rectangle(
            start,                  20+thread*ROW_HEIGHT+level*BLOCK_HEIGHT+BLOCK_HEIGHT+2,
            start+max(length, 200), 20+thread*ROW_HEIGHT+level*BLOCK_HEIGHT+BLOCK_HEIGHT*6+2,
            state="hidden", fill="white"
        )
        t2 = self.canvas.create_text(
            start+2, 20+thread*ROW_HEIGHT+level*BLOCK_HEIGHT+BLOCK_HEIGHT+2,
            text=tip, width=max(length, 200), tags="event_tip", anchor="nw",
            justify="left", state="hidden",
        )

        def ttip_show():
            self.canvas.itemconfigure(r2, state="disabled")
            self.canvas.itemconfigure(t2, state="disabled")
            self.canvas.tag_raise(r2)
            self.canvas.tag_raise(t2)

        def ttip_hide():
            self.canvas.itemconfigure(r2, state="hidden")
            self.canvas.itemconfigure(t2, state="hidden")

        def focus():
            # scale the canvas so that the (selected item width + padding == screen width)
            canvas_w = self.canvas.bbox(ALL)[2]
            view_w = self.canvas.winfo_width()
            rect_x = self.canvas.bbox(r)[0]
            rect_w = self.canvas.bbox(r)[2] - self.canvas.bbox(r)[0] + 20
            self.scale_view(n=float(view_w)/rect_w)

            # move the view so that the selected (item x1 = left edge of screen + padding)
            canvas_w = self.canvas.bbox(ALL)[2]
            rect_x = self.canvas.bbox(r)[0] - 5
            self.canvas.xview_moveto(float(rect_x)/canvas_w)

        self.canvas.tag_bind(r, "<Enter>", lambda e: ttip_show())
        self.canvas.tag_bind(r, "<Leave>", lambda e: ttip_hide())
        self.canvas.tag_bind(r, "<1>",     lambda e: focus())


def _center(root):
    w = 800
    h = 600
    ws = root.winfo_screenwidth()
    hs = root.winfo_screenheight()
    x = (ws/2) - (w/2)
    y = (hs/2) - (h/2)
    root.geometry('%dx%d+%d+%d' % (w, h, x, y))


def display(database_file):
    root = Tk()
    root.title(NAME)
    #root.state("zoomed")
    #_center(root)
    App(root, database_file)
    root.mainloop()
    return 0


def main(argv):
    parser = OptionParser()
    parser.add_option("-i", "--import", dest="log_file",
            help="import log file to database", metavar="LOG")
    parser.add_option("-d", "--database", dest="database", default="cbtv.db",
            help="database file to use", metavar="DB")
    (options, args) = parser.parse_args(argv)

    if options.log_file and options.database:
        compile_log(options.log_file, options.database)

    elif options.database:
        display(options.database)


if __name__ == "__main__":
    sys.exit(main(sys.argv))
