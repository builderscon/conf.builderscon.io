import builderscon
import markdown
import markupsafe
import mdx_gfm
import model
import flasktools

@builderscon.app.template_filter('dateobj')
def dateobj_filter(s, lang='en', timezone='UTC'): # note: this is probably going to be deprecated
    return model.ConferenceDate(s, lang=lang, timezone=timezone)

markdown_converter = markdown.Markdown(extensions=[mdx_gfm.GithubFlavoredMarkdownExtension()]).convert
@builderscon.app.template_filter('markdown')
def markdown_filter(s):
    return markdown_converter(s)

@builderscon.app.template_filter('audlevelname')
def audience_level_value_to_name(v):
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


