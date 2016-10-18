import werkzeug.routing
import sys

if sys.version[0] == "3":
    import urllib.parse
    urlencode = urllib.parse.urlencode
    quote = urllib.parse.quote
    quote_plus = urllib.parse.quote_plus
else:
    import urllib
    urlencode = urllib.urlencode
    quote = urllib.quote
    quote_plus = urllib.quote_plus

# Required to use regular expressions in the routing
class RegexConverter(werkzeug.routing.BaseConverter):
    def __init__(self, url_map, *items):
        super(RegexConverter, self).__init__(url_map)
        self.regex = items[0]



