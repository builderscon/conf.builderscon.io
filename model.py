# coding:utf-8

import iso8601
import pytz

months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
class ConferenceDate(object):
    def __init__(self, jsonval, lang='en', timezone='UTC'):
        print(lang)
        localtz = pytz.timezone(timezone)
        self.open = iso8601.parse_date(jsonval.get('open')).astimezone(localtz)
        self.close = iso8601.parse_date(jsonval.get('close')).astimezone(localtz)
        self.lang = lang

    def date(self):
        return '%d年%d月%d日'.decode('utf-8') % (self.open.year, self.open.month, self.open.day)

    def open_time(self):
        return '%02d:%02d' % (self.open.hour, self.open.minute)

    def close_time(self):
        return '%02d:%02d' % (self.close.hour, self.close.minute)

    def __str__(self):
        return self.date()
