#!/usr/bin/env python
# -*- coding:utf-8 -*-

import bottle
from bottle import Bottle, redirect, request, response, HTTPError, static_file
from bottle import jinja2_view as view
from datetime import datetime, timedelta
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

class Config(object):
    def __init__(self, file):
        with open(file, 'r') as f:
            self.cfg = json.load(f)

        for section in ['OCTAV', 'REDIS_INFO', 'GITHUB', 'GOOGLE_MAP']:
            if not self.cfg.get(section):
                raise "missing section '" + section + "' in config file '" + file + "'"
        if self.cfg.get('OCTAV').get('BASE_URI'):
            raise Exception(
                'DEPRECATED: {"OCTAV":{"BASE_URI"}} in config.json is deprecated.\
 Please use {"OCTAV":{"endpoint"}} instead and remove {"OCTAV":{"BASE_URI"}}.'
        )

    def section(self, name):
        return self.cfg.get(name)

    def googlemap_api_key(self):
        self.cfg.get("GOOGLE_MAP").get("api_key")

config_file = os.getenv(
    "CONFIG_FILE",
    os.path.join(os.path.dirname(__file__), 'config.json')
)
cfg = Config(config_file)

bottle.BaseTemplate.settings.update({'filters': {'markdown': markdown.Markdown(extensions=[GithubFlavoredMarkdownExtension()]).convert}})
app = application = Bottle()
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


@route('/')
@view('index.tpl')
def index():
    lang = request.environ.get("lang")
    key = "conferences.lang." + lang
    conferences = cache.get(key)
    if not conferences:
        conferences = octav.list_conference(lang=lang)
        if conferences is None:
            raise HTTPError(status=500, body=octav.last_error())
        cache.set(key, conferences, 600)
    return {
        'pagetitle': 'top',
        'body_id': "top",
        'conferences': conferences,
        'login': {'username': _session_user()},
        'url': url
    }


@route('/login')
@view('login.tpl')
def login():
    return {
        'pagetitle': 'login',
        'url': url
    }


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


@route('/<series_slug>')
def conference(series_slug):
    redirect('/{0}/latest'.format(series_slug))


@route('/<series_slug>/<slug:path>/sponsors')
@view('sponsors.tpl')
def conference_sponsors(series_slug, slug):
    lang = request.environ.get("lang")
    conference = _get_conference_by_slug(series_slug, slug, lang)
    return {
        'pagetitle': series_slug + ' ' + slug,
        'conference': conference,
        'login': {'username': _session_user()},
        'url': url
    }

@route('/speaker/<id_:int>')
@route('/<series_slug>/<slug:path>')
@view('conference.tpl')
def conference_instance(series_slug, slug):
    lang = request.environ.get("lang")
    if slug == 'latest':
        conference = _get_latest_conference(series_slug)
    else:
        conference = _get_conference_by_slug(series_slug, slug, lang)
    return {
        'pagetitle': series_slug + ' ' + slug,
        'conference': conference,
        'login': {'username': _session_user()},
        'url': url,
        'googlemap_api_key': cfg.googlemap_api_key(),
    }


@route('/<series_slug>/<slug>/sessions')
@view('sessions.tpl')
def conference_sessions(series_slug, slug):
    if slug == 'latest':
        conference = _get_latest_conference(series_slug)
    else:
        conference = _get_conference_by_slug(series_slug, slug)
    return {
        'pagetitle': series_slug + ' ' + slug,
        'conference': conference,
        'login': {'username': _session_user()},
        'url': url
    }


@route('/<series_slug>/<slug>/session/add')
@view('add_session.tpl')
@session
def add_session(series_slug, slug):
    return {
        'pagetitle': series_slug + ' ' + slug,
        'login': {'username': _session_user()},
        'url': url
    }


@post('/<series_slug>/<slug>/session/add')
@session
def add_session_post(series_slug, slug):
    redirect('/')


@route('/<series_slug>/<slug>/session/<id>')
@view('session_detail.tpl')
def conference_session_details(series_slug, slug, id):
    lang = request.environ.get("lang")
    session = octav.lookup_session(lang=lang, id=id)
    if not session:
        raise HTTPError(status=404, body=octav.last_error())
    return {
        'pagetitle': series_slug + ' ' + slug,
        'session': session,
        'login': {'username': _session_user()},
        'url': url
    }

def speaker_details(id_):
    return {
        'pagetitle': 'spkeaker',
        'login': {'username': _session_user()},
        'url': url
    }


@route('/user/<id_:int>')
def user_details(id_):
    return {
        'pagetitle': 'user',
        'login': {'username': _session_user()},
        'url': url
    }


def _get_conference(id, lang):
    key = "conference." + id
    conference = cache.get(key)
    if not conference:
        conference = octav.lookup_conference(id=id, lang=lang)
        if not conference:
            return ConferenceNotFoundError
        cache.sete(key, conference, 300)
    return conference


def _get_conference_by_slug(series_slug, slug, lang):
    slug_query = '/' + series_slug + '/' + slug
    slugkey = "conference.by_slug." + slug_query
    cid = cache.get(slugkey)
    if cid:
        return _get_conference(id=id, lang=lang)

    conference = octav.lookup_conference_by_slug(slug=slug_query, lang=lang)
    if conference:
        key = "conference." + conference["id"]
        seconds = 300
        cache.set(key, conference, seconds)
        return conference
    raise ConferenceNotFoundError


def _get_latest_conference(series_slug, lang):
    # XXX There should be a specific API call for this
    conferences = octav.list_conference(lang=lang)
    if conferences is None:
        raise ConferenceNotFoundError
    for conference in conferences:
        if str(conference['series']['slug']) == series_slug:
            return conference


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
