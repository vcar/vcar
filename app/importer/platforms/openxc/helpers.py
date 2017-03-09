from .constants import TRANSFORM

# -------------------- OpenXC Helpers --------------------------------------- #


def correct_value(value):
    try:
        return int(value)
    except:
        for k, v in TRANSFORM.items():
            if value == v:
                return k
        return -99999


def correct_time(timestamp):
    try:
        timestamp = str(timestamp)
        t = timestamp.split('.')
        return '{}{}'.format(t[0], t[1][:3].ljust(3, '0'))
    except:
        return timestamp.split('.')[0]
