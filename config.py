SECRET_KEY = '\xe2\xe7A\x92\xcftl\@\xb3\xc8\x83\xc4\xad\xe9'

import os
basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

OIDC_CLIENT_SECRETS = './client_secrets.json'
OIDC_ID_TOKEN_COOKIE_SECURE = False
OIDC_ID_TOKEN_COOKIE_NAME = 'oidc_id_token'
OIDC_ID_TOKEN_COOKIE_TTL = 60

ADMIN_EMAIL = 'idfumg@gmail.com'
