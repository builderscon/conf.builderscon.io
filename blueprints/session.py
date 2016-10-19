import app
import app.hooks
import flask
import functools
import re
import time

LIST_EXPIRES = 300
page = flask.Blueprint('session', __name__)

check_login = app.hooks.check_login
require_login = app.hooks.require_login
with_conference_by_slug = app.hooks.with_conference_by_slug
with_session = app.hooks.with_session
with_session_types = app.hooks.with_session_types

@page.route('/<series_slug>/<path:slug>/sessions')
@with_conference_by_slug
def list():
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

def _list_sessions(conference_id, status, lang):
    key = list_cache_key(conference_id, status, lang)
    conference_sessions = app.cache.get(key)
    if conference_sessions:
        return conference_sessions

    conference_sessions = app.api.list_sessions(conference_id, lang=lang, status=status)
    if conference_sessions :
        app.cache.set(key, conference_sessions, LIST_EXPIRES)
        return conference_sessions
    return None

def list_cache_key(conference_id, status, lang):
    if not conference_id:
        raise Exception("faild to create conference cache key: no id")
    return "conference_sessions.%s.status.%s.lang.%s" % (conference_id, status, lang)

@page.route('/<series_slug>/<path:slug>/session/<id>')
@check_login
@with_conference_by_slug
@with_session
def view():
    return flask.render_template('session/view.tpl')

@page.route('/<series_slug>/<path:slug>/session/<id>/edit')
@require_login
@with_conference_by_slug
@functools.partial(with_session, lang='all')
@with_session_types
def edit():
    return flask.render_template('session/edit.tpl')

@page.route('/<series_slug>/<path:slug>/session/<id>/update', methods=['POST'])
@require_login
@with_conference_by_slug
@functools.partial(with_session, lang='all')
@with_session_types
def update():
    form = flask.request.form
    # Silly to do this by hand, but I'm going to do this
    # right now so that we get better error reporting to uers
    required = ['session_type_id']
    flask.g.stash['missing'] = {}
    for f in required:
        if not form.get(f):
            flask.g.stash['errors'] = True
            flask.g.stash['missing'][f] = True
    l10n = {}
    required = ['title', 'abstract']
    flask.g.stash['missing'] = {}
    for f in required:
        has_field = False
        if form.get(f):
            has_field = True

        for l in app.LANGUAGES:
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
            flask.g.stash['errors'] = True
            flask.g.stash['missing'][f] = True
    
    if flask.g.stash.get('errors') > 0:
        flask.g.stash["session"] = form
        return flask.render_template('session/edit.tpl')

    user = flask.g.stash.get('user')
    try:
        id = flask.g.stash.get('session').get('id')
        ok = app.api.update_session(
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
            for l in app.LANGUAGES:
                app.cache.delete(app.hooks.session_cache_key(id=id, lang=l.get('value')))
            app.cache.delete(app.hooks.session_cache_key(id=id, lang='all'))
            return flask.redirect('/%s/session/%s' % (flask.g.stash.get('full_slug'), id))
        else:
            flask.g.stash["error"] = app.api.last_error()
    except BaseException as e:
        flask.g.stash["error"] = e
        print(e)
        pass

    # XXX redirect to a proper location
    return flask.render_template('session/edit.tpl')

@page.route('/<series_slug>/<path:slug>/session/<id>/delete', methods=['GET', 'POST'])
@require_login
@with_conference_by_slug
@with_session
def delete():
    method = flask.request.method
    pat = re.compile('^del_session_')
    now = time.time()
    for k in flask.session:
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
            return flask.abort(500)

        del flask.session[token]
        user = flask.g.stash.get("user")
        id = session.get('id')
        ok = app.api.delete_session(
            id      = id,
            user_id = user.get('id')
        )
        if not ok:
            flask.g.stash["error"] = app.api.last_error()
            return flask.render_template('session/delete.tpl')

        for l in app.LANGUAGES:
            app.cache.delete(app.hooks.session_cache_key(id=id, lang=l.get('value')))
        app.cache.delete(app.hooks.session_cache_key(id=id, lang='all'))
        return flask.redirect('/dashboard')
    else:
        return flask.abort(401)
        

