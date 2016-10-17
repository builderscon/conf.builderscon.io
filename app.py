#!/usr/bin/env python
# -*- coding:utf-8 -*-

import flask
import flask_babel
import flask_oauth
import markupsafe
import time
import hashlib
import random
from requestlogger import WSGILogger, ApacheFormatter
from logging import StreamHandler
import json
import os
import cache
import sessionmgr
from octav import Octav
import markdown
from mdx_gfm import GithubFlavoredMarkdownExtension
import feedparser
import re
import model
import flasktools
import functools
import traceback
import sys

CACHE_CONFERENCE_EXPIRES = 300
CACHE_CONFERENCE_SESSIONS_EXPIRES = 300
CACHE_SESSION_EXPIRES = 300
LANGUAGES=[
    {'name': 'English', 'value': 'en'},
    {'name': 'Japanese', 'value': 'ja'}
]

class Config(object):
    def __init__(self, file):
        with open(file, 'r') as f:
            self.cfg = json.load(f)

        for section in ['OCTAV', 'REDIS_INFO', 'GITHUB', 'GOOGLE_MAP']:
            if not self.cfg.get(section):
                raise Exception( "missing section '" + section + "' in config file '" + file + "'" )
        if self.cfg.get('OCTAV').get('BASE_URI'):
            raise Exception(
                'DEPRECATED: {"OCTAV":{"BASE_URI"}} in config.json is deprecated.'
                ' Please use {"OCTAV":{"endpoint"}} instead and remove {"OCTAV":{"BASE_URI"}}.'
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
flaskapp.secret_key = cfg.section('Flask').get('secret_key')
flaskapp.base_url = cfg.section('Flask').get('base_url', 'https://builderscon.io')
flaskapp.url_map.converters['regex'] = flasktools.RegexConverter
babel = flask_babel.Babel(flaskapp)
app = WSGILogger(flaskapp, [StreamHandler(sys.stdout)], ApacheFormatter())

octav = Octav(**cfg.section('OCTAV'))

cache = cache.build(os.getenv('CACHE_BACKEND', 'Redis'), cfg)

flaskapp.session_interface = sessionmgr.build(os.getenv('SESSION_BACKEND', 'Redis'), cfg)

oauth = flask_oauth.OAuth()
twitter = oauth.remote_app('twitter',
    base_url='https://api.twitter.com/1.1/',
    request_token_url='https://api.twitter.com/oauth/request_token',
    access_token_url='https://api.twitter.com/oauth/access_token',
    authorize_url='https://api.twitter.com/oauth/authenticate',
    consumer_key=cfg.section('TWITTER').get('client_id'),
    consumer_secret=cfg.section('TWITTER').get('client_secret').encode('ASCII')
)

facebook = oauth.remote_app('facebook',
    base_url='https://graph.facebook.com/',
    request_token_url=None,
    access_token_url='/oauth/access_token',
    authorize_url='https://www.facebook.com/dialog/oauth',
    consumer_key=cfg.section('FACEBOOK').get('client_id'),
    consumer_secret=cfg.section('FACEBOOK').get('client_secret').encode('ASCII'),
    request_token_params={'scope': 'email'}
)

github = oauth.remote_app('github',
    base_url='https://api.github.com',
    request_token_url=None,
    authorize_url='https://github.com/login/oauth/authorize',
    access_token_url='https://github.com/login/oauth/access_token',
    consumer_key=cfg.section('GITHUB').get('client_id'),
    consumer_secret=cfg.section('GITHUB').get('client_secret').encode('ASCII'),
    request_token_params={'scope': ''}
)

class ConferenceNotFoundError(Exception):
    pass

class OAuthError(Exception):
    pass

@flaskapp.errorhandler(404)
def page_not_found(e):
    return flask.render_template('errors/404.tpl'), 404

@flaskapp.errorhandler(500)
def internal_sever_error(e):
    flask.g.stash["error"] = e
    return flask.render_template('errors/500.tpl'), 500

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
    stash["languages"] = LANGUAGES
    stash["flask_session"] = flask.session
    stash["url"] = flask.url_for
    return stash

@flaskapp.template_filter('is_oauth_error')
def is_oauth_error(v):
    return type(v) is OAuthError

# Used in templates, when all you have is the user's input value
@flaskapp.template_filter('permname')
def permission_value_to_name(v):
    return v.title()

@flaskapp.template_filter('audlevelname')
def audience_level_value_to_name(v):
    return v.title()

# Used in templates, when all you have is the user's input value
@flaskapp.template_filter('langname')
def lang_value_to_name(v):
    for l in LANGUAGES:
        if l.get('value') == v:
            return l.get('name')
    return ""

@flaskapp.template_filter('urlencode')
def urlencode_filter(s):
    if type(s) == 'Markup':
        s = s.unescape()
    s = s.encode('utf8')
    s = flasktools.quote_plus(s)
    return markupsafe.Markup(s)

def load_logged_in_user():
    if 'user_id' in flask.session:
        user = octav.lookup_user(flask.session.get('user_id'))
        if user:
            flask.g.stash['user'] = user
            return True
        del flask.session['user_id']
    return False

def load_user_only(cb, **args):
    load_logged_in_user()
    return cb(**args)

def check_login(cb, **args):
    return functools.update_wrapper(functools.partial(load_user_only, cb, **args), cb)

def load_user_or_login(cb, **args):
    if load_logged_in_user():
        return cb(**args)
    next_url = flask.request.path + "?" + flasktools.urlencode(flask.request.args)
    query = flasktools.urlencode({'.next': next_url})
    return flask.redirect("/login?" + query)

# Check if we have the user session field pre-populated.
def require_login(cb, **args):
    return functools.update_wrapper(functools.partial(load_user_or_login, cb, **args), cb)

def check_email(cb, **args):
    user = flask.g.stash.get('user')
    if not user:
        return "require_login must be called first", 500

    if not user.get('email'):
        next_url = flask.request.path + "?" + flasktools.urlencode(flask.request.args)
        flask.session['next_url_after_email_registration'] = next_url
        return flask.redirect('/user/email/register')

    return cb(**args)

def require_email(cb, **args):
    return functools.update_wrapper(functools.partial(check_email, cb, **args), cb)

# Note: this has to come BEFORE other handlers
@flaskapp.route('/favicon.ico')
def favicon():
    flask.abort(404)

@flaskapp.route('/beacon')
def beacon():
    return flask.render_template('beacon.tpl')

@flaskapp.template_filter('dateobj')
def dateobj_filter(s, lang='en', timezone='UTC'): # note: this is probably going to be deprecated
    return model.ConferenceDate(s, lang=lang, timezone=timezone)

markdown_converter = markdown.Markdown(extensions=[GithubFlavoredMarkdownExtension()]).convert
@flaskapp.template_filter('markdown')
def markdown_filter(s):
    return markdown_converter(s)

jarx = re.compile('^ja(?:-\w+)$')
@babel.localeselector
def get_locale():
    l = flask.request.args.get('lang')
    if not l:
        # This is silly, accept_languages.best_match doesn't
        # match against ja-JP if the arguments are just 'ja'
        # TODO: Lookup Accept-Language, and change its value
        # to make the matching easier
        l = flask.request.accept_languages.best_match(['ja', 'ja-JP', 'en'])
    if l:
        if jarx.match(l):
            l = 'ja'
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

@flaskapp.route('/dashboard')
@require_login
def dashboard():
    user = flask.g.stash.get('user')
    conferences = octav.list_conferences_by_organizer(organizer_id=user.get('id'))
    sessions = octav.list_sessions(
        speaker_id = user.get('id'),
        status     = ['pending', 'accepted', 'rejected'],
        lang       = flask.g.lang
    )

    return flask.render_template('dashboard.tpl',
        user=user,
        conferences=conferences,
        sessions=sessions
    )



def start_oauth(oauth_handler, callback):
    try:
        args = {}
        if flask.request.args.get('.next'):
            args['.next'] = flask.request.args.get('.next')

        if len(args.keys()) > 0:
            callback = '%s?%s' % (callback, flasktools.urlencode(args))

        return oauth_handler.authorize(callback=callback)
    except:
        print(traceback.format_exc())
        raise OAuthError
    

@flaskapp.route('/login')
def login():
    return flask.render_template('login.tpl',
        next_url=flask.request.args.get('.next')
    )

@github.tokengetter
def get_github_token(token=None):
    print("get_github_token")
    return flask.session.get('github_token')

@flaskapp.route('/login/github')
def login_github():
    return start_oauth(github, flaskapp.base_url + '/login/github/callback')

@flaskapp.route('/login/github/callback')
@github.authorized_handler
def login_github_callback(resp):
    if resp is None:
        err = flask.request.args.get('error_description') or flask.request.args.get('error')
        return flask.render_template('login.tpl', error=err)
    if 'error' in resp:
        err = resp.get('error_description') or resp.get('error')
        return flask.render_template('login.tpl', error=err)

    flask.session['github_token'] = (
        resp['access_token'],
        ''
    )
    res = github.request('user')
    if res.status != 200:
        print("got status %d" % res.status)
        print(res.data)
        return flask.render_template('login.tpl', error='failed to fetch user information after oauth')

    data = res.data

    # Load user via github id
    user = octav.lookup_user_by_auth_user_id(auth_via='github', auth_user_id=str(data['id']))
    if user:
        flask.session['user_id'] = user.get('id')
        flask.g.stash['user'] = user
        return flask.redirect(flask.request.args.get('.next') or '/')

    names = re.compile('\s+').split(data.get('name'))
    first_name = 'Unknown'
    last_name = 'Unknown'
    if len(names) > 1:
        first_name = names[0]
        last_name = names[-1]
    elif len(names) == 1:
        first_name = names[0]

    user = octav.create_user (
        str(data.get('id')),
        auth_via='github',
        nickname=data.get('login'),
        first_name=first_name,
        last_name=last_name,
        avatar_url='https://avatars.githubusercontent.com/u/' + str(data.get('id'))
    )
    if not user:
        return flask.render_template('login.tpl', error='failed to register user in the backend server')

    flask.session['user_id'] = user.get('id')
    flask.g.stash['user'] = user
    return flask.redirect(flask.request.args.get('.next') or '/')

@facebook.tokengetter
def get_facebook_token(token=None):
    return flask.session.get('facebook_token')

@flaskapp.route('/login/facebook')
def login_facebook():
    return start_oauth(facebook, flaskapp.base_url + '/login/facebook/callback')

@flaskapp.route('/login/facebook/callback')
@facebook.authorized_handler
def login_facebook_callback(resp):
    if resp is None:
        err = flask.request.args.get('error_description') or flask.request.args.get('error')
        return flask.render_template('login.tpl', error=err)

    flask.session['facebook_token'] = (
        resp['access_token'],
        ''
    )
    res = facebook.request('me')
    if res.status != 200:
        print("got status %d" % res.status)
        print(res.data)
        return flask.render_template('login.tpl', error='failed to fetch user information after oauth')

    data = res.data

    # Load user via facebook id
    user = octav.lookup_user_by_auth_user_id(auth_via='facebook', auth_user_id=data['id'])
    if user:
        flask.session['user_id'] = user.get('id')
        flask.g.stash['user'] = user
        return flask.redirect(flask.request.args.get('.next') or '/')

    names = re.compile('\s+').split(data.get('name'))
    first_name = 'Unknown'
    last_name = 'Unknown'
    if len(names) > 1:
        first_name = names[0]
        last_name = names[-1]
    elif len(names) == 1:
        first_name = names[0]

    params = dict({
        'height':130,
        'width': 130,
        'fields': 'url',
        'redirect': False
    })
    res = facebook.request('v2.7/me/picture', data=params)
    if res.status != 200:
        print("got status %d" % res.status)
        print(res.data)
        return flask.render_template('login.tpl', error='failed to fetch user photo after oauth')
    picture = res.data

    user = octav.create_user (
        data.get('id'),
        auth_via='facebook',
        nickname=data.get('name'),
        first_name=first_name,
        last_name=last_name,
        avatar_url=picture.get('data', dict()).get('url')
    )
    if not user:
        return flask.render_template('login.tpl', error='failed to register user in the backend server')

    flask.session['user_id'] = user.get('id')
    flask.g.stash['user'] = user
    return flask.redirect(flask.request.args.get('.next') or '/')

@twitter.tokengetter
def get_twitter_token(token=None):
    return flask.session.get('twitter_token')

@flaskapp.route('/login/twitter')
def login_twitter():
    if 'twitter_token' in flask.session:
        del flask.session['twitter_token']
    return start_oauth(twitter, flaskapp.base_url + '/login/twitter/callback')

@flaskapp.errorhandler(flask_oauth.OAuthException)
def handle_oauth_exception(e):
    return str(e)

@flaskapp.route('/login/twitter/callback')
@twitter.authorized_handler
def login_twitter_callback(resp):
    if resp is None:
        err = flask.request.args.get('error_description') or flask.request.args.get('error')
        return flask.render_template('login.tpl', error=err)

    flask.session['twitter_token'] = (
        resp['oauth_token'],
        resp['oauth_token_secret']
    )

    # Load user via twitter id
    user = octav.lookup_user_by_auth_user_id(auth_via='twitter', auth_user_id=resp['user_id'])
    if user:
        flask.session['user_id'] = user.get('id')
        flask.g.stash['user'] = user
        return flask.redirect(flask.request.args.get('.next') or '/')

    res = twitter.request('account/verify_credentials.json')
    if res.status != 200:
        print("got status %d" % res.status)
        print(res.data)
        return flask.render_template('login.tpl', error='failed to fetch user information after oauth')

    data = res.data

    avatar_url = data.get('profile_image_url')
    if avatar_url:
        avatar_url = re.compile('_normal\.').sub('_bigger.', avatar_url)

    names = re.compile('\s+').split(data.get('name'))
    first_name = 'Unknown'
    last_name = 'Unknown'
    if len(names) > 1:
        first_name = names[0]
        last_name = names[-1]
    elif len(names) == 1:
        first_name = names[0]

    user = octav.create_user (
        data.get('id_str'),
        auth_via='twitter',
        nickname=data.get('screen_name'),
        avatar_url=avatar_url, 
        first_name=first_name,
        last_name=last_name,
    )
    if not user:
        return flask.render_template('login.tpl', error='failed to register user in the backend server')

    flask.session['user_id'] = user.get('id')
    flask.g.stash['user'] = user
    return flask.redirect(flask.request.args.get('.next') or '/')


@flaskapp.route('/logout', methods=['POST'])
def logout(p=None):
    flask.session.clear()
    return flask.redirect('/')

@flaskapp.route('/user/email/register', methods=['GET'])
@require_login
def email_register():
    return flask.render_template('user/email_register.tpl')

@flaskapp.route('/user/email/register', methods=['POST'])
@require_login
def email_register_post():
    email = flask.request.form.get('email')
    if not email:
        return "email is required", 500

    ok = octav.create_temporary_email(
        user_id = flask.g.stash.get('user').get('id'),
        target_id = flask.g.stash.get('user').get('id'),
        email = email
    )
    if not ok:
        return octav.last_error(), 500
    flask.g.stash['show_directions'] = True
    return flask.redirect('/user/email/confirm')

@flaskapp.route('/user/email/confirm', methods=['GET'])
@require_login
def email_confirm():
    v = flask.request.args.get('confirmation_key')
    if v:
        flask.g.stash['confirmation_key'] = v
    return flask.render_template('user/email_confirm.tpl')

@flaskapp.route('/user/email/confirm', methods=['POST'])
@require_login
def email_confirm_post():
    confirmation_key = flask.request.form.get('confirmation_key')
    if not confirmation_key:
        return "confirmation_key is required", 500

    user = flask.g.stash.get('user')
    ok = octav.confirm_temporary_email(
        user_id = user.get('id'),
        target_id = user.get('id'),
        confirmation_key = confirmation_key
    )
    if not ok:
        return octav.last_error(), 500

    user = octav.lookup_user_by_auth_user_id(auth_via=user['auth_via'], auth_user_id=user['auth_user_id'])
    flask.g.stash['user'] = user

    return flask.redirect('/user/email/done')

@flaskapp.route('/user/email/done', methods=['GET'])
@require_login
def email_done():
    if 'next_url_after_email_registration' in flask.session:
        flask.g.stash['next_url'] = flask.session['next_url_after_email_registration']
        del flask.session['next_url_after_email_registration']
    return flask.render_template('user/email_done.tpl')

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

def with_conference_by_slug(cb):
    def load_conference_by_slug(cb, series_slug, slug, **args):
        full_slug = "%s/%s" % (series_slug, slug)
        conference = _get_conference_by_slug(full_slug, flask.g.lang)
        if not conference:
            return flask.abort(404)
        flask.g.stash['series_slug'] = series_slug
        flask.g.stash['slug'] = slug
        flask.g.stash['full_slug'] = full_slug
        flask.g.stash['conference'] = conference
        return cb(**args)
    return functools.update_wrapper(functools.partial(load_conference_by_slug, cb), cb)

@flaskapp.route('/<series_slug>/<path:slug>/sponsors')
@with_conference_by_slug
def conference_sponsors():
    return flask.render_template('sponsors.tpl')

@flaskapp.route('/<series_slug>/<path:slug>/sessions')
@with_conference_by_slug
def conference_sessions():
    conference = flask.g.stash.get('conference')
    sessions = _list_sessions(conference.get('id'), ['accepted', 'pending'], flask.g.lang)

    accepted = []
    pending  = []
    if sessions:
        for session in sessions:
            if session.get('status') == 'accepted':
                accepted.append(session)
            else:
                pending.append(session)

    flask.g.stash['accepted_sessions'] = accepted
    flask.g.stash['pending_sessions']  = pending
    return flask.render_template('session/list.tpl')

def with_session_types(cb):
    def load_session_types(cb, **args):
        conference_id = ''
        conference = flask.g.stash.get('conference')

        if conference:
            conference_id = conference.get('id')
        else:
            session = flask.g.stash.get('session')
            if session:
                conference_id = session.get('conference_id')

        if conference_id:
            session_types = octav.list_session_types_by_conference(conference_id=conference_id, lang=flask.g.lang)

        if not session_types:
            session_types = []

        flask.g.stash["session_types"] = session_types

        return cb(**args)

    return functools.update_wrapper(functools.partial(load_session_types, cb), cb)

@flaskapp.route('/<series_slug>/<path:slug>/cfp')
@require_login
@require_email
@with_conference_by_slug
@with_session_types
def conference_cfp():
    key = flask.request.args.get('key')
    if key:
        session = flask.session.get(key)
        if not session:
            return flask.abort(404)
        flask.g.stash["session"] = session

    f = '%s/cfp.tpl' % flask.g.stash.get('full_slug')
    return flask.render_template([f, 'cfp.tpl'])

@flaskapp.route('/<series_slug>/<path:slug>/cfp/input', methods=['GET','POST'])
@require_login
@require_email
@with_conference_by_slug
@with_session_types
def conference_cfp_input():
    if flask.request.method != 'POST':
        return flask.redirect('/%s/cfp' % flask.g.stash.get('full_slug'))

    form = flask.request.form
    # Silly to do this by hand, but I'm going to do this
    # right now so that we get better error reporting to uers
    required = ['session_type_id']
    flask.g.stash['missing'] = {}
    for f in required:
        if not form.get(f):
            print("missing %s" % f)
            flask.g.stash['errors'] = True
            flask.g.stash['missing'][f] = True
    l10n = {}
    required = ['title', 'abstract']
    flask.g.stash['missing'] = {}
    for f in required:
        has_l10n_field = False
        for l in LANGUAGES:
            v = l.get('value')
            if v == "en":
                continue
            l10nk = '%s#%s' %(f, v)
            l10nv = form.get(l10nk)
            if l10nv:
                has_l10n_field = True
                l10n[l10nk] = l10nv
                break

        if not has_l10n_field and not form.get(f):
            print("missing %s" % f)
            flask.g.stash['errors'] = True
            flask.g.stash['missing'][f] = True
    
    if flask.g.stash.get('errors') > 0:
        flask.g.stash["session"] = form
        return flask.render_template('cfp.tpl')

    h = hashlib.sha256()
    h.update('%f' % time.time())
    h.update('%f' % random.random())
    h.update('%d' % os.getpid())
    key = 'cfp_submission_%s' % h.hexdigest()
    flask.g.stash["submission_key"] = key

    conference = flask.g.stash.get('conference')
    user = flask.g.stash.get('user')
    flask.session[key] = dict(
        expires           = time.time() + 900,
        conference_id     = conference.get('id'),
        abstract          = form.get('abstract'),
        session_type_id   = form.get('session_type_id'),
        speaker_id        = user.get('id'),
        user_id           = user.get('id'),
        title             = form.get('title'),
        category          = form.get('category'),
        material_level    = form.get('material_level'),
        memo              = form.get('memo'),
        photo_release     = form.get('photo_release'),
        recording_release = form.get('recording_release'),
        materials_release = form.get('materials_release'),
        slide_language    = form.get('slide_language'),
        spoken_language   = form.get('spoken_language'),
        **l10n
    )

    pat = re.compile('^cfp_submission_')
    now = time.time()
    for k in list(flask.session):
        if not pat.match(k):
            continue
        v = flask.session.get(k)
        if v.get('expires') > now:
            continue
        del flask.session[k]

    return flask.redirect('/%s/cfp/confirm?key=%s' % (flask.g.stash.get('full_slug'), key))

@flaskapp.route('/<series_slug>/<path:slug>/cfp/confirm')
@require_login
@require_email
@with_conference_by_slug
@with_session_types
def conference_cfp_confirm():
    key = flask.request.args.get('key')
    session = flask.session.get(key)
    if not session:
        return flask.abort(404)

    session_type_id = session.get('session_type_id')
    for stype in flask.g.stash.get('session_types'):
        if stype.get('id') == session_type_id:
            flask.g.stash['session_type'] = stype
            break
    flask.g.stash['session'] = session
    flask.g.stash['submission_key'] = key
    return flask.render_template('cfp_confirm.tpl')

@flaskapp.route('/<series_slug>/<path:slug>/cfp/commit', methods=['GET','POST'])
@with_conference_by_slug
@with_session_types
def conference_cfp_commit():
    if flask.request.method != 'POST':
        return flask.redirect('/%s/cfp' % flask.g.stash.get('full_slug'))

    key = flask.request.form.get('key')
    values = flask.session.get(key)
    if not values:
        return flask.abort(404)
    try:
        del values['expires']
        session = octav.create_session(**values)
        if session:
            del flask.session[key]
    except:
        # TODO: capture, and do the right thing
        pass

    if session:
        return flask.redirect('/%s/cfp_done?id=%s' % (flask.g.stash.get('full_slug'), session.get('id')))

    return flask.render_template('cfp.tpl')

@flaskapp.route('/<series_slug>/<path:slug>/cfp_done')
@require_login
@require_email
@with_conference_by_slug
@with_session_types
def confernece_cfp_done():
    id = flask.request.values.get('id')
    session = octav.lookup_session(lang='all', id=id)
    if not session:
        return octav.last_error(), 404

    flask.g.stash["session"] = session
    return flask.render_template('cfp_done.tpl')

@flaskapp.route('/<series_slug>/<path:slug>/news')
@with_conference_by_slug
def conference_news():
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
    slug = flask.g.stash.get('full_slug')
    for entry in news_entries:
        if entry.category == slug:
            if not entry.published_parsed:
                entry.date = ""
            else:
                entry.date = time.strftime( '%b %d, %Y', entry.published_parsed )
            filtered_entries.append(entry)
    return flask.render_template('news.tpl', entries=filtered_entries)


@flaskapp.route('/<series_slug>/<path:slug>')
@with_conference_by_slug
def conference_instance():
    return flask.render_template('conference.tpl', googlemap_api_key=cfg.googlemap_api_key())

def with_session(cb, lang=''):
    def load_session(cb, id, lang, **args):
        if not lang:
            lang = flask.g.lang

        session = _get_session(id=id, lang=lang)
        if not session:
            return flask.abort(404)
        flask.g.stash["session"] = session

        if flask.g.stash["conference"]:
            if flask.g.stash["conference"].get('id') != session.get('conference_id'):
                return flask.abort(404)

        return cb(**args)
    return functools.update_wrapper(functools.partial(load_session, cb, lang=lang), cb)

def with_session_from_args(cb, fname='id'):
    def load_session_from_args(cb, **args):
        id = flask.request.values.get(fname)
        session = octav.lookup_session(id=id, lang=flask.g.lang)
        flask.g.stash["session"] = session
        if not session:
            return octav.last_error(), 404

        return cb(**args)
    return functools.update_wrapper(functools.partial(load_session_from_args, cb), cb)

def with_user(cb, lang=''):
    def load_user(cb, id, lang, **args):
        if not lang:
            lang = flask.g.lang

        user = _get_user(id=id, lang=lang)
        if not user:
            return octav.last_error(), 404
        flask.g.stash["user"] = user
        return cb(**args)
    return functools.update_wrapper(functools.partial(load_user, cb, lang=lang), cb)

@flaskapp.route('/<series_slug>/<path:slug>/session/<id>/update', methods=['POST'])
@require_login
@with_conference_by_slug
@functools.partial(with_session, lang='all')
@with_session_types
def session_update():
    form = flask.request.form
    # Silly to do this by hand, but I'm going to do this
    # right now so that we get better error reporting to uers
    required = ['session_type_id']
    flask.g.stash['missing'] = {}
    for f in required:
        if not form.get(f):
            print("missing %s" % f)
            flask.g.stash['errors'] = True
            flask.g.stash['missing'][f] = True
    l10n = {}
    required = ['title', 'abstract']
    flask.g.stash['missing'] = {}
    for f in required:
        has_field = False
        if form.get(f):
            has_field = True

        for l in LANGUAGES:
            v = l.get('value')
            if v == "en":
                continue
            l10nk = '%s#%s' %(f, v)
            l10nv = form.get(l10nk)
            if l10nv:
                has_field = True
                l10n[l10nk] = l10nv
                break

        if not has_field:
            print("missing %s" % f)
            flask.g.stash['errors'] = True
            flask.g.stash['missing'][f] = True
    
    if flask.g.stash.get('errors') > 0:
        flask.g.stash["session"] = form
        return flask.render_template('session/edit.tpl')

    user = flask.g.stash.get('user')
    try:
        id = flask.g.stash.get('session').get('id')
        ok = octav.update_session(
            id                = id,
            abstract          = form.get('abstract'),
            session_type_id   = form.get('session_type_id'),
            user_id           = user.get('id'),
            title             = form.get('title'),
            category          = form.get('category'),
            material_level    = form.get('material_level'),
            memo              = form.get('memo'),
            photo_release     = form.get('photo_release'),
            recording_release = form.get('recording_release'),
            materials_release = form.get('materials_release'),
            slide_language    = form.get('slide_language'),
            spoken_language   = form.get('spoken_language'),
            **l10n
        )
        if ok:
            for l in LANGUAGES:
                cache.delete(session_cache_key(id=id, lang=l.get('value')))
            cache.delete(session_cache_key(id=id, lang='all'))
            return flask.redirect('/%s/session/%s' % (flask.g.stash.get('full_slug'), id))
        else:
            flask.g.stash["error"] = octav.last_error()
    except BaseException as e:
        flask.g.stash["error"] = e
        print(e)
        pass

    # XXX redirect to a proper location
    return flask.render_template('session/edit.tpl')

@flaskapp.route('/<series_slug>/<path:slug>/session/<id>/edit')
@require_login
@with_conference_by_slug
@functools.partial(with_session, lang='all')
@with_session_types
def session_edit():
    return flask.render_template('session/edit.tpl')

@flaskapp.route('/<series_slug>/<path:slug>/session/<id>/delete', methods=['GET', 'POST'])
@require_login
@with_conference_by_slug
@with_session
def session_delete():
    method = flask.request.method

    pat = re.compile('^del_session_')
    now = time.time()
    for k in list(flask.session):
        if not pat.match(k):
            continue
        v = flask.session.get(k)
        if v.get('expires') > now:
            continue
        del flask.session[k]

    session = flask.g.stash["session"]
    if method == 'GET':
        token = "del_session_"
        flask.g.stash["delete_token"] = token
        flask.session[token] = dict(
            expires = time.time() + 900,
            id      = session.get('id')
        )
        return flask.render_template('session/delete.tpl')
    elif method == 'POST':
        token = flask.request.form.get('delete_token')
        data  = flask.session[token]
        if not data:
            return flask.abort(404)

        if data.get('id') != session.get('id'):
            return "Invalid token", 500

        del flask.session[token]
        user = flask.session.get("user")
        id = session.get('id')
        ok = octav.delete_session(
            id      = id,
            user_id = user.get('id')
        )
        if not ok:
            flask.g.stash["error"] = octav.last_error()
            return flask.render_template('session/delete.tpl')

        for l in LANGUAGES:
            cache.delete(session_cache_key(id=id, lang=l.get('value')))
        cache.delete(session_cache_key(id=id, lang='all'))
        return flask.redirect('/dashboard')
    else:
        return "", 401
        
@flaskapp.route('/<series_slug>/<path:slug>/session/<id>')
@check_login
@with_conference_by_slug
@with_session
def session_view():
    return flask.render_template('session/view.tpl')

@flaskapp.route('/user/<id>')
@with_user
def user_view():
    sessions = octav.list_sessions(
        speaker_id=flask.g.stash.get("user").get("id"),
        status=["accepted"],
        lang=flask.g.lang
    )
    if not sessions:
        sessions = []
    flask.g.stash["sessions"] = sessions

    return flask.render_template('user/view.tpl')

def user_cache_key(id, lang):
    if not id:
        raise Exception("faild to create user cache key: no id")
    return "user.%s.lang.%s" % (id, lang)

def session_cache_key(id, lang):
    if not id:
        raise Exception("faild to create session cache key: no id")
    return "session.%s.lang.%s" % (id, lang)

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

def conference_sessions_cache_key(conference_id, status, lang):
    if not conference_id:
        raise Exception("faild to create conference cache key: no id")
    return "conference_sessions.%s.status.%s.lang.%s" % (conference_id, status, lang)

def _get_user(id, lang):
    key = user_cache_key(id, lang)
    user = cache.get(key)
    if not user:
        user = octav.lookup_user(id=id)
        if not user:
            return None
        cache.set(key, user, CACHE_SESSION_EXPIRES)
    return user

def _get_session(id, lang):
    key = session_cache_key(id, lang)
    session = cache.get(key)
    if not session:
        session = octav.lookup_session(id=id, lang=lang)
        if not session:
            return None
        cache.set(key, session, CACHE_SESSION_EXPIRES)
    return session

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


def _list_sessions(conference_id, status, lang):
    key = conference_sessions_cache_key(conference_id, status, lang)
    conference_sessions = cache.get(key)
    if conference_sessions:
        return conference_sessions

    conference_sessions = octav.list_sessions(conference_id, lang=lang, status=status)
    if conference_sessions :
        cache.set(key, conference_sessions, CACHE_CONFERENCE_SESSIONS_EXPIRES)
        return conference_sessions
    return None


if __name__ == '__main__':
    from wsgiref import simple_server
    server = simple_server.make_server('', 3000, app)
    server.serve_forever()
