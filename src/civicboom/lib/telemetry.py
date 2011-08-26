from __future__ import print_function
from decorator import decorator
import threading
from time import time
import sys


_output = None


if __name__ != "__main__":
    if _output == None:
        _output = open("telemetry.log", "a", 1)


def set_log(fp):
    global _output
    _output = fp


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


def show(start, length, thread, level, text):
    print(
        "<div class='event' style='top: %(level)d; left: %(time)d; width: %(length)d;' title='%(length)sms @%(time)sms -- %(text)s'>%(text)s</div>" % {
            "level": thread*100+level*20,
            "time": start,
            "length": length,
            "text": text.replace("'", '"')
        }
    )


def main(argv):
    print("""<html>
    <head>
        <title>Civicboom Telemetry Viewer</title>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
        <style>
.event {
    position: absolute;
    overflow: hidden;
    background: #DFD;
    border: 1px solid #484;
    height: 19px; /* other box model would be handy... */
    font-size: 0.75em;
    text-align: center;
}
.thread {
    position: absolute;
    left: 0px;
    width: 100%;
    height: 99px;
    background: #EFE;
    border-bottom: 1px solid black;
    z-index: -1;
}
        </style>
    </head>
    <body>
    """)

    render_start = 0
    render_len = 5000
    resolution = 1000

    threads = []
    thread_level_starts = []
    # if we don't have a defined start and end, guess them
    if render_start == 0:
        render_start = float(open("telemetry.log").readline().strip().split(" ")[0])

    for line in open("telemetry.log"):
        (_time, _thread, _io, _text) = line.strip().split(" ", 3)
        _time = float(_time)

        # allocate a position to any new threads
        if _thread not in threads:
            threads.append(_thread)
            thread_level_starts.append([])
            print("<div class='thread' style='top: %dpx'></div>" % ((len(threads)-1)*100, ))
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
                    show(int(start_px), int(length_px), thread_idx, stack_len, _text)
    print("""
    </body>
</html>""")

if __name__ == "__main__":
    sys.exit(main(sys.argv))
