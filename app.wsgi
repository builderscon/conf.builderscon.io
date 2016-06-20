#!/usr/bin/env python
# -*- coding:utf-8 -*-

from bottle import Bottle, redirect, request
from bottle import jinja2_view as view
from bottle import static_file
from datetime import date, datetime as dt
import functools
import json
import requests

with open('conf.json', 'r') as f:
    cfg = json.load(f)

app = application = Bottle()
route = app.route
url = app.get_url


class ConferenceNotFoundError(Exception):
    pass


@route('/')
@view('index.tpl')
def index():
    return {
        "pagetitle": "top",
        "conferences": _get_conference_list(),
        "url": url
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
        res = requests.get(
            'https://api.github.com/user?' + access_token.text
        )
        user_info = res.json()
        _save_auth(user_info['name'], 'GitHub', access_token.text)
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
        'url': url
    }


@route('/<series_slug>/<slug>/session/<id_:int>')
@view('session_detail.tpl')
def conference_session_details(series_slug, slug, id_):
    endpoint = cfg['API_BASE_URI'] + '/session/lookup'
    res = json.loads(requests.get(endpoint + '?id=' + id_).text)
    return {
        'pagetitle': series_slug + ' ' + slug,
        'session': session,
        'url': url
    }


@route('/speaker/<id_:int>')
def speaker_details(id_):
    return {
        'pagetitle': 'spkeaker',
        'url': url
    }


@route('/user/<id_:int>')
def user_details(id_):
    return {
        'pagetitle': 'user',
        'url': url
    }


@route('/assets/<filename:path>', name='statics')
def statics(filename):
    return static_file(filename, root='assets')


def _get_conference_list():
    endpoint = cfg['API_BASE_URI'] + '/conference/list'
    res = json.loads(requests.get(endpoint).text)
    return res


def _get_conference(series_slug, slug):
    conferences = _get_conference_list()
    for conference in conferences:
        if (
                str(conference['series']['slug']) == series_slug and
                str(conference['slug']) == slug
        ):
            return conference
    raise ConferenceNotFoundError


def _get_latest_conference(series_slug):
    conferences = _get_conference_list()
    for conference in conferences:
        if str(conference['series']['slug']) == series_slug:
            return conference
    raise ConferenceNotFoundError


def _save_auth(username, auth_with, access_token):
    query = 'INSERT INTO users (username, auth, token) VALUES (%s, %s, %s);'
    with MySQLdb.connect(cursorclass=DictCursor, **cfg['DB_INFO']) as cursor:
        try:
            cursor.execute(
                query,
                (username, auth_with, access_token)
            )
        except:
            return False
        else:
            return True
