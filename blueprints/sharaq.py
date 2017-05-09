import flask

page = flask.Blueprint('sharaq', __name__)

@page.route('/sharaq/<preset>/<path:url>')
def sharaq(preset, url):
    url = url.replace('?', '%3F')
    return flask.redirect('https://sharaq-dot-builderscon-1248.appspot.com/?preset=%s&url=%s' % (preset, url))


