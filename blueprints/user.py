import app
import flask
import functools

page = flask.Blueprint('user', __name__)

require_login = app.hooks.require_login
with_user = app.hooks.with_user

@page.route('/dashboard')
@require_login
def dashboard():
    user = flask.g.stash.get('user')
    conferences = app.api.list_conferences_by_organizer(organizer_id=user.get('id'))
    sessions = app.api.list_sessions(
        speaker_id = user.get('id'),
        status     = ['pending', 'accepted', 'rejected'],
        lang       = flask.g.lang
    )

    return flask.render_template('dashboard.tpl',
        user=user,
        conferences=conferences,
        sessions=sessions
    )

@page.route('/user/<id>')
@with_user
def view():
    sessions = app.api.list_sessions(
        speaker_id=flask.g.stash.get("user").get("id"),
        status=["accepted"],
        lang=flask.g.lang
    )
    if not sessions:
        sessions = []
    flask.g.stash["sessions"] = sessions

    return flask.render_template('user/view.tpl')

@page.route('/user/email/register', methods=['GET'])
@require_login
def email_register():
    return flask.render_template('user/email_register.tpl')

@page.route('/user/email/register', methods=['POST'])
@require_login
def email_register_post():
    email = flask.request.form.get('email')
    if not email:
        return "email is required", 500

    ok = app.api.create_temporary_email(
        user_id = flask.g.stash.get('user').get('id'),
        target_id = flask.g.stash.get('user').get('id'),
        email = email
    )
    if not ok:
        return app.api.last_error(), 500
    flask.g.stash['show_directions'] = True
    return flask.redirect('/user/email/confirm')

@page.route('/user/email/confirm', methods=['GET'])
@require_login
def email_confirm():
    v = flask.request.args.get('confirmation_key')
    if v:
        flask.g.stash['confirmation_key'] = v
    return flask.render_template('user/email_confirm.tpl')

@page.route('/user/email/confirm', methods=['POST'])
@require_login
def email_confirm_post():
    confirmation_key = flask.request.form.get('confirmation_key')
    if not confirmation_key:
        return "confirmation_key is required", 500

    user = flask.g.stash.get('user')
    ok = app.api.confirm_temporary_email(
        user_id = user.get('id'),
        target_id = user.get('id'),
        confirmation_key = confirmation_key
    )
    if not ok:
        return app.api.last_error(), 500

    user = app.api.lookup_user_by_auth_user_id(auth_via=user['auth_via'], auth_user_id=user['auth_user_id'])
    flask.g.stash['user'] = user

    return flask.redirect('/user/email/done')

@page.route('/user/email/done', methods=['GET'])
@require_login
def email_done():
    if 'next_url_after_email_registration' in flask.session:
        flask.g.stash['next_url'] = flask.session['next_url_after_email_registration']
        del flask.session['next_url_after_email_registration']
    return flask.render_template('user/email_done.tpl')

def with_session_from_args(cb, fname='id'):
    def load_session_from_args(cb, **args):
        id = flask.request.values.get(fname)
        session = app.api.lookup_session(id=id, lang=flask.g.lang)
        flask.g.stash["session"] = session
        if not session:
            return app.api.last_error(), 404

        return cb(**args)
    return functools.update_wrapper(functools.partial(load_session_from_args, cb), cb)

@page.route('/user/edit', methods=['GET'])
@require_login
def edit():
    flask.g.stash["next_url"] = flask.request.args.get('.next')
    flask.g.stash["setup"] = flask.request.args.get('setup')
    return flask.render_template('user/edit.tpl')

@page.route('/user/update', methods=['POST'])
@require_login
def update():
    user = flask.g.stash.get('user')
    ok = app.api.update_user(
        id = user.get('id'),
        lang = flask.request.values.get('lang'),
        user_id = user.get('id'),
    )
    if not ok:
        flask.flash('failed to update', 'error')

    next_url = flask.request.values.get('.next')
    if next_url:
        return flask.redirect(next_url)

    return flask.redirect('/dashboard')

