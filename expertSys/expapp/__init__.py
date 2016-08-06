# -*- coding:utf-8 -*-

from __future__ import absolute_import

from flask import Flask, g, render_template, send_from_directory, session, request, url_for
from flask_bootstrap import Bootstrap
import os
import os.path

from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import redirect
from flask_login import LoginManager, current_user, AnonymousUserMixin

from flask import Flask,render_template

app=Flask(__name__)
Bootstrap(app)

_basedir = os.path.abspath(os.path.dirname(__file__))
configPy=os.path.join(os.path.join( _basedir,os.path.pardir), 'config.py')

app.config.from_pyfile(configPy)

flask_sqlalchemy_used=True
db=SQLAlchemy(app)

login_manager=LoginManager(app)
login_manager.login_view= "users.showLogin"

from expapp.users.views import mod as usersModule
app.register_blueprint(usersModule,url_prefix='/users')

from expapp.users.models import User, Expert, Expert_Qualification, \
	Expert_Appraise_Experience, Expert_Working_Experience, Expert_Avoiding_Unit
db.create_all()

import expapp.users.views


#*****************
# controllers
#*****************

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'ico/favicon.ico')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route("/")
def index():
    return redirect(url_for('users.showLogin'))