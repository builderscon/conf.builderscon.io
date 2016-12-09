import app
import feedparser
import flask
import flasktools
import re
import time

page = flask.Blueprint('conference', __name__)
page.add_app_url_map_converter(flasktools.RegexConverter, 'regex')

with_conference_by_slug = app.hooks.with_conference_by_slug
with_latest_conference = app.hooks.with_latest_conference

# This route maps "latest" URLs to the actual latest conference
# URLs, so that we don't have to refer to "latest" elsewhere in 
# the code
@page.route('/<series_slug>/<regex("latest(/.*)?"):rest>')
@with_latest_conference
def latest(rest):
    conference = flask.g.stash.get('conference')
    if conference is None:
        return flask.abort(404)
    rest = re.compile('^latest').sub(flask.g.stash.get('slug'), rest)
    return flask.redirect('/%s/%s' % (flask.g.stash.get('series_slug'), rest))


@page.route('/<series_slug>')
def conference(series_slug):
    return flask.redirect('/{0}/latest'.format(series_slug))

@page.route('/<series_slug>/<path:slug>')
@with_conference_by_slug
def view():
    key = "staff.%s.%s" % (flask.g.stash.get('conference_id'), flask.g.lang)
    staff = app.cache.get(key)
    if not staff:
        staff = app.api.list_conference_staff(
            conference_id=flask.g.stash.get('conference_id'),
            lang=flask.g.lang
        )
        if staff:
            app.cache.set(key, staff, 600)
    flask.g.stash['staff'] = staff
    return flask.render_template('conference/view.tpl',
        googlemap_api_key=app.cfg.googlemap_api_key())

@page.route('/<series_slug>/<path:slug>/sponsors')
@with_conference_by_slug
def sponsors():
    return flask.render_template('sponsors.tpl')

@page.route('/<series_slug>/<path:slug>/news')
@with_conference_by_slug
def news():
    key = "news_entries.lang." + flask.g.lang
    news_entries = app.cache.get(key)
    if not news_entries:
        feed_url = 'http://blog.builderscon.io/feed.xml'
        news = feedparser.parse(feed_url)
        if not news.entries:
            return 'Failed to get news from Atom feed = %, check if the feed is generated there.' % feed_url, 500
        news_entries = news.entries
        app.cache.set(key, news.entries, 600)

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

@page.route('/<series_slug>/<path:slug>/schedule.ics')
@with_conference_by_slug
def schedule_ics():
    conference = flask.g.stash.get('conference')
    key = "scheule-ics.%s.%s" % (conference.get('id'), flask.g.lang)
    ics = app.cache.get(key)
    if ics:
        return flask.Response(ics, 200, {'Content-Type': 'text/calendar'})

    if not app.api.get_conference_schedule(conference.get('id')):
        return "failed to fetch schedule", 500

    ics = app.api.last_response().data
    app.cache.set(key, ics, 300)
    return flask.Response(ics, 200, {'Content-Type': 'text/calendar'})


@page.route('/<series_slug>/<path:slug>/feedback/blogs')
@with_conference_by_slug
def feedback_blogs():
    key = "blog_entries.%s.%s" % (flask.g.stash.get('conference_id'), flask.g.lang)
    blog_entries = app.cache.get(key)
    if not blog_entries:
        blog_entries = app.api.list_blog_entries(
            conference_id=flask.g.stash.get('conference_id'),
            lang=flask.g.lang,
            status=['public']
        )
        if not blog_entries:
            flask.abort(500, "failed to fetch blog entries")
            return
        app.cache.set(key, blog_entries, 600)

    flask.g.stash['blog_entries'] = blog_entries or [];
    return flask.render_template('conference/blogs.tpl')

@page.route('/<series_slug>/<path:slug>/staff')
@with_conference_by_slug
def staff():
    key = "staff.%s.%s" % (flask.g.stash.get('conference_id'), flask.g.lang)
    staff = app.cache.get(key)
    if not staff:
        staff = app.api.list_conference_staff(
            conference_id=flask.g.stash.get('conference_id'),
            lang=flask.g.lang
        )
        if staff is None:
            flask.abort(500, "failed to fetch staff")
            return
        app.cache.set(key, staff, 600)

    flask.g.stash['staff'] = staff or [];
    return flask.render_template('conference/staff.tpl')


