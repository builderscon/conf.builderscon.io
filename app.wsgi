#!/usr/bin/env python
# -*- coding:utf-8 -*-

from bottle import Bottle, redirect, request, response
from bottle import jinja2_view as view
from bottle import static_file
from datetime import date, datetime, timedelta
import functools
import json
import MySQLdb
from MySQLdb.cursors import DictCursor as DC
import requests
from uuid import uuid4
import os

from octav import Octav

config_file = os.path.join(os.path.dirname(__file__), 'config.json')
with open(config_file, 'r') as f:
    cfg = json.load(f)

app = application = Bottle()
route = app.route
post = app.post
url = app.get_url

octav = Octav()


class ConferenceNotFoundError(Exception):
    pass


def session(func):
    @functools.wraps(func)
    def _(*a, **ka):
        if _has_session():
            return func(*a, **ka)
        else:
            redirect('/login')
    return _


@route('/')
@view('index.tpl')
def index():
    return {
        'pagetitle': 'top',
        'conferences': octav.list_conference().json(),
        'login': {'username': _session_user()} if _has_session() else '',
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
    if not code:
        redirect(
            'https://github.com/login/oauth/authorize' +
            '?client_id=' + cfg['GITHUB']['client_id']
        )
    else:
        access_token = requests.get(
            'https://github.com/login/oauth/access_token',
            params={
                'code': code,
                'client_id': cfg['GITHUB']['client_id'],
                'client_secret': cfg['GITHUB']['client_secret']
            }
        )
        if 'error' not in access_token.text:
            res = requests.get(
                'https://api.github.com/user?' + access_token.text
            )
            user_info = res.json()
            _create_session(user_info['login'])
            redirect('/')
        else:
            redirect('/login')


@route('/logout')
@route('/<p:path>/logout')
def logout(p=None):
    response.set_cookie('username', '')
    response.set_cookie('session_id', '', expires=datetime.now()-timedelta(1))
    redirect('/')


@route('/<series_slug>')
def conference(series_slug):
    redirect('/{0}/latest'.format(series_slug))


@route('/<series_slug>/<slug>')
@view('conference.tpl')
def conference_per_instance(series_slug, slug):
    if slug == 'latest':
        conference = _get_latest_conference(series_slug)
    else:
        conference = _get_conference(series_slug, slug)
    return {
        'pagetitle': series_slug + ' ' + slug,
        'conference': conference,
        'login': {'username': _session_user()} if _has_session() else '',
        'url': url
    }


@route('/<series_slug>/<slug>/sessions')
@view('sessions.tpl')
def conference_sessions(series_slug, slug):
    if slug == 'latest':
        conference = _get_latest_conference(series_slug)
    else:
        conference = _get_conference(series_slug, slug)
    return {
        'pagetitle': series_slug + ' ' + slug,
        'conference': conference,
        'login': {'username': _session_user()} if _has_session() else '',
        'url': url
    }


@route('/<series_slug>/<slug>/session/add')
@view('add_session.tpl')
@session
def add_session(series_slug, slug):
    return {
        'pagetitle': series_slug + ' ' + slug,
        'login': {'username': _session_user()} if _has_session() else '',
        'url': url
    }

@post('/<series_slug>/<slug>/session/add')
@session
def add_session_post(series_slug, slug):
    redirect('/')


@route('/<series_slug>/<slug>/session/<id_:int>')
@view('session_detail.tpl')
def conference_session_details(series_slug, slug, id_):
    endpoint = cfg['API_BASE_URI'] + '/session/lookup'
    res = json.loads(requests.get(endpoint + '?id=' + id_).text)
    return {
        'pagetitle': series_slug + ' ' + slug,
        'session': session,
        'login': {'username': _session_user()} if _has_session() else '',
        'url': url
    }


@route('/speaker/<id_:int>')
def speaker_details(id_):
    return {
        'pagetitle': 'spkeaker',
        'login': {'username': _session_user()} if _has_session() else '',
        'url': url
    }


@route('/user/<id_:int>')
def user_details(id_):
    return {
        'pagetitle': 'user',
        'login': {'username': _session_user()} if _has_session() else '',
        'url': url
    }


@route('/assets/<filename:path>', name='statics')
def statics(filename):
    return static_file(filename, root='assets')



def _get_conference(series_slug, slug):
    slug_query = '/' + series_slug + '/' + slug
    conference = octav.lookup_conference_by_slug(slug_query).json()
    if conference:
        return conference
    else:
        raise ConferenceNotFoundError


def _get_latest_conference(series_slug):
    conferences = octav.list_conference().json()
    for conference in conferences:
        if str(conference['series']['slug']) == series_slug:
            return conference
    raise ConferenceNotFoundError


def _create_session(username):
    query = 'INSERT INTO auth_sessions VALUES (%s, %s, %s);'
    session_id = str(uuid4())
    expire = datetime.now() + timedelta(7)
    with MySQLdb.connect(cursorclass=DC, **cfg['DB_INFO']) as cursor:
        try:
            cursor.execute(
                query,
                (username, session_id, expire)
            )
        except:
            return False
        else:
            response.set_cookie('username', username, path='/')
            response.set_cookie('session_id', session_id, expires=expire, path='/')
            return session_id


def _has_session():
    username = request.get_cookie('username')
    session_id = request.get_cookie('session_id')
    query = '''SELECT * FROM auth_sessions
    WHERE username=%s AND session_id=%s;'''
    with MySQLdb.connect(cursorclass=DC, **cfg['DB_INFO']) as cursor:
        cursor.execute(
            query,
            (username, session_id)
        )
        row = cursor.fetchone()
    return (row and row['expire'] > datetime.now())


def _session_user():
    if _has_session():
        return request.get_cookie('username')
    else:
        return ''


if __name__ == '__main__':
    from wsgiref import simple_server
    server = simple_server.make_server('', 3000, application)
    server.serve_forever()
