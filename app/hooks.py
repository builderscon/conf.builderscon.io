import builderscon
import flask
import flasktools
import functools

CACHE_CONFERENCE_EXPIRES = 300
CACHE_SESSION_EXPIRES = 300

def check_login(cb, **args):
    return functools.update_wrapper(functools.partial(builderscon.load_user_only, cb, **args), cb)


# Check if we have the user session field pre-populated.
def require_login(cb, **args):
    return functools.update_wrapper(functools.partial(builderscon.load_user_or_login, cb, **args), cb)

def require_email(cb, **args):
    return functools.update_wrapper(functools.partial(check_email, cb, **args), cb)

def check_email(cb, **args):
    user = flask.g.stash.get('user')
    if not user:
        return "require_login must be called first", 500

    if not user.get('email'):
        next_url = flask.request.path + "?" + flasktools.urlencode(flask.request.args)
        flask.session['next_url_after_email_registration'] = next_url
        return flask.redirect('/user/email/register')

    return cb(**args)

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

def _get_session(id, lang):
    key = session_cache_key(id, lang)
    session = builderscon.cache.get(key)
    if not session:
        session = builderscon.api.lookup_session(id=id, lang=lang)
        if not session:
            return None
        builderscon.cache.set(key, session, CACHE_SESSION_EXPIRES)
    return session

def session_cache_key(id, lang):
    if not id:
        raise Exception("faild to create session cache key: no id")
    return "session.%s.lang.%s" % (id, lang)

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
            session_types = builderscon.api.list_session_types_by_conference(conference_id=conference_id, lang=flask.g.lang)

        if not session_types:
            session_types = []

        flask.g.stash["session_types"] = session_types

        return cb(**args)

    return functools.update_wrapper(functools.partial(load_session_types, cb), cb)

def load_conference_by_slug(cb, series_slug, slug, **args):
    if slug == 'latest':
        conference = _get_latest_conference(series_slug, flask.g.lang)
        if conference:
            slug = conference.get('slug')
            full_slug = "%s/%s" % (series_slug, slug)
    else:
        full_slug = "%s/%s" % (series_slug, slug)
        conference = _get_conference_by_slug(full_slug, flask.g.lang)

    if not conference:
        return flask.abort(404)

    if conference.get('redirect_url'):
        return flask.redirect(conference.get('redirect_url'))

    flask.g.stash['series_slug'] = series_slug
    flask.g.stash['slug'] = slug
    flask.g.stash['full_slug'] = full_slug
    flask.g.stash['conference_id'] = conference.get('id')
    flask.g.stash['conference'] = conference
    return cb(**args)

def with_latest_conference(cb):
    return functools.update_wrapper(functools.partial(load_conference_by_slug, cb, slug='latest'), cb)

def with_conference_by_slug(cb):
    return functools.update_wrapper(functools.partial(load_conference_by_slug, cb), cb)

def latest_conference_cache_key(series_slug):
    if not series_slug:
        raise Exception("faild to create conference cache key: no series_slug")
    return "conference.latest.%s" % series_slug

def _get_latest_conference(series_slug, lang):
    key = latest_conference_cache_key(series_slug)
    cid = builderscon.cache.get(key)
    if cid:
        return _get_conference(id=cid, lang=lang)

    # XXX There should be a specific API call for this
    conferences = builderscon.api.list_conference(lang=lang)
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


def conference_by_slug_cache_key(full_slug):
    if not full_slug:
        raise Exception("faild to create conference cache key: no full_slug")
    return "conference.by_slug.%s" % full_slug

def conference_cache_key(id, lang):
    if not id:
        raise Exception("faild to create conference cache key: no id")
    return "conference.%s.lang.%s" % (id, lang)

def _get_conference(id, lang):
    key = conference_cache_key(id, lang)
    conference = builderscon.cache.get(key)
    if not conference:
        conference = builderscon.api.lookup_conference(id=id, lang=lang)
        if not conference:
            return None
        builderscon.cache.set(key, conference, CACHE_CONFERENCE_EXPIRES)
    return conference

def _get_conference_by_slug(slug, lang):
    slugkey = conference_by_slug_cache_key(slug)
    cid = builderscon.cache.get(slugkey)
    if cid:
        return _get_conference(id=cid, lang=lang)

    conference = builderscon.api.lookup_conference_by_slug(slug="/"+slug, lang=lang)
    if not conference:
        return None

    cid = conference.get('id')
    if cid:
        builderscon.cache.set(slugkey, cid, CACHE_CONFERENCE_EXPIRES)
    return conference

def with_user(cb, lang=''):
    def load_user(cb, id, lang, **args):
        if not lang:
            lang = flask.g.lang

        user = _get_user(id=id, lang=lang)
        if not user:
            return builderscon.api.last_error(), 404
        flask.g.stash["user"] = user
        return cb(**args)
    return functools.update_wrapper(functools.partial(load_user, cb, lang=lang), cb)

def _get_user(id, lang):
    key = user_cache_key(id, lang)
    user = builderscon.cache.get(key)
    if not user:
        user = builderscon.api.lookup_user(id=id)
        if not user:
            return None
        builderscon.cache.set(key, user, CACHE_SESSION_EXPIRES)
    return user

def user_cache_key(id, lang):
    if not id:
        raise Exception("faild to create user cache key: no id")
    return "user.%s.lang.%s" % (id, lang)


