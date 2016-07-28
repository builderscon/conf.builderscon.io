#!/usr/bin/env python
# -*- coding:utf-8 -*-

import bottle
from bottle import Bottle, redirect, request, response, HTTPError, static_file
from datetime import datetime, timedelta
import time
from requestlogger import WSGILogger, ApacheFormatter
from logging import StreamHandler
import functools
import json
import requests
import os
import cache
from accept_language import LangDetector
from uuid import uuid4
from octav import Octav
from sys import stdout
import markdown
from mdx_gfm import GithubFlavoredMarkdownExtension
import feedparser
from view import jinja2_template as template
import re

CACHE_CONFERENCE_EXPIRES = 300

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

app = application = Bottle()
bottle.BaseTemplate.settings.update({
    'extensions': ['jinja2.ext.i18n'],
    'globals': {
        'url': app.get_url
    },
    'filters': {
        'markdown': markdown.Markdown(extensions=[GithubFlavoredMarkdownExtension()]).convert
    }
})


route = app.route
post = app.post
url = app.get_url
app = LangDetector(app, languages=["ja", "en"])
app = WSGILogger(app, [StreamHandler(stdout)], ApacheFormatter())


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
            redirect('/login')
    return _


# Note: this has to come BEFORE other handlers
@route('/favicon.ico')
def favicon():
    raise HTTPError(status=404)

# Note: this has to come BEFORE other handlers
@route('/assets/<filename:path>', name='statics')
def statics(filename):
    return static_file(filename, root='assets')

@route('/beacon')
def beacon():
    lang = request.environ.get("lang")
    return template('beacon.tpl', {}, lang=lang)

@route('/')
def index():
    lang = request.environ.get("lang")
    key = "conferences.lang." + lang
    conferences = cache.get(key)
    if not conferences:
        conferences = octav.list_conference(lang=lang)
        if conferences is None:
            raise HTTPError(status=500, body=octav.last_error())
        cache.set(key, conferences, 600)
    return template('index.tpl', {
        'pagetitle': 'top',
        'conferences': conferences,
        'login': {'username': _session_user()},
        'url': url
    }, languages=[lang])

@route('/login')
def login():
    lang = request.environ.get("lang")
    return template('login.tpl', {
        'pagetitle': 'login',
        'url': url
    }, languages=[lang])

@route('/login/github')
def login_github():
    code = request.query.code
    ghcfg = cfg.section('GITHUB')
    if not code:
        redirect(
            'https://github.com/login/oauth/authorize' +
            '?client_id=' + ghcfg.get('client_id')
        )
    access_token = requests.get(
        'https://github.com/login/oauth/access_token',
        params={
            'code': code,
            'client_id': ghcfg.get('client_id'),
            'client_secret': ghcfg.get('client_secret')
        }
    )
    if 'error' in access_token.text:
        redirect('/login')

    res = requests.get(
        'https://api.github.com/user?' + access_token.text
    )
    user_info = res.json()
    _create_session(user_info['login'])
    redirect('/')


@route('/logout')
@route('/<p:path>/logout')
def logout(p=None):
    response.set_cookie('session_id', '', expires=datetime.now()-timedelta(1))
    redirect('/')

# This route maps "latest" URLs to the actual latest conference
# URLs, so that we don't have to refer to "latest" elsewhere in 
# the code
@route('/<series_slug>/<rest:re:latest(/.*)?>')
def latest(series_slug, rest):
    lang = request.environ.get("lang")
    latest_conference = _get_latest_conference(series_slug, lang)
    if not latest_conference:
        raise ConferenceNotFoundError
    rest = re.compile('^latest').sub(latest_conference.get('slug'), rest)
    redirect("/" + series_slug + "/" + rest)


@route('/<series_slug>')
def conference(series_slug):
    redirect('/{0}/latest'.format(series_slug))


@route('/<series_slug>/<slug:path>/sponsors')
def conference_sponsors(series_slug, slug):
    lang = request.environ.get("lang")
    full_slug = "%s/%s" % (series_slug, slug)
    conference = _get_conference_by_slug(full_slug, lang)
    return template('sponsors.tpl', {
        'slug': full_slug,
        'pagetitle': series_slug + ' ' + slug,
        'conference': conference,
        'login': {'username': _session_user()},
        'url': url
    }, languages=[lang])


@route('/<slug:path>/news')
def conference_news(slug):
    lang = request.environ.get("lang")
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
    return template('news.tpl', {
        'slug': slug,
        'entries': filtered_entries,
        'login': {'username': _session_user()},
        'url': url
    }, languages=[lang])


@route('/<series_slug>/<slug:path>')
def conference_instance(series_slug, slug):
    lang = request.environ.get("lang")
    full_slug = "%s/%s" % (series_slug, slug)
    conference = _get_conference_by_slug(full_slug, lang)
    return template('conference.tpl', {
        'pagetitle': series_slug + ' ' + slug,
        'slug': full_slug,
        'conference': conference,
        'login': {'username': _session_user()},
        'url': url,
        'googlemap_api_key': cfg.googlemap_api_key(),
    }, languages=[lang])


@route('/<series_slug>/<slug>/sessions')
def conference_sessions(series_slug, slug):
    lang = request.environ.get("lang")
    conference = _get_conference_by_slug(series_slug, slug)
    if not conference:
        raise ConferenceNotFoundError

    return template('sessions.tpl', {
        'pagetitle': series_slug + ' ' + slug,
        'conference': conference,
        'login': {'username': _session_user()},
        'url': url
    }, languages=[lang])


@route('/<series_slug>/<slug>/session/add')
def add_session(series_slug, slug):
    lang = request.environ.get("lang")
    return template('add_session.tpl', {
        'pagetitle': series_slug + ' ' + slug,
        'login': {'username': _session_user()},
        'url': url
    }, languages=[lang])


@post('/<series_slug>/<slug>/session/add')
def add_session_post(series_slug, slug):
    redirect('/')


@route('/<series_slug>/<slug>/session/<id>')
def conference_session_details(series_slug, slug, id):
    lang = request.environ.get("lang")
    session = octav.lookup_session(lang=lang, id=id)
    if not session:
        raise HTTPError(status=404, body=octav.last_error())
    return template('session_detail.tpl',{
        'pagetitle': series_slug + ' ' + slug,
        'session': session,
        'login': {'username': _session_user()},
        'url': url
    }, languages=[lang])

@route('/speaker/<id>')
def speaker_details(id):
    lang = request.environ.get("lang")
    return template('speaker_details.tpl', {
        'pagetitle': 'spkeaker',
        'login': {'username': _session_user()},
        'url': url
    }, languages=[lang])


@route('/user/<id_:int>')
def user_details(id_):
    lang = request.environ.get("lang")
    return template('user_details.tpl', {
        'pagetitle': 'user',
        'login': {'username': _session_user()},
        'url': url
    }, languages=[lang])

def conference_cache_key(id, lang):
    if not id:
        raise Exception("faild to create conference cache key: no id")
    return "conference.%d.lang" % id

def conference_by_slug_cache_key(full_slug):
    if not id:
        raise Exception("faild to create conference cache key: no full_slug")
    return "conference.by_slug.%s" % full_slug

def latest_conference_cache_key(series_slug):
    if not series_slug:
        raise Exception("faild to create conference cache key: no series_slug")
    return "conference.latest.%s" % series_slug

def _get_conference(id, lang):
    key = conference_cache_key(conference, lang)
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


def _session_user():
    session_id = request.get_cookie('session_id')
    username = request.environ.get("__current_session")
    if username is not None:
        return username

    username = cache.get(session_id)
    if username is None:
        return ''
    request.environ["__current_session"] = username
    return username


if __name__ == '__main__':
    from wsgiref import simple_server
    server = simple_server.make_server('', 3000, app)
    server.serve_forever()
