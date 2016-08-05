import flask_oauth

oauth = flask_oauth.OAuth()
def Init(name, **args):
    v = oauth.remote_app(name, **args)
    return v
