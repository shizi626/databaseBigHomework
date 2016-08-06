# -*- coding: utf-8 -*-

from flask_wtf import Form
from wtforms import StringField,BooleanField,PasswordField,SelectField,SubmitField
from wtforms.validators import DataRequired, EqualTo, Length, InputRequired

class LoginForm(Form):
	"""docstring for LoginForm"""
	
	role=SelectField(u'角色选择：',choices=[('0',u'用户'),('1',u'管理员')])
	loginUsername=StringField(u'用户名：',validators=[DataRequired()])
	password=PasswordField(u'密码：',validators=[DataRequired()])
	login_button=SubmitField(u'登录')
		

class RegisteringForm(Form):
	"""docstring for RegisteringForm"""
	
	regUsername=StringField(u'用户名：',validators=[Length(min=5,max=20)])
	password=PasswordField(u'密码：',validators=[Length(min=6,max=20)])
	confirm=PasswordField(u'密码确认：',validators=[EqualTo('password',message=u'两次输入的密码不同，请重新输入！')])
	reg_button=SubmitField(u'注册')


class ChangePsw(Form):
	"""docstring for ChangePsw"""
	
	oldpsw=PasswordField(u'旧密码：',validators=[Length(min=6,max=20)])
	newpsw=PasswordField(u'新密码：',validators=[Length(min=6,max=20,message=u'密码长度必须为6-20个字符！')])
	confirm=PasswordField(u'密码确认：',validators=[EqualTo('newpsw',message=u'两次输入的密码不同，请重新输入！')])
	ok_button=SubmitField(u'确认')