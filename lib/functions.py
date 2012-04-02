__author__ = 'swasher'

def safe_int(val):
    try:
        return int(val)
    except (TypeError, ValueError):
        return 0
