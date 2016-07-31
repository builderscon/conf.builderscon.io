# coding:utf-8

months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
class ConferenceDate(object):
    def __init__(self, jsonval, lang='en'):
        self.date = jsonval.get('date')
        self.open = jsonval.get('open')
        self.close = jsonval.get('close')
        self.lang = lang

    def datestr(self):
        # We should use datetime, timezone and stuff, but..
        # just not now.
        l = self.date.split('-')
        if self.lang == 'ja':
            return '%s年%d月%d日'.decode('utf-8') % (l[0], int(l[1]), int(l[2]))

        # Silly, I know I know...
        return '%s %s %d' % (months[int(l[1])-1], l[2], int(l[0]))

    def __str__(self):
        return self.datestr()
