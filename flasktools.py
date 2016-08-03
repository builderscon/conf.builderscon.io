import werkzeug.routing
import sys

if sys.version[0] == "3":
    from urllib.parse import urlencode
else:
    from urllib import urlencode

# Required to use regular expressions in the routing
class RegexConverter(werkzeug.routing.BaseConverter):
    def __init__(self, url_map, *items):
        super(RegexConverter, self).__init__(url_map)
        self.regex = items[0]



