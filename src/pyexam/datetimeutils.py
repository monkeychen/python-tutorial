import time
import datetime
from dateutil import relativedelta

FMT_DEFAULT = "%Y-%m-%d %H:%M:%S"
FMT_Ymd = "%Y%m%d"
FMT_YmdHMS = "%Y%m%d%H%M%S"
FMT_HMS = "%H%M%S"


def str_to_time(time_str, fmt=FMT_DEFAULT):
    return time.strptime(time_str, fmt)


def str_to_datetime(dt_str, fmt=FMT_DEFAULT):
    return datetime.datetime.strptime(dt_str, fmt)


def time_to_str(tm, fmt=FMT_DEFAULT):
    return tm.strftime(fmt)


def datetime_to_str(dt, fmt=FMT_DEFAULT):
    return dt.strftime(fmt)


def time_to_timestamp(tm):
    return time.mktime(tm)


def timestamp_to_time(ts):
    return time.localtime(ts)


def datetime_to_timestamp(dt):
    return dt.timestamp()


def timestamp_to_datetime(ts):
    return datetime.datetime.fromtimestamp(ts)


def datetime_to_time(dt):
    return dt.timetuple()


def time_to_datetime(tm):
    return datetime.datetime(*tm[0:6])


def timestamp_to_str(ts, fmt=FMT_DEFAULT):
    return datetime_to_str(timestamp_to_datetime(ts), fmt)


def get_ago_date_id(date_id: str, ago: int, fmt=FMT_Ymd) -> str:
    ago_dt = str_to_datetime(date_id, fmt) - relativedelta.relativedelta(days=ago)
    return datetime_to_str(ago_dt, fmt)


def get_ahead_date_id(date_id: str, ahead: int, fmt=FMT_Ymd) -> str:
    ahead_dt = str_to_datetime(date_id, fmt) + relativedelta.relativedelta(days=ahead)
    return datetime_to_str(ahead_dt, fmt)

