import datetime, copy

#===============================================================================
# Takes year, month, day and turns them into a normalized date
#  e.g. 2000,2,29 returns 29/02/2000 and 2001,2,29 returns 01/03/2001
#===============================================================================
def normalize_date(year, month, day):
    while month > 12:
        year += 1
        month -= 12
    while month < 1:
        year -= 1
        month += 12
    try:
        date = datetime.date(year=year, month=month, day=day)
    except ValueError as e:
        if e.message != 'day is out of range for month':
            raise e
        month += 1
        if month > 12:
            year += 1
            month -= 12
        date = datetime.date(year=year, month=month, day=1)
    return date

#===============================================================================
# Calculates the next available start date (including today)
# >>> calculate_start_date(
#         datetime.date(year=2011,month=6,day=16),
#         'month',
#         datetime.datetime(year=2011,month=8,day=16)
#     )
# datetime.date(2011, 8, 16)
# >>> calculate_start_date(
#         datetime.date(year=2011,month=7,day=31),
#         'month',
#         datetime.datetime(year=2011,month=9,day=1)
#     )
# datetime.date(2011, 9, 1) # Should have been 31/08 but does not exist so rolls over to 01/09
#===============================================================================
def calculate_start_date(start_date, frequency, time_now, offset=0):
    p_day = start_date.day
    p_mon = start_date.month
    p_year = time_now.year
    if frequency == 'month':
        p_mon = time_now.month
    if time_now.day == 1:
        p_mon -= 1
    while True:
        if normalize_date(p_year, p_mon, p_day) >= time_now.date():
            break
        if frequency == 'year':
            p_year += 1
        elif frequency == 'month':
            p_mon += 1
    if offset:
        if frequency == 'year':
            p_year += offset
        elif frequency == 'month':
            p_mon += offset
            print 'p_mon', p_mon
    return normalize_date(p_year, p_mon, p_day)

def next_start_date(start_date, frequency, time_now):
    _start_date = calculate_start_date(start_date, frequency, time_now)
    if _start_date == time_now.date():
        _start_date = calculate_start_date(start_date, frequency, time_now, 1)
    return _start_date

def previous_start_date(start_date, frequency, time_now):
    _start_date = calculate_start_date(start_date, frequency, time_now, -1)
    if _start_date == time_now.date():
        _start_date = calculate_start_date(start_date, frequency, time_now, -2)
    return _start_date
    