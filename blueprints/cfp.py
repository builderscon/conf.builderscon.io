import app
import flask
import hashlib
import os
import random
import re
import time

page = flask.Blueprint('cfp', __name__)

check_login = app.hooks.check_login
require_login = app.hooks.require_login
require_email = app.hooks.require_email
with_conference_by_slug = app.hooks.with_conference_by_slug
with_session_types = app.hooks.with_session_types

@page.route('/<series_slug>/<path:slug>/cfp')
@require_login
@require_email
@with_conference_by_slug
@with_session_types
def view():
    key = flask.request.args.get('key')
    if key:
        session = flask.session.get(key)
        if not session:
            return flask.abort(404)
        flask.g.stash["session"] = session

    f = '%s/cfp.tpl' % flask.g.stash.get('full_slug')
    return flask.render_template([f, 'cfp.tpl'])

@page.route('/<series_slug>/<path:slug>/cfp/input', methods=['GET','POST'])
@require_login
@require_email
@with_conference_by_slug
@with_session_types
def input():
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
        for l in app.LANGUAGES:
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

@page.route('/<series_slug>/<path:slug>/cfp/confirm')
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

@page.route('/<series_slug>/<path:slug>/cfp/commit', methods=['GET','POST'])
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
        session = app.api.create_session(**values)
        if session:
            del flask.session[key]
    except:
        # TODO: capture, and do the right thing
        pass

    if session:
        return flask.redirect('/%s/cfp_done?id=%s' % (flask.g.stash.get('full_slug'), session.get('id')))

    return flask.render_template('cfp.tpl')

@page.route('/<series_slug>/<path:slug>/cfp_done')
@require_login
@require_email
@with_conference_by_slug
@with_session_types
def confernece_cfp_done():
    id = flask.request.values.get('id')
    session = app.api.lookup_session(lang='all', id=id)
    if not session:
        return app.api.last_error(), 404

    flask.g.stash["session"] = session
    return flask.render_template('cfp_done.tpl')


