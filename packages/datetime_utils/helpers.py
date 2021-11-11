from datetime import datetime

XMLDT = "%Y-%m-%dT%H:%M:%SZ"
XMLDT_ms = "%Y-%m-%dT%H:%M:%S.%fZ"


def parse_datetime(str_time) -> datetime:
    return datetime.strptime(str_time, XMLDT)


def datetime_to_str(time):
    return time.strftime(XMLDT)


def datetime_to_str_ms(time):
    return time.strftime(XMLDT_ms)


def timestamp_ms_to_datetime(timestamp):
    return timestamp_s_to_datetime(int(int(timestamp) // 1000))


def timestamp_s_to_datetime(timestamp):
    return datetime.utcfromtimestamp(int(timestamp))


def datetime_to_timestamp(time):
    return int((time - datetime(1970, 1, 1)).total_seconds())


def datetime_to_timestamp_ms(time):
    diff = time - datetime(1970, 1, 1)
    return int(diff.total_seconds() * 1000)
