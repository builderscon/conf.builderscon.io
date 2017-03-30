import app
import datetime
import flask
import pytz

page = flask.Blueprint('root', __name__)

@page.route('/')
def index():
    # Fetch conferences that are coming soon, and fetch conferences
    # that have been.

    # First, conferences that are coming soon.
    today = datetime.datetime.utcnow().replace(
        hour=0,
        minute=0,
        second=0,
        microsecond=0,
        tzinfo=pytz.utc
    )
    key = 'conferences.after.%s.lang.%s' % (today.strftime('%Y-%m-%d'), flask.g.lang)
    conferences = app.cache.get(key)
    if not conferences:
        conferences = flask.g.api.list_conference(
            range_start=today.strftime('%Y-%m-%d'),
            lang=flask.g.lang
        )
        if conferences is None:
            conferences = []
        app.cache.set(key, conferences, 86400)
    flask.g.stash['upcoming_conferences'] = conferences

    # Next, old conferences
    key = 'conferences.before.%s.lang.%s' % (today.strftime('%Y-%m-%d'), flask.g.lang)
    conferences = app.cache.get(key)
    if not conferences:
        conferences = flask.g.api.list_conference(
            range_start=today.replace(year=today.year - 1).strftime('%Y-%m-%d'),
            range_end=today.strftime('%Y-%m-%d'),
            lang=flask.g.lang
        )
        if conferences is None:
            conferences = []
        app.cache.set(key, conferences, 86400)
    flask.g.stash['past_conferences'] = conferences
    flask.g.stash['pagetitle'] = 'top'

    print(flask.g.stash.get('upcoming_conferences'))
    print(flask.g.stash.get('past_conferences'))
    return flask.render_template('index.tpl')

# Note: this has to come BEFORE other handlers
@page.route('/favicon.ico')
def favicon():
    flask.abort(404)

@page.route('/beacon')
def beacon():
    return flask.render_template('beacon.tpl')


