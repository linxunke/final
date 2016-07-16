import os
basedir = os.path.abspath(os.path.dirname(__file__))

CSRF_ENABLED = True
SECRET_KEY = 'secret'
MAX_SEARCH_RESULTS = 50
OPENID_PROVIDERS = [

    { 'name': 'Yahoo', 'url': 'https://me.yahoo.com' }
]
if os.environ.get('DATABASE_URL') is None:
    SQLALCHEMY_DATABASE_URI = ('sqlite:///' + os.path.join(basedir, 'app.db') +
                               '?check_same_thread=False')
else:
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
SQLALCHEMY_RECORD_QUERIES = True
WHOOSH_BASE = os.path.join(basedir, 'search.db')

MAX_SEARCH_RESULTS = 50

