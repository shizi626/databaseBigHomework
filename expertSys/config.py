# -*- coding: utf-8 -*-

from __future__ import absolute_import
import os
from datetime import timedelta

_basedir = os.path.abspath(os.path.dirname(__file__))


SQLALCHEMY_TRACK_MODIFICATIONS = True
DEBUG = True
TESTING = True
SECRET_KEY = os.urandom(24)
PERMANENT_SESSION_LIFETIME=timedelta(seconds=24*60*60)
CSRF_ENABLED = True
CSRF_SESSION_KEY=SECRET_KEY

VALIDATETIMEINSECOND=158112000 # 5 YEARS

IMGPATH='expapp/static/'

DB_USER = 'root'
DB_PASSWORD = 'nicai@690!?'
DB_URI = 'localhost:3306/expapp'
SQLALCHEMY_DATABASE_URI = 'mysql://' + DB_USER + ':' + DB_PASSWORD + '@' + DB_URI+'?charset=utf8'
