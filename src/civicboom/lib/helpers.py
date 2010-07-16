"""Helper functions

Consists of functions to typically be used within templates, but also
available to Controllers. This module is available to templates as 'h'.
"""
# Import helpers as desired, or define your own, ie:
#from webhelpers.html.tags import checkbox, password

def priority_to_color(pri):
    """
    turn a priority number into a relevant colour for
    display in the even log
    """
    m = {
         0: "#0F0", # undefined, green
        10: "#999", # debug, grey
        20: "#000", # info, black
        30: "#800", # warning, dark red
        40: "#C00", # error, mid red
        50: "#F00", # critical, bright red
    }
    if pri in m:
        return m[pri]
    else:
        return "#00F" # nonstandard level, green
