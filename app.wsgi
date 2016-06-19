#!/usr/bin/env python
# -*- coding:utf-8 -*-

from bottle import Bottle, redirect
from bottle import jinja2_view as view
from bottle import static_file
from datetime import date, datetime as dt
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
        "title": "top",
        "conferences": _get_conference_list(),
        "url": url
    }


@route('/login')
@view('login.tpl')
def login():
    return {'url': url}


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
    return {'conference': conference, 'url': url}


@route('/<series_slug>/<slug>/news')
def conference_latest_news(series_slug, slug):
    return {'url': url}


@route('/<series_slug>/<slug>/schedule')
def conference_schedule(series_slug, slug):
    return {'url': url}


@route('/<series_slug>/<slug>/session/<id_:int>')
def conference_session_details(series_slug, slug, id_):
    return {'url': url}


@route('/speaker/<id_:int>')
def speaker_details(id_):
    return {'url': url}


@route('/user/<id_:int>')
def user_details(id_):
    return {'url': url}


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
        if (str(conference['series']['slug']) == series_slug and
            str(conference['slug']) == slug):
            return conference
    raise ConferenceNotFoundError


def _get_latest_conference(series_slug):
    conferences = _get_conference_list()
    for conference in conferences:
        if str(conference['series']['slug']) == series_slug:
            return conference
    raise ConferenceNotFoundError
