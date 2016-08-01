#!/usr/bin/env python
# -*- coding:utf-8 -*-

import flask
import flask_babel
import babel.support
import time
from requestlogger import WSGILogger, ApacheFormatter
from logging import StreamHandler
import functools
import json
import os
import cache
from uuid import uuid4
from octav import Octav
import markdown
from mdx_gfm import GithubFlavoredMarkdownExtension
import feedparser
import re
import model
import flasktools

import sys
if sys.version[0] == "3":
    from urllib.parse import urlencode
else:
    from urllib import urlencode

if os.getenv('SERVER_SOFTWARE', '').startswith('Google App Engine/') or os.getenv('SERVER_SOFTWARE', '').startswith('Development/'):
    import urllib3.contrib.appengine
    http = urllib3.contrib.appengine.AppEngineManager()
else:
    import urllib3
    http = urllib3.PoolManager()

CACHE_CONFERENCE_EXPIRES = 300
CACHE_CONFERENCE_SESSIONS_EXPIRES = 300



class Config(object):
    def __init__(self, file):
        with open(file, 'r') as f:
            self.cfg = json.load(f)

        for section in ['OCTAV', 'REDIS_INFO', 'GITHUB', 'GOOGLE_MAP']:
            if not self.cfg.get(section):
                raise Exception( "missing section '" + section + "' in config file '" + file + "'" )
        if self.cfg.get('OCTAV').get('BASE_URI'):
            raise Exception(
                'DEPRECATED: {"OCTAV":{"BASE_URI"}} in config.json is deprecated.\
 Please use {"OCTAV":{"endpoint"}} instead and remove {"OCTAV":{"BASE_URI"}}.'
        )

    def section(self, name):
        return self.cfg.get(name)

    def googlemap_api_key(self):
        return self.cfg.get("GOOGLE_MAP").get("api_key")

config_file = os.getenv(
    "CONFIG_FILE",
    os.path.join(os.path.dirname(__file__), 'config.json')
)
cfg = Config(config_file)

flaskapp = flask.Flask("builderscon")
flaskapp.url_map.converters['regex'] = flasktools.RegexConverter
babel = flask_babel.Babel(flaskapp)
app = WSGILogger(flaskapp, [StreamHandler(sys.stdout)], ApacheFormatter())


octav = Octav(**cfg.section('OCTAV'))

cache = cache.Redis(**cfg.section('REDIS_INFO'))


class ConferenceNotFoundError(Exception):
    pass


def session(func):
    @functools.wraps(func)
    def _(*a, **ka):
        if _session_user() != '':
            return func(*a, **ka)
        else:
            flask.redirect('/login')
    return _


# Note: this has to come BEFORE other handlers
@flaskapp.route('/favicon.ico')
def favicon():
    flask.abort(404)

@flaskapp.route('/beacon')
def beacon():
    return flask.render_template('beacon.tpl')

@flaskapp.template_filter('dateobj')
def dateobj_filter(s, lang='en'): # note: this is probably going to be deprecated
    return model.ConferenceDate(s, lang)

markdown_converter = markdown.Markdown(extensions=[GithubFlavoredMarkdownExtension()]).convert
@flaskapp.template_filter('markdown')
def markdown_filter(s):
    return markdown_converter(s)

@flaskapp.context_processor
def inject_template_vars():
    return dict(
        flask_session=flask.session,
        url=flask.url_for
    )

@babel.localeselector
def get_locale():
    l = flask.request.args.get('lang')
    if l:
        return l
    return flask.request.accept_languages.best_match(['ja', 'en'])

@flaskapp.route('/')
def index():
    lang = get_locale()
    key = "conferences.lang." + lang
    conferences = cache.get(key)
    if not conferences:
        conferences = octav.list_conference(lang=lang)
        if conferences is None:
            raise HTTPError(status=500, body=octav.last_error())
        cache.set(key, conferences, 600)
    return flask.render_template('index.tpl',
        pagetitle='top',
        conferences=conferences
    )

@flaskapp.route('/login')
def login():
    lang = get_locale()
    return flask.render_template('login.tpl', {
        'pagetitle': 'login',
        'url': url
    }, languages=[lang])

@flaskapp.route('/login/github')
def login_github():
    code = flask.request.query.code
    ghcfg = cfg.section('GITHUB')
    if not code:
        return flask.redirect(
            'https://github.com/login/oauth/authorize' +
            '?client_id=' + ghcfg.get('client_id')
        )
    params={
        'code': code,
        'client_id': ghcfg.get('client_id'),
        'client_secret': ghcfg.get('client_secret')
    }
    access_token = http.request('GET', 'https://github.com/login/oauth/access_token?%s' % urlencode(params))
    if 'error' in access_token.text:
        return flask.redirect('/login')

    res = http.request('GET',
        'https://api.github.com/user?' + access_token.text
    )
    user_info = res.json()
    _create_session(user_info['login'])
    return flask.redirect('/')


@flaskapp.route('/logout')
@flaskapp.route('/<path:p>/logout')
def logout(p=None):
    response.set_cookie('session_id', '', expires=0)
    flask.redirect('/')

# This route maps "latest" URLs to the actual latest conference
# URLs, so that we don't have to refer to "latest" elsewhere in 
# the code
@flaskapp.route('/<series_slug>/<regex("latest(/.*)?"):rest>')
def latest(series_slug, rest):
    lang = get_locale()
    latest_conference = _get_latest_conference(series_slug, lang)
    if not latest_conference:
        raise ConferenceNotFoundError
    rest = re.compile('^latest').sub(latest_conference.get('slug'), rest)
    flask.redirect("/" + series_slug + "/" + rest)


@flaskapp.route('/<series_slug>')
def conference(series_slug):
    flask.redirect('/{0}/latest'.format(series_slug))


@flaskapp.route('/<series_slug>/<path:slug>/sponsors')
def conference_sponsors(series_slug, slug):
    lang = get_locale()
    full_slug = "%s/%s" % (series_slug, slug)
    conference = _get_conference_by_slug(full_slug, lang)
    return flask.render_template('sponsors.tpl',
        slug=full_slug,
        pagetitle=series_slug + ' ' + slug,
        conference=conference,
    )


@flaskapp.route('/<series_slug>/<path:slug>/sessions')
def conference_sessions(series_slug, slug):
    lang = get_locale()
    full_slug = "%s/%s" % (series_slug, slug)
    conference = _get_conference_by_slug(full_slug, lang)
    if not conference:
        raise ConferenceNotFoundError
    conference_sessions = _list_session_by_conference(conference.get('id'), lang)
    return flask.render_template('sessions.tpl',
        pagetitle=series_slug + ' ' + slug,
        conference=conference,
        sessions=conference_sessions,
        login={'username': _session_user()},
    )


@flaskapp.route('/<path:slug>/news')
def conference_news(slug):
    lang = get_locale()
    key = "news_entries.lang." + lang
    news_entries = cache.get(key)
    if not news_entries:
        feed_url = 'http://blog.builderscon.io/feed.xml'
        news = feedparser.parse(feed_url)
        if not news.entries:
            raise HTTPError(status=500, body="Failed to get news from Atom feed = " + feed_url + ", check if the feed is generated there." )
        else:
            news_entries = news.entries
            cache.set(key, news.entries, 600)

    filtered_entries = []
    for entry in news_entries:
        if entry.category == slug:
            if not entry.published_parsed:
                entry.date = ""
            else:
                entry.date = time.strftime( '%b %d, %Y', entry.published_parsed )
            filtered_entries.append(entry)
    return flask.render_template('news.tpl',
        slug=slug,
        entries=filtered_entries,
        login={'username': _session_user()}
    )


@flaskapp.route('/<series_slug>/<path:slug>')
def conference_instance(series_slug, slug):
    lang = get_locale()
    full_slug = "%s/%s" % (series_slug, slug)
    conference = _get_conference_by_slug(full_slug, lang)
    if not conference:
        raise HTTPError(status=404, body=octav.last_error())

    return flask.render_template('conference.tpl',
        pagetitle=series_slug + ' ' + slug,
        slug=full_slug,
        conference=conference,
        lang=lang,
        googlemap_api_key=cfg.googlemap_api_key()
    )

@flaskapp.route('/<series_slug>/<slug>/session/add')
def add_session(series_slug, slug):
    lang = get_locale()
    return flask.render_template('add_session.tpl', 
        pagetitle=series_slug + ' ' + slug
    )


@flaskapp.route('/<series_slug>/<slug>/session/add', methods=['POST'])
def add_session_post(series_slug, slug):
    flask.redirect('/')


@flaskapp.route('/<series_slug>/<slug>/session/<id>')
def conference_session_details(series_slug, slug, id):
    lang = get_locale()
    session = octav.lookup_session(lang=lang, id=id)
    if not session:
        return octav.last_error(), 404
    return flask.render_template('session_detail.tpl',
        pagetitle=series_slug + ' ' + slug,
        session=session
    )

@flaskapp.route('/speaker/<id>')
def speaker_details(id):
    lang = get_locale()
    return flask.render_template('speaker_details.tpl',
        pagetitle='spkeaker',
        login={'username': _session_user()},
    )


@flaskapp.route('/user/<int:id_>')
def user_details(id_):
    lang = get_locale()
    return flask.render_template('user_details.tpl',
        pagetitle='user',
        login={'username': _session_user()}
    )

def conference_cache_key(id, lang):
    if not id:
        raise Exception("faild to create conference cache key: no id")
    return "conference.%s.lang.%s" % (id, lang)

def conference_by_slug_cache_key(full_slug):
    if not full_slug:
        raise Exception("faild to create conference cache key: no full_slug")
    return "conference.by_slug.%s" % full_slug

def latest_conference_cache_key(series_slug):
    if not series_slug:
        raise Exception("faild to create conference cache key: no series_slug")
    return "conference.latest.%s" % series_slug

def conference_sessions_cache_key(conference_id, lang):
    if not conference_id:
        raise Exception("faild to create conference cache key: no id")
    return "conference_sessions.%s.lang%s" % (conference_id, lang)

def _get_conference(id, lang):
    key = conference_cache_key(id, lang)
    conference = cache.get(key)
    if not conference:
        conference = octav.lookup_conference(id=id, lang=lang)
        if not conference:
            return None
        cache.set(key, conference, CACHE_CONFERENCE_EXPIRES)
    return conference


def _get_conference_by_slug(slug, lang):
    slugkey = conference_by_slug_cache_key(slug)
    cid = cache.get(slugkey)
    if cid:
        return _get_conference(id=cid, lang=lang)

    conference = octav.lookup_conference_by_slug(slug="/"+slug, lang=lang)
    if not conference:
        return None

    cid = conference.get('id')
    if cid:
        cache.set(slugkey, cid, CACHE_CONFERENCE_EXPIRES)
    return conference


def _get_latest_conference(series_slug, lang):
    key = latest_conference_cache_key(series_slug)
    cid = cache.get(key)
    if cid:
        return _get_conference(id=cid, lang=lang)

    # XXX There should be a specific API call for this
    conferences = octav.list_conference(lang=lang)
    if conferences is None:
        return None

    for conference in conferences:
        series = conference.get("series")
        if not series:
            continue
        slug = series.get("slug")
        if not slug:
            continue
        if str(slug) == series_slug:
            return conference

    return None


def _list_session_by_conference(conference_id, lang):
    key = conference_sessions_cache_key(conference_id, lang)
    conference_sessions = cache.get(key)
    if conference_sessions:
        return conference_sessions

    conference_sessions = octav.list_session_by_conference(conference_id)
    if conference_sessions :
        cache.set(key, conference_sessions, CACHE_CONFERENCE_SESSIONS_EXPIRES)
        return conference_sessions
    return None


def _create_session(username):
    session_id = str(uuid4())
    expire_time = 5*60*60
    cache.set(session_id, username, expire_time)
    response.set_cookie(
        'session_id',
        session_id,
        expires=expire_time,
        path='/'
    )
    request.environ["__current_session"] = username
    return session_id


if __name__ == '__main__':
    from wsgiref import simple_server
    server = simple_server.make_server('', 3000, app)
    server.serve_forever()
