# An incomplete implementation of RFC3339 without support for timezones.
# Parses into standard datetime objects.

import datetime as dt
import re

re_date_str = r'(\d\d\d\d)-(\d\d)-(\d\d)'
re_time_str = r'(\d\d):(\d\d):(\d\d)(\.(\d+))?[zZ]'

def make_re(*parts):
    return re.compile(r'^\s*' + ''.join(parts) + r'\s*$')

re_datetime = make_re(re_date_str, r'[ tT]', re_time_str)

def parse_datetime(s):
    
    m = re_datetime.match(s)
    if m:
        y, m, d, hour, min, sec, i1, fsec = m.groups()

        if fsec:
            msec = int(float("0."+fsec) * 1000000)
        else:
            msec = 0
        return dt.datetime(int(y), int(m), int(d),
                            int(hour), int(min), int(sec), msec)


if __name__ == '__main__':
    print parse_datetime("2010-10-15T11:03:47.681Z")
