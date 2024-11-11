from django import template
import datetime
# from django.utils.timezone import make_aware
from django.utils import timezone
register = template.Library()


def print_timestamp(timestamp):
    try:
        #assume, that timestamp is given in seconds with decimal point
        # print(typeof(timestamp))
        ts = float(timestamp)/1000

    except ValueError:
        return None

    return datetime.datetime.fromtimestamp(ts)
    # return make_aware(datetime.datetime.utcfromtimestamp(ts).replace(tzinfo=get_current_timezone()))
register.filter(print_timestamp)
