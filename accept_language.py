if sys.version[0] == 3:
    from http.cookies import SimpleCookie
else:
    from Cookie import SimpleCookie

import re
import locale
from datetime import datetime, timedelta
from urlparse import urlparse, parse_qs

__all__ = ["LangDetector"]


DEFAULT_LANGS = "en",
COOKIE_NAME = "lang"
COOKIE_FORMAT = "%a, %d-%b-%Y %H:%M:%S UTC"
COOKIE_EXPIRATION = 30 # days


class LangDetector(object):
    """WSGI Middleware that deals with language support for you
    you only have to use environ["lang"] to read/set it
    """

    SEP = re.compile(", *")

    def __init__(self, application, languages=None, with_cookie=True):
        self.application = application
        if languages is not None:
            self.languages = languages
        else:
            self.languages = DEFAULT_LANGS
        self.with_cookie = with_cookie

    @property
    def default_language(self):
        return self.languages[0]

    def in_languages(self, lang):
        return lang in self.languages

    def language_from_cookie(self, cookie):
        if not cookie:
            return None

        tmp = cookie[COOKIE_NAME].value
        if self.in_languages(tmp):
            return  tmp

        return None

    def preferred_language(self, accept):
        preferred = None
        if accept:
            langs = {}
            l = self.SEP.split(accept)
            for lang in l:
                lang = lang.strip()
                hasq = lang.find(";q=")

                q = 1.
                if hasq > -1:
                    code = lang[:hasq]
                    q = float(lang[hasq+4:])
                else:
                    code = lang

                # ignore region
                if len(code) > 2:
                    code = code[:2]

                langs[code] = q

            score = 0
            for lang in self.languages:
                # ignore region
                l = lang[:2]
                if l in langs and langs[l] > score:
                    score = langs[l]
                    preferred = l

        return preferred

    def cookie_header(self, lang):
        expiration = datetime.utcnow() + timedelta(days=COOKIE_EXPIRATION)

        # Prevent non-english output
        current_locale = locale.getlocale(locale.LC_TIME)
        locale.setlocale(locale.LC_TIME, "en_US.UTF-8")

        expires = expiration.strftime(COOKIE_FORMAT)

        locale.setlocale(locale.LC_TIME, current_locale)

        return ('Set-Cookie',
                '%s="%s"; expires=%s; path=/' %
                    (COOKIE_NAME,
                     lang,
                     expires))

    def __detect__(self, environ):
        parsed = parse_qs(environ.get("QUERY_STRING"))
        lang = parsed.get("lang")
        if lang is not None and self.in_languages(lang[0]):
            return lang[0]

        if self.with_cookie:
            lang = self.language_from_cookie(SimpleCookie().load(environ.get("HTTP_COOKIE")))
            if lang:
                return lang

        lang = self.preferred_language(environ.get("HTTP_ACCEPT_LANGUAGE"))
        if lang:
            return lang

        return self.default_language

    def __call__(self, environ, start_response):
        lang = self.__detect__(environ)

        def _start_response(status, response_headers, exc_info=None):
            # Removing any existing content-language
            response_headers = [(name, value)
                                for name, value in response_headers
                                    if name.lower() != 'content-language']

            # lang changed
            lang = environ['lang.origin']
            if lang != environ['lang']:
                if environ['lang'] not in self.languages:
                    environ['lang'] = lang
                else:
                    lang = environ['lang']

                if self.with_cookie:
                    response_headers.append(self.cookie_header(lang))

            response_headers.append(('Content-Language', lang))

            return start_response(status, response_headers)

        environ['lang'] = lang
        environ['lang.origin'] = lang # shouldn't be touched

        return self.application(environ, _start_response)
