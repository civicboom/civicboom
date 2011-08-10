import datetime

def next_start_date(start_date, frequency, time_now, offset=0):
    _start_date = start_date
    while _start_date < time_now.date():
        _start_date = start_date
        
        new_year  = time_now.year
        new_month = start_date.month
        
        if frequency == "year":
            new_year += offset    
        elif frequency == "month":
            new_month = time_now.month + offset
            while new_month > 12:
                new_year += 1
                new_month -= 12
            while new_month < 1:
                new_year -= 1
                new_month += 12
        
        try:
            _start_date = _start_date.replace(year=new_year, month=new_month)
        except ValueError as e:
            if e.message != 'day is out of range for month':
                raise e
            new_month += 1
            if new_month > 12:
                new_year += 1
                new_month -= 12
            _start_date = _start_date.replace(year=new_year, month=new_month, day=1)
        offset += 1
    return _start_date
