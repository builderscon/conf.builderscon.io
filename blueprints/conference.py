import app
import feedparser
import flask
import flasktools
import re
import time

page = flask.Blueprint('conference', __name__)
page.add_app_url_map_converter(flasktools.RegexConverter, 'regex')

with_conference_by_slug = app.hooks.with_conference_by_slug

# This route maps "latest" URLs to the actual latest conference
# URLs, so that we don't have to refer to "latest" elsewhere in 
# the code
@page.route('/<series_slug>/<regex("latest(/.*)?"):rest>')
def latest(series_slug, rest):
    latest_conference = _get_latest_conference(series_slug, flask.g.lang)
    if not latest_conference:
        raise ConferenceNotFoundError
    rest = re.compile('^latest').sub(latest_conference.get('slug'), rest)
    return flask.redirect("/" + series_slug + "/" + rest)


@page.route('/<series_slug>')
def conference(series_slug):
    return flask.redirect('/{0}/latest'.format(series_slug))

@page.route('/<series_slug>/<path:slug>')
@with_conference_by_slug
def view():
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

def latest_conference_cache_key(series_slug):
    if not series_slug:
        raise Exception("faild to create conference cache key: no series_slug")
    return "conference.latest.%s" % series_slug

def _get_latest_conference(series_slug, lang):
    key = latest_conference_cache_key(series_slug)
    cid = app.cache.get(key)
    if cid:
        return _get_conference(id=cid, lang=lang)

    # XXX There should be a specific API call for this
    conferences = app.api.list_conference(lang=lang)
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


