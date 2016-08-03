#!/usr/bin/env python
# -*- coding:utf-8 -*-

import flask
import flask_babel
import time
from requestlogger import WSGILogger, ApacheFormatter
from logging import StreamHandler
import json
import os
import cache
from octav import Octav
import markdown
from mdx_gfm import GithubFlavoredMarkdownExtension
import feedparser
import re
import model
import flasktools
import functools
import sys
import oauth

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

# stash is where we keep values that get automatically passed
# to the template when rendering
@flaskapp.before_request
def init_stash():
    lang = get_locale()
    flask.g.lang = lang # this gets a special slot
    flask.g.stash = dict(
        lang=lang
    )

# Inject the stash and other assorted goodes so that they are
# available in the template
@flaskapp.context_processor
def inject_template_vars():
    stash = flask.g.stash
    stash["flask_session"] = flask.session
    stash["url"] = flask.url_for
    return stash

# Check if we have the user session field pre-populated.
def require_login(cb):
    def check_login(cb, **args):
        if not 'user' in flask.session:
            query = flasktools.urlencode({
                '.next': flask.request.path + "?" + flasktools.urlencode(flask.request.args)
            })
            return flask.redirect("/login?" + query)
        return cb(**args)
    return functools.update_wrapper(functools.partial(check_login, cb), cb)

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

@babel.localeselector
def get_locale():
    l = flask.request.args.get('lang')
    if l:
        return l
    l = flask.request.accept_languages.best_match(['ja', 'en'])
    if l:
        return l
    return 'en'

@flaskapp.route('/')
def index():
    key = "conferences.lang." + flask.g.lang

    conferences = cache.get(key)
    if not conferences:
        conferences = octav.list_conference(lang=flask.g.lang)
        if conferences is None:
            return octav.last_error(), 500
        cache.set(key, conferences, 600)
    return flask.render_template('index.tpl',
        pagetitle='top',
        conferences=conferences
    )

@flaskapp.route('/login')
def login():
    return flask.render_template('login.tpl',
        pagetitle='login'
    )

@flaskapp.route('/login/github')
def login_github():
    return do_oauth(oauth.Github(http, cfg.section('GITHUB')))

@flaskapp.route('/login/facebook')
def login_facebook():
    return do_oauth(oauth.Facebook(http, cfg.section('FACEBOOK')))

@flaskapp.route('/login/twitter')
def login_twitter():
    return do_oauth(oauth.Facebook(http, cfg.section('TWITTER')))

def do_oauth(v):
    res = v.handle_auth()
    if res.is_redirect():
        return flask.redirect(res.redirect)
    if res.is_error():
        return res.error, 500

    flask.session["user"] = res.userinfo


@flaskapp.route('/logout')
@flaskapp.route('/<path:p>/logout')
def logout(p=None):
    flask.session.clear()
    flask.redirect('/')

# This route maps "latest" URLs to the actual latest conference
# URLs, so that we don't have to refer to "latest" elsewhere in 
# the code
@flaskapp.route('/<series_slug>/<regex("latest(/.*)?"):rest>')
def latest(series_slug, rest):
    latest_conference = _get_latest_conference(series_slug, flask.g.lang)
    if not latest_conference:
        raise ConferenceNotFoundError
    rest = re.compile('^latest').sub(latest_conference.get('slug'), rest)
    return flask.redirect("/" + series_slug + "/" + rest)


@flaskapp.route('/<series_slug>')
def conference(series_slug):
    flask.redirect('/{0}/latest'.format(series_slug))


@flaskapp.route('/<series_slug>/<path:slug>/sponsors')
def conference_sponsors(series_slug, slug):
    full_slug = "%s/%s" % (series_slug, slug)
    conference = _get_conference_by_slug(full_slug, flask.g.lang)
    return flask.render_template('sponsors.tpl',
        slug=full_slug,
        pagetitle=series_slug + ' ' + slug,
        conference=conference,
    )


@flaskapp.route('/<series_slug>/<path:slug>/sessions')
def conference_sessions(series_slug, slug):
    full_slug = "%s/%s" % (series_slug, slug)
    conference = _get_conference_by_slug(full_slug, flask.g.lang)
    if not conference:
        raise ConferenceNotFoundError
    conference_sessions = _list_session_by_conference(conference.get('id'), flask.g.lang)
    return flask.render_template('sessions.tpl',
        pagetitle=series_slug + ' ' + slug,
        conference=conference,
        sessions=conference_sessions
    )


@flaskapp.route('/<regex("(.+)"):slug>/news')
def conference_news(slug):
    key = "news_entries.lang." + flask.g.lang
    news_entries = cache.get(key)
    if not news_entries:
        feed_url = 'http://blog.builderscon.io/feed.xml'
        news = feedparser.parse(feed_url)
        if not news.entries:
            return 'Failed to get news from Atom feed = %, check if the feed is generated there.' % feed_url, 500
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
        entries=filtered_entries
    )


@flaskapp.route('/<series_slug>/<path:slug>')
def conference_instance(series_slug, slug):
    full_slug = "%s/%s" % (series_slug, slug)
    conference = _get_conference_by_slug(full_slug, flask.g.lang)
    if not conference:
        return octav.last_error(), 404

    return flask.render_template('conference.tpl',
        pagetitle=series_slug + ' ' + slug,
        slug=full_slug,
        conference=conference,
        googlemap_api_key=cfg.googlemap_api_key()
    )

@flaskapp.route('/<series_slug>/<slug>/session/add')
def add_session(series_slug, slug):
    return flask.render_template('add_session.tpl', 
        pagetitle=series_slug + ' ' + slug
    )


@flaskapp.route('/<series_slug>/<slug>/session/add', methods=['POST'])
def add_session_post(series_slug, slug):
    flask.redirect('/')


@flaskapp.route('/<series_slug>/<slug>/session/<id>')
def conference_session_details(series_slug, slug, id):
    session = octav.lookup_session(lang=flask.g.lang, id=id)
    if not session:
        return octav.last_error(), 404
    return flask.render_template('session_detail.tpl',
        pagetitle=series_slug + ' ' + slug,
        session=session
    )

@flaskapp.route('/speaker/<id>')
def speaker_details(id):
    return flask.render_template('speaker_details.tpl',
        pagetitle='spkeaker'
    )


@flaskapp.route('/user/<int:id_>')
def user_details(id_):
    return flask.render_template('user_details.tpl',
       pagetitle='user'
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


if __name__ == '__main__':
    from wsgiref import simple_server
    server = simple_server.make_server('', 3000, app)
    server.serve_forever()
