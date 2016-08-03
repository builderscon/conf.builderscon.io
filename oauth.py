import flask
import flasktools
import json
import random
import string

random_src_chars = string.ascii_letters + string.digits
def random_string(n):
    s = ''
    for i in range(n):
        s += random.choice(random_src_chars)
    return s

class OAuthResult(object):
    def __init__(self, redirect='', error='', userinfo=''):
        self.redirect = redirect
        self.error = error
        self.userinfo = userinfo

    def is_redirect(self):
        return not not self.redirect

    def is_error(self):
        return not not self.error


class OAuth2(object):
    def __init__(self, http, auth_via, access_token_url, authorize_url, userinfo_url, redirect_uri, client_id, client_secret, scope=["user"]):
        self.http = http
        self.auth_via = auth_via
        self.access_token_url = access_token_url
        self.authorize_url = authorize_url
        self.client_id = client_id
        self.client_secret = client_secret
        self.userinfo_url = userinfo_url
        self.redirect_uri = redirect_uri
        self.scope = scope
        self.error = None

    def extract_userinfo(self, h):
        return h

    def make_headers(self, **extra):
        h=extra
        h["User-Agent"] = 'python/urrlib3/0.6'
        return h

    def redirect_authorize_url(self, state):
        qs = flasktools.urlencode({
            'client_id': self.client_id,
            'scope': ' '.join(self.scope),
            'state': state,
            'redirect_uri': self.redirect_uri,
        })
        return OAuthResult(redirect='%s?%s' % (self.authorize_url, qs))

    def fetch_access_token(self, code, state):
        qs = flasktools.urlencode({
            'code': code,
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'redirect_uri': self.redirect_uri,
            'state': state
        })
        hdrs = self.make_headers(Accept='application/json')
        res = self.http.request('GET', '%s?%s' % (self.access_token_url, qs), headers=hdrs)
        if res.status != 200:
            print(res.data)
            self.error = OAuthResult(
                error='failed to exchange access token',
                redirect='/login?.error=failed+to+acquire+token'
            )
            return None

        h = json.loads(res.data)
        if not h:
            self.error = OAuthResult(
                error='failed to parse access token',
            )
            return None
        return h["access_token"]

    def fetch_userinfo(self, token, state):
        qs = flasktools.urlencode({
            'state': state,
            'access_token': token
        })
        hdrs = self.make_headers()
        res = self.http.request('GET', '%s?%s' % (self.userinfo_url, qs), headers=hdrs)
        if res.status != 200:
            print(res.data)
            self.error = OAuthResult(
                error='failed to get userinfo',
                redirect='/login?.error=failed+to+acquire+userinfo'
            )
            return None
        h = json.loads(res.data)
        if not h:
            self.error = OAuthResult(
                error='failed to parse userinfo',
            )
            return None

        return self.extract_userinfo(h)

    def handle_auth(self):
        code = flask.request.args.get('code')
        state = random_string(64)
        if not code:
            return self.redirect_authorize_url(state)

        token = self.fetch_access_token(code, state)
        if self.error:
            return self.error

        userinfo = self.fetch_userinfo(token, state)
        if self.error:
            return self.error

        return OAuthResult(userinfo=userinfo)

class Github(OAuth2):
    def __init__(self, http, cfg):
        super(Github, self).__init__(
            http=http,
            auth_via='github',
            authorize_url='https://github.com/login/oauth/authorize',
            access_token_url='https://github.com/login/oauth/access_token',
            redirect_uri='https://builderscon.io/login/github',
            userinfo_url='https://api.github.com/user',
            client_id=cfg["client_id"],
            client_secret=cfg["client_secret"]
        )

    def extract_userinfo(self, h):
        return {
            'auth_via': self.auth_via,
            'nickname': h.get('login', h.get('name', "No name")),
            'name': h.get('name', h.get('login', "No name")),
            'email': h.get('email')
        }

class Facebook(OAuth2):
    def __init__(self, http, cfg):
        super(Facebook, self).__init__(
            http=http,
            auth_via='facebook',
            authorize_url='https://www.facebook.com/dialog/oauth',
            access_token_url='https://graph.facebook.com/v2.3/oauth/access_token',
            redirect_uri='https://builderscon.io/login/facebook',
            userinfo_url='https://graph.facebook.com/me',
            scope=["email"],
            client_id=cfg["client_id"],
            client_secret=cfg["client_secret"]
        )

    def extract_userinfo(self, h):
        return {
            'auth_via':self.auth_via,
            'remote_id': h.get("id"),
            'nickname': h.get("username", h.get("name", "No Name")),
            'name': h.get("name", h.get("username", "No Name")),
            'email': h.get("email"),
        }

class Twitter(OAuth2):
    def __init__(self, http, cfg):
        super(Twitter, self).__init__(
            http=http,
            auth_via='twitter',
            authorize_url='https://api.twitter.com/oauth/request_token',
            access_token_url='https://api.twitter.com/oauth/access_token',
            redirect_uri='https://builderscon.io/login/twitter',
            userinfo_url='https://api.twitter.com/1.1/account/verify_credentials.json',
            client_id=cfg["client_id"],
            client_secret=cfg["client_secret"]
        )

    def extract_userinfo(self, h):
        return {
            'auth_via': self.auth_via,
            'remote_id': h.get('id'),
            'nickname': h.get('screen_name'),
            'name': h.get('name')
        }

