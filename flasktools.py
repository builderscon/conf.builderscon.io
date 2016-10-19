import werkzeug.routing
import sys

if sys.version[0] == "3":
    import urllib.parse
    urlencode = urllib.parse.urlencode
    urlparse = urllib.parse.urlparse
    urlunparse = urllib.parse.urlunparse
    quote = urllib.parse.quote
    quote_plus = urllib.parse.quote_plus
    parse_qsl = urllib.parse.parse_qsl
else:
    import urllib
    import urlparse as _urlparse
    urlencode = urllib.urlencode
    urlparse = _urlparse.urlparse
    urlunparse = _urlparse.urlunparse
    quote = urllib.quote
    quote_plus = urllib.quote_plus
    parse_qsl = _urlparse.parse_qsl

# Required to use regular expressions in the routing
class RegexConverter(werkzeug.routing.BaseConverter):
    def __init__(self, url_map, *items):
        super(RegexConverter, self).__init__(url_map)
        self.regex = items[0]



