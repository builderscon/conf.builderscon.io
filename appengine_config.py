import os
import sys

from google.appengine.ext import vendor

vendor.add('lib')

# Fix for msvcrt import error https://github.com/gae-init/gae-init/pull/527
# Otherwise, GAE local dev server fails at "import msvcrt" in "click" package
if os.name == 'nt':
    os.name = None
    sys.platform = ''