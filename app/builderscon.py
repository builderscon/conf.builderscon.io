import config
import flask
import flask_babel
import flasktools
import functools
import os
import octav
import re
import sessionmgr

app = flask.Flask("builderscon")
babel = flask_babel.Babel(app)

LANGUAGES=[
    {'name': 'English', 'value': 'en'},
    {'name': 'Japanese', 'value': 'ja'}
]

def initialize():
    global api, cache, cfg

    import blueprints
    app.register_blueprint(blueprints.auth.page)
    app.register_blueprint(blueprints.cfp.page)
    app.register_blueprint(blueprints.conference.page)
    app.register_blueprint(blueprints.root.page)
    app.register_blueprint(blueprints.session.page)
    app.register_blueprint(blueprints.sharaq.page)
    app.register_blueprint(blueprints.user.page)

    config_file = os.getenv("CONFIG_FILE")
    if not config_file:
        raise Exception("missing CONFIG_FILE environemnt variable")
    cfg = config.Config(config_file)

    api = octav.Octav(**cfg.section('OCTAV'))

    if os.getenv('CACHE_BACKEND', 'Redis') == 'Redis':
        import cache_redis
        cache = cache_redis.Cache(**cfg.section('REDIS_INFO'))
    else:
        import cache_memd
        cache = cache_memd.Cache(**cfg.section('MEMCACHED'))

    app.secret_key = cfg.section('Flask').get('secret_key')
    app.base_url = cfg.section('Flask').get('base_url', 'https://builderscon.io')
    app.session_interface = sessionmgr.build(os.getenv('SESSION_BACKEND', 'Redis'), cfg)

# Get the current locale
jarx = re.compile('^ja(?:-\w+)$')
@babel.localeselector
def get_locale():
    l = flask.request.args.get('lang')
    if not l:
        stash = flask.g.get('stash')
        if stash:
            u = stash.get('user')
            if u:
                l = u.get('lang', l)
        # This is silly, accept_languages.best_match doesn't
        # match against ja-JP if the arguments are just 'ja'
        # TODO: Lookup Accept-Language, and change its value
        # to make the matching easier
        if not l:
            l = flask.request.accept_languages.best_match(['ja', 'ja-JP', 'en'])
    if l:
        if jarx.match(l):
            l = 'ja'
        return l
    return 'en'

# stash is where we keep values that get automatically passed
# to the template when rendering
@app.before_request
def init_stash():
    lang = get_locale()
    flask.g.api = api
    flask.g.lang = lang # this gets a special slot
    flask.g.stash = dict(
        lang=lang
    )

# Inject the stash and other assorted goodes so that they are
# available in the template
@app.context_processor
def inject_template_vars():
    stash = flask.g.stash
    stash["languages"] = LANGUAGES
    stash["flask_session"] = flask.session
    stash["url"] = flask.url_for
    return stash

def load_logged_in_user():
    has_octav_session = True
    for k in ['octav_session_id', 'octav_session_expires']:
        if k not in flask.session:
            print("Could not find key %s" % k)
            has_octav_session = False
            break

    if not has_octav_session:
        for k in ['access_token', 'user_id']:
            if k not in flask.session:
                return False

        s = api.new_session(flask.session['access_token'], flask.session['user_id'])
        if s is None:
            return False
        flask.session['octav_session_id'] = s.sid
        flask.session['octav_session_expires'] = s.expires
    else:
        sid = flask.session['octav_session_id']
        print("session exists %s" % sid)
        expires = flask.session['octav_session_expires']
        f = functools.partial(api.create_client_session, flask.session['access_token'], flask.session['user_id'])
        s = octav.Session(api, f, sid, expires)
        v = s.renew()
        print("result of renew %s" % v)
        if v is None:
            return False
        if v:
            # Update the stored octav session ID
            flask.session['octav_session_id'] = s.sid
            flask.session['octav_session_expires'] = s.expires
    flask.g.api = s

    if 'user_id' in flask.session:
        user = api.lookup_user(flask.session.get('user_id'))
        if user:
            flask.g.stash['user'] = user
            flask.g.lang = get_locale()
            return True
        del flask.session['user_id']
    return False

def load_user_only(cb, **args):
    load_logged_in_user()
    return cb(**args)

def load_user_or_login(cb, **args):
    if load_logged_in_user():
        return cb(**args)
    next_url = flask.request.path + "?" + flasktools.urlencode(flask.request.args)
    query = flasktools.urlencode({'.next': next_url})
    return flask.redirect("/login?" + query)

@app.errorhandler(404)
def page_not_found(e):
    return flask.render_template('errors/404.tpl'), 404

@app.errorhandler(500)
def internal_sever_error(e):
    flask.g.stash["error"] = e
    return flask.render_template('errors/500.tpl'), 500



