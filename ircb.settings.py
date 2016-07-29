import os
from ircb.config.default_settings import *

DB_URI = 'sqlite:///' + os.path.join(
    os.path.dirname(__file__), 'webapp/ircb.db')
