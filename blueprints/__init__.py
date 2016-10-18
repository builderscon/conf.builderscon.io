import flask

def add_app_url_map_converter(self, func, name=None):
    def register_converter(state):
        state.app.url_map.converters[name or func.__name__] = func
    self.record_once(register_converter)

flask.Blueprint.add_app_url_map_converter = add_app_url_map_converter

import auth
import cfp
import conference
import root
import session
import user

# silence pyflakes
assert auth
assert cfp
assert conference
assert root
assert session
assert user
