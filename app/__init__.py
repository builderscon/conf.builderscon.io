import builderscon
import os

if os.getenv('CONFIG_FILE') is None:
    p = os.path.join(os.path.dirname(__file__), '..', 'config.json')
    os.environ['CONFIG_FILE'] = os.path.normpath(p)

builderscon.initialize()

import hooks
import filters
import logging
import oauth # always load AFTER builderscon.initialize
import requestlogger
import sys

# silence pyflakes
assert hooks
assert filters

api = builderscon.api
app = requestlogger.WSGILogger(builderscon.app, [
    logging.StreamHandler(sys.stdout)], 
    requestlogger.ApacheFormatter()
)
cache = builderscon.cache
cfg = builderscon.cfg
LANGUAGES = builderscon.LANGUAGES

def github_oauth():
    return oauth.start(oauth.github, builderscon.app.base_url + '/login/github/callback')

def facebook_oauth():
    return oauth.start(oauth.facebook, builderscon.app.base_url + '/login/facebook/callback')

def twitter_oauth():
    return oauth.start(oauth.twitter, builderscon.app.base_url + '/login/twitter/callback')

github_oauth_callback = oauth.github_callback
facebook_oauth_callback = oauth.facebook_callback
twitter_oauth_callback = oauth.twitter_callback
