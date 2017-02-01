# coding:utf-8

import iso8601
import pytz

MONTHS_EN = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
WDAYS_EN  = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
WDAYS_JA  = map(lambda n:n.decode('utf-8'), ['月', '火', '水', '木', '金', '土', '日'])

class ConferenceDate(object):
    def __init__(self, jsonval, lang='en', timezone='UTC'):
        localtz = pytz.timezone(timezone)
        self.open = iso8601.parse_date(jsonval.get('open')).astimezone(localtz)
        self.close = iso8601.parse_date(jsonval.get('close')).astimezone(localtz)
        self.lang = lang

    def date(self):
        if self.lang == 'ja':
            return '%d年%d月%d日(%s)'.decode('utf-8') % (self.open.year, self.open.month, self.open.day, WDAYS_JA[self.open.weekday()])
        else:
            return '%s %d, %d (%s)'.decode('utf-8') % (MONTHS_EN[self.open.month-1], self.open.day, self.open.year, WDAYS_EN[self.open.weekday()])

    def open_time(self):
        return '%02d:%02d' % (self.open.hour, self.open.minute)

    def close_time(self):
        return '%02d:%02d' % (self.close.hour, self.close.minute)

    def __str__(self):
        return self.date()
