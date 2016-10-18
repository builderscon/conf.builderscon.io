import app
import flask

page = flask.Blueprint('root', __name__)

@page.route('/')
def index():
    key = "conferences.lang." + flask.g.lang

    conferences = app.cache.get(key)
    if not conferences:
        print 'app.api = %s' % app.api
        conferences = app.api.list_conference(lang=flask.g.lang)
        if conferences is None:
            return app.api.last_error(), 500
        app.cache.set(key, conferences, 600)

    return flask.render_template('index.tpl',
        pagetitle='top',
        conferences=conferences
    )

# Note: this has to come BEFORE other handlers
@page.route('/favicon.ico')
def favicon():
    flask.abort(404)

@page.route('/beacon')
def beacon():
    return flask.render_template('beacon.tpl')


