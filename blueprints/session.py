import app
import app.hooks
import datetime
import flask
import functools
import iso8601
import model
import pytz
import re
import time
import uuid

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
    if conference.get('timetable_available'):
        return flask.redirect('/%s/timetable' % conference.get('full_slug'))
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
    return flask.render_template('v2017/session/list.html')

@page.route('/<series_slug>/<path:slug>/timetable')
@with_conference_by_slug
def timetable():
    conference = flask.g.stash.get('conference')
    if not conference.get('timetable_available'):
        return flask.redirect('/%s/sessions' % conference.get('full_slug'))

    tz = pytz.timezone(conference.get('timezone'))
    date = flask.request.args.get('date')
    if date:
        dt = datetime.datetime.strptime(date, '%Y-%m-%d')
        dt = tz.localize(dt)
        range_start = dt.isoformat('T')
        range_end = (dt + datetime.timedelta(days=1)).isoformat('T')
    else:
        cdt = model.ConferenceDate(conference.get('dates')[0], lang=flask.g.lang, timezone=conference.get('timezone'))
        dt = datetime.datetime(cdt.open.year, cdt.open.month, cdt.open.day, 0, 0, 0, 0, pytz.UTC)
        date = dt.strftime('%Y-%m-%d')
        range_start = dt.isoformat('T')
        range_end = (dt + datetime.timedelta(days=1)).isoformat('T')

    flask.g.stash['date'] = date

    # In this handler we cache two things:
    # 1) The raw JSON search result, and
    # 2) The HTML (gasp) generated by this method
    html_key = 'timetable.html.%s.%s.%s.%s.%s' % (conference.get('id'), ['accepted'], flask.g.lang, range_start, range_end)
    html = app.cache.get(html_key)
    if html:
        flask.g.stash['table'] = html
        return flask.render_template('session/timetable.tpl')

    sessions = _list_sessions(conference.get('id'), ['accepted'], flask.g.lang, range_start, range_end)
    sessions_by_room = dict()
    start_h = 9
    end_h = 22
    if sessions:
        min_start_h = 24
        max_end_h = 0
        for session in sessions:
            in_room = sessions_by_room.get(session.get('room_id'))
            if not in_room:
                in_room = []
                sessions_by_room[session.get('room_id')] = in_room
            in_room.append(session)
            starts_on = iso8601.parse_date(session.get('starts_on')).astimezone(tz)
            end_on = starts_on + datetime.timedelta(seconds=session.get('duration'))
            session['starts_on_obj'] = starts_on
            session['end_on_obj'] = end_on
            if starts_on.hour < min_start_h:
                min_start_h = starts_on.hour
            if end_on.hour > max_end_h:
                max_end_h = end_on.hour
        start_h = min_start_h
        end_h = max_end_h

        room_in_session = dict()
        rooms = dict()
        for r_id in sessions_by_room:
            r = flask.g.api.lookup_room(r_id)
            rooms[r_id] = r

        widthclass = 'room-col-%d' % (int(100 / len(rooms)))
        t = '<table class="ttt">\n' # time-table-table = ttt
        t += '<thead>\n<tr>\n<td class="top-left"></td>\n'
        for track in conference.get('tracks'):
            room_id = track.get('room_id')
            room_in_session[room_id] = 0
            t += '<td class="room-name %s">%s</td>\n' % (widthclass, track.get('name'))
        t += '</tr>\n</thead>\n<tbody>\n'

        for h in range(start_h, end_h + 1):
            for m in map(lambda n:n*5, range(0,12)):
                t += "<tr>\n"
                t += '<td class="time-cell">%02d:%02d</td>\n' % (h, m)
                for track in conference.get('tracks'):
                    room_id = track.get('room_id')
                    if room_id not in room_in_session:
                        continue
                    room_sessions = sessions_by_room.get(room_id)
                    session = None
                    st = None
                    if len(room_sessions) > 0:
                        session = room_sessions[0]
                        st = session.get('starts_on_obj')
                    if st is not None and st.hour == h and st.minute == m:
                        r = (session.get('duration') // 300)
                        su = '/%s/session/%s' % (conference.get('full_slug'), session.get('id'))
                        uu = '/user/%s' % (session.get('speaker').get('id'))
                        t += '<td class="session %s" rowspan="%d">' % (widthclass, r)
                        t += '<a href="%s"><img class="speaker-avatar" src="%s"></a> ' % (uu, session.get('speaker').get('avatar_url') or '/static/images/noprofile.png')
                        t += '<a class="title" href="%s">%s</a>' % (su, session.get('title'))
                        t += '</td>\n'
                        sessions_by_room[room_id] = room_sessions[1:]
                        room_in_session[room_id] = r - 1
                    elif room_in_session[room_id] > 0:
                        room_in_session[room_id] = room_in_session[room_id] - 1
                    else:
                        t += '<td class="empty %s padding"></td>\n' % widthclass
                t += '</tr>\n'
        t += '</tbody>\n</table>\n'
        flask.g.stash['table'] = t
        app.cache.set(html_key, t, 3600)

    return flask.render_template('session/timetable.tpl')

def _list_sessions(conference_id, status, lang, range_start=None, range_end=None):
    key = list_cache_key(conference_id, status, lang, range_start=range_start, range_end=range_end)
    conference_sessions = app.cache.get(key)
    if conference_sessions:
        return conference_sessions

    conference_sessions = flask.g.api.list_sessions(conference_id, lang=lang, status=status, range_start=range_start, range_end=range_end)
    if conference_sessions :
        app.cache.set(key, conference_sessions, LIST_EXPIRES)
        return conference_sessions
    return None

def list_cache_key(conference_id, status, lang, range_start=None, range_end=None):
    if not conference_id:
        raise Exception("faild to create conference cache key: no id")
    return "conference_sessions.%s.status.%s.lang.%s.%s.%s" % (conference_id, status, lang, range_start, range_end)

@page.route('/<series_slug>/<path:slug>/session/<id>')
@check_login
@with_conference_by_slug
@with_session
def view():
    return flask.render_template('v2017/session/view.html')

@page.route('/<series_slug>/<path:slug>/session/<id>/edit')
@require_login
@with_conference_by_slug
@functools.partial(with_session, lang='all')
@with_session_types
def edit():
    flask.g.stash['selected_session_type_id'] = flask.g.stash.get('session').get('session_type_id')

    return flask.render_template('v2017/session/edit.html')

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
    
    if flask.g.stash.get('errors'):
        errors = []
        for v in flask.g.stash['missing']:
            errors.append('Missing field %s' % v)
        flask.g.stash['errors'] = errors
        flask.g.stash['session'] = form
        return flask.render_template('v2017/session/edit.html')

    try:
        has_interpretation = False
        if form.get('has_interpretation'):
            has_interpretation =  True
        id = flask.g.stash.get('session').get('id')
        ok = flask.g.api.update_session(
            id                = id,
            abstract          = form.get('abstract'),
            session_type_id   = form.get('session_type_id'),
            title             = form.get('title'),
            category          = form.get('category'),
            material_level    = form.get('material_level'),
            memo              = form.get('memo'),
            photo_release     = form.get('photo_release'),
            recording_release = form.get('recording_release'),
            materials_release = form.get('materials_release'),
            slide_language    = form.get('slide_language'),
            spoken_language   = form.get('spoken_language'),
            slide_url         = form.get('slide_url'),
            video_url         = form.get('video_url'),
            has_interpretation = has_interpretation,
            **l10n
        )
        if ok:
            for l in app.LANGUAGES:
                app.cache.delete(app.hooks.session_cache_key(id=id, lang=l.get('value')))
            app.cache.delete(app.hooks.session_cache_key(id=id, lang='all'))
            return flask.redirect('/%s/session/%s' % (flask.g.stash.get('full_slug'), id))
        else:
            flask.g.stash["errors"] = [flask.g.api.last_error()]
    except BaseException as e:
        flask.g.stash["errors"] = [e]
        print(e)
        pass

    # XXX redirect to a proper location
    return flask.render_template('v2017/session/edit.html')

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
        token = "del_session_" + str(uuid.uuid4())
        flask.g.stash["delete_token"] = token
        flask.session[token] = dict(
            expires = time.time() + 900,
            id      = session.get('id')
        )
        return flask.render_template('v2017/session/delete.html')
    elif method == 'POST':
        token = flask.request.form.get('delete_token')
        data  = flask.session[token]
        if not data:
            return flask.abort(404)

        if data.get('id') != session.get('id'):
            return flask.abort(500)

        del flask.session[token]
        id = session.get('id')
        ok = flask.g.api.delete_session(id)
        if not ok:
            flask.g.stash["error"] = flask.g.api.last_error()
            return flask.render_template('v2017/session/delete.html')

        for l in app.LANGUAGES:
            app.cache.delete(app.hooks.session_cache_key(id=id, lang=l.get('value')))
        app.cache.delete(app.hooks.session_cache_key(id=id, lang='all'))
        return flask.redirect('/dashboard')
    else:
        return flask.abort(401)
        

@page.route('/<series_slug>/<path:slug>/session/confirm', methods=['GET'])
@require_login
@with_conference_by_slug
def show_confirm():
    # List sessions by the same speaker
    conference = flask.g.stash.get("conference")
    user = flask.g.stash.get("user")
    sessions = flask.g.api.list_sessions(
        conference_id=conference.get('id'),
        speaker_id=user.get('id'),
        lang=flask.g.lang,
        status="accepted",
        confirmed=False
    )
    flask.g.stash["sessions"] = sessions
    return flask.render_template('session/confirm.tpl')

@page.route('/<series_slug>/<path:slug>/session/<id>/confirm', methods=['POST'])
@require_login
@with_conference_by_slug
@with_session
def post_confirm():
    session = flask.g.stash.get("session")
    user = flask.g.stash.get('user')
    if user.get("id") != session.get("speaker_id"):
        flask.g.stash["error"] = "You are not the owner of this session"
        return flask.render_template('session/confirm.tpl')

    if session.get("status") != "accepted":
        flask.g.stash["error"] = "The specified session has not been accepted"
        return flask.render_template('session/confirm.tpl')
        

    ok = flask.g.api.update_session(
        id = session.get('id'),
        confirmed = True,
        user_id = user.get('id')
    )
    if not ok:
        flask.g.stash["error"] = flask.g.api.last_error()
        return flask.render_template('session/confirm.tpl')

    return flask.redirect('/%s/session/%s/confirmed' % (flask.g.stash.get('full_slug'), session.get('id')))

@page.route('/<series_slug>/<path:slug>/session/<id>/confirmed', methods=['GET'])
@with_conference_by_slug
@with_session
def confirmed():
    session = flask.g.stash.get('session')
    if session.get('id'):
        keys = app.cache.keys('*%s*' % session.get('id'))
        for key in keys:
            app.cache.delete(key)
    return flask.render_template('session/confirm_done.tpl')

