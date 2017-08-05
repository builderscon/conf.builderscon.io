import babel
import builderscon
import flasktools
import iso8601
import markdown
import markupsafe
import mdx_gfm
import model
import oauth
import oembed
import pytz
import re

OEMBED_EXPIRES = 3600
SESSION_SLIDE_EMBED_EXPIRES = 3600
SESSION_VIDEO_EMBED_EXPIRES = 3600
SESSION_THUMBNAIL_URL_EXPIRES = 3600

oembed_consumer = oembed.OEmbedConsumer()
oembed_endpoints = [
    [ 'https://www.youtube.com/oembed', [ 'https://*.youtube.com/*' ] ],
    [ 'http://www.slideshare.net/api/oembed/2', [ 'http://www.slideshare.net/*' ] ],
    [ 'http://speakerdeck.com/oembed.json', [ 'https://speakerdeck.com/*' ], ],
]
for ent in oembed_endpoints:
    e = oembed.OEmbedEndpoint(*ent)
    oembed_consumer.addEndpoint(e)

@builderscon.app.template_filter('video_id')
def video_id(url):
    mobj = re.search(r'youtube\.com/watch\?v=(.+)', url, flags=re.UNICODE)
    if mobj:
        return mobj.group(1)
    return ''

def video_oembed(url, **opt):
    key = 'oembed.%s.%s' % (url, opt)
    o = flasktools.urlparse(url)
    if re.search(r'youtube\.com$', o.netloc, flags=re.UNICODE):
        if 'maxwidth' not in opt:
            opt['maxwidth'] = 600
        if 'maxheight' not in opt:
            opt['maxheight'] = 480
        res = oembed_consumer.embed(url, **opt)
        builderscon.cache.set(key, res, OEMBED_EXPIRES)
        return res
    return None

def slide_oembed(url, **opt):
    key = 'oembed.%s.%s' % (url, opt)
    o = flasktools.urlparse(url)
    if re.search(r'(slideshare\.net|speakerdeck\.com)$', o.netloc, flags=re.UNICODE):
        try:
            res = oembed_consumer.embed(url)
            builderscon.cache.set(key, res, OEMBED_EXPIRES)
            return res
        except:
            print(traceback.format_exc())
            return None

    return None

@builderscon.app.template_filter('session_thumbnail_url')
def session_thumbnail_url(session):
    key = "session.thumbnail_url.%s" % session.get('id')
    thumb = builderscon.cache.get(key)
    if thumb:
        return thumb

    if session.get('video_url'):
        res = video_oembed(session.get('video_url'))
        url = res['thumbnail_url']
        if url:
            builderscon.cache.set(key, url, SESSION_THUMBNAIL_URL_EXPIRES)
            return url

    if session.get('slide_url'):
        res = slide_oembed(session.get('slide_url'))
        if not res:
            return None
        url = res.get('thumbnail_url')
        if url:
            builderscon.cache.set(key, url, SESSION_THUMBNAIL_URL_EXPIRES)
            return url
 
    return None

@builderscon.app.template_filter('video_embed')
def video_embed(url, **opt):
    key = "session.video.embed.html.%s" % url
    html = builderscon.cache.get(key)
    if html:
        return html

    res = video_oembed(url, **opt)
    if res:
        html = res['html']
        builderscon.cache.set(key, html, SESSION_VIDEO_EMBED_EXPIRES)
        return html
    html = '<a href="%s">%s</a>' % (url, url)
    builderscon.cache.set(key, html, SESSION_VIDEO_EMBED_EXPIRES)
    return html

@builderscon.app.template_filter('slide_embed')
def slide_embed(url, **opt):
    key = "session.slide.embed.html.%s" % url
    html = builderscon.cache.get(key)
    if html:
        return html

    o = flasktools.urlparse(url)
    if re.search(r'^docs\.google\.com$', o.netloc, flags=re.UNICODE):
        url = re.sub(r'/pub\?', '/embed?', url)
        o = flasktools.urlparse(url)
        q = flasktools.parse_qsl(o.query)
        q.append(('width', 400))
        html = '<iframe src="%s" frameborder="0" width="500" height="450"allowfullscreen="true" mozallowfullscreen="true" webkitallowfullscreen="true"></iframe>' % flasktools.urlunparse(o)
        builderscon.cache.set(key, html, SESSION_SLIDE_EMBED_EXPIRES)
        return html

    res = slide_oembed(url, **opt)
    if res:
        html = res['html']
        builderscon.cache.set(key, html, SESSION_SLIDE_EMBED_EXPIRES)
        return html

    html = '<a href="%s">%s</a>' % (url, url)
    builderscon.cache.set(key, html, SESSION_SLIDE_EMBED_EXPIRES)
    return html

@builderscon.app.template_filter('confdate')
def conference_date_filter(s, lang='en', timezone='UTC'):
    return model.ConferenceDate(s, lang=lang, timezone=timezone)

markdown_converter = markdown.Markdown(extensions=[mdx_gfm.GithubFlavoredMarkdownExtension()]).convert
@builderscon.app.template_filter('markdown')
def markdown_filter(s):
    return markdown_converter(s)

@builderscon.app.template_filter('audlevelname')
def audience_level_value_to_name(v):
    if not v:
        return ''
    return v.title()

# Used in templates, when all you have is the user's input value
@builderscon.app.template_filter('langname')
def lang_value_to_name(v):
    for l in builderscon.LANGUAGES:
        if l.get('value') == v:
            return l.get('name')
    return ""

# Used in templates, when all you have is the user's input value
@builderscon.app.template_filter('permname')
def permission_value_to_name(v):
    return v.title()

@builderscon.app.template_filter('is_oauth_error')
def is_oauth_error(v):
    return type(v) is oauth.Error

@builderscon.app.template_filter('urlencode')
def urlencode_filter(s):
    if type(s) == 'Markup':
        s = s.unescape()
    s = s.encode('utf8')
    s = flasktools.quote_plus(s)
    return markupsafe.Markup(s)

@builderscon.app.template_filter('dateobj')
def dateobj(s, timezone='UTC'):
    localtz = pytz.timezone(timezone)
    return iso8601.parse_date(s).astimezone(localtz)

@builderscon.app.template_filter('datefmt')
def datefmt(dt, locale, tzinfo, format='short'):
    return babel.dates.format_datetime(dt, tzinfo=tzinfo, locale=locale, format=format)

