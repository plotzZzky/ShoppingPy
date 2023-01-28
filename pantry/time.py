import datetime


def last_day_date(date, validate):
    day = datetime.datetime.strptime(date, '%Y-%m-%d').date()
    last_day = day + datetime.timedelta(validate)
    return last_day


def today_date():
    today = datetime.date.today()
    return today


def format_date(date):
    result = datetime.datetime.strptime(date, '%Y-%m-%d').date()
    return result