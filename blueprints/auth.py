import app
import flask

page = flask.Blueprint('auth', __name__)

@page.route('/logout', methods=['POST'])
def logout(p=None):
    flask.session.clear()
    return flask.redirect('/')

@page.route('/login')
def login():
    return flask.render_template('login.tpl',
        next_url=flask.request.args.get('.next')
    )

@page.route('/login/github')
def github():
    return app.github_oauth()

@page.route('/login/github/callback')
def github_callback():
    return app.github_oauth_callback()

@page.route('/login/facebook')
def facebook():
    return app.facebook_oauth()

@page.route('/login/facebook/callback')
def facebook_callback():
    return app.facebook_oauth_callback()

@page.route('/login/twitter')
def twitter():
    if 'twitter_token' in flask.session:
        del flask.session['twitter_token']
    return app.twitter_oauth()

@page.route('/login/twitter/callback')
def twitter_callback():
    return app.twitter_oauth_callback()


