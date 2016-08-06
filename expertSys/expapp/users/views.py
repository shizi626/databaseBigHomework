# -*- coding: utf-8 -*-

import os
import time
import random
import json
from flask import Blueprint, Flask, request, session, g, redirect, url_for, abort, render_template, flash
from sqlalchemy import or_
from flask_login import login_user, login_required, logout_user, current_user

import getcaptcha
from expapp import app,db,login_manager
from form import LoginForm,RegisteringForm,ChangePsw
from models import User,Expert,Expert_Qualification,Expert_Appraise_Experience,\
					Expert_Working_Experience,Expert_Avoiding_Unit
from config import VALIDATETIMEINSECOND,IMGPATH

mod = Blueprint('users', __name__) #register the users blueprint module

# for login manager
@login_manager.user_loader
def load_user(userid):
	return User.query.filter(User.username==userid).first()


# for views
@mod.route('/login',methods=['GET','POST'])
def showLogin():
	form=LoginForm(request.form)
	if request.method=='GET':
		return render_template('login.html',form=form)
	if request.method=='POST':
		user=User.query.filter(User.username==form.loginUsername.data,\
			User.password==form.password.data, User.userType==form.role.data).first()

		if user!=None:
			login_user(user)
			flash(u'登录成功')
			if form.role.data=='0':
				return redirect(url_for("users.showRegIndex"))
			return redirect(url_for("users.mngrindex"))
		else:
			flash(u'用户名或者密码错误！')
			return render_template('login.html',form=form)
	return render_template('login.html',form=form)

@mod.route('/logout')
@login_required
def logout():
	logout_user()
	return redirect(url_for('users.showLogin'))


@mod.route('/register',methods=['GET','POST'])
def showReg():
	form=RegisteringForm(request.form)
	if request.method=='GET':
		return render_template('register.html',form=form)
	if request.method=='POST':
		if form.validate_on_submit():
			user=User()
			user.username=form.regUsername.data
			print user.username
			if user.query.filter(User.username==user.username).first():
				err=u'已存在此用户名'
				flash(err,"error")
				return render_template('register.html',form=form)
			user.password=form.password.data
			user.userType=0

			db.session.add(user)
			db.session.commit()
			logout_user()
			flash(u'注册成功，请重新登录！')
			return redirect(url_for('users.showLogin'))
	return render_template('register.html',form=form)


@mod.route('/regindex')
@login_required
def showRegIndex():
	expName=current_user.username
	expert=Expert.query.filter(Expert.username==expName).first()
	expState =None
	reason=None
	if expert is not None:
		expState=expert.verifyState
		reason=expert.verifyStateReason
	return render_template("regindex.html",expState=expState,reason=reason)


@mod.route('/regtable')
@login_required
def showRegTable():
	expName=current_user.username
	expert=Expert.query.filter(Expert.username==expName).first()
	if expert is None:
		expert=Expert()
		expert.username=expName
		expert.save()
	expQuali = Expert_Qualification.query.filter(Expert_Qualification.username == expName).all()
	expAppraiseExp = Expert_Appraise_Experience.query.filter(Expert_Appraise_Experience.username == expName).all()
	expWorkExp = Expert_Working_Experience.query.filter(Expert_Working_Experience.username == expName).all()
	expAvoid = Expert_Avoiding_Unit.query.filter(Expert_Avoiding_Unit.username == expName).all()

	return render_template("regtable.html",expert=expert,expQuali = expQuali,expAppraiseExp = expAppraiseExp,
	                       expWorkExp = expWorkExp,expAvoid = expAvoid)

@mod.route('/expGetInfo')
@login_required
def expGetInfo():
	expName=current_user.username
	expert = Expert.query.filter(Expert.username == expName).first()
	expert.__dict__['_sa_instance_state'] = ''
	if (expert.__dict__['birthday'] != None):
		expert.__dict__['birthday'] = expert.__dict__['birthday'].isoformat()
	if (expert.__dict__['certificateValidTime'] != None):
		expert.__dict__['certificateValidTime'] = expert.__dict__['certificateValidTime'].isoformat()
	return json.dumps(expert.__dict__)


@mod.route('/regtable/saveInfo',methods=['GET','POST'])
@login_required
def savaInfo():
	expUserName=current_user.username
	expert=Expert.query.filter(Expert.username==expUserName).first()
	if expert is None:
		expert=Expert()

	expert.verifyState = u'填写中'

	expert.username=expUserName
	expert.expName=request.values.get('expName')
	expert.expSex=request.values.get('expSex')
	# expert.expPhoto=???
	if (request.values.get("birthday") == ""):
		expert.birthday = "1900-01-01"
	else:
		expert.birthday=request.values.get('birthday')
	expert.politicalStatus=request.values.get('politicalStatus')

	expert.IDType=request.values.get('IDType')
	expert.authority=request.values.get('authority')
	expert.IDNumber=request.values.get('IDNumber')

	expert.highestSchooling=request.values.get('highestSchooling')
	expert.highestDegree=request.values.get('highestDegree')
	expert.title=request.values.get('title')
	expert.titleID=request.values.get('titleID')
	expert.expjob=request.values.get('expjob')
	expert.workingLength=request.values.get('workingLength')
	expert.isRetired=request.values.get('isRetired')
	expert.isPart_time=request.values.get('isPart_time')
	expert.expworkingUnit=request.values.get('expworkingUnit')
	expert.address=request.values.get('address')
	expert.zipcode=request.values.get('zipcode')

	expert.email=request.values.get('email')
	expert.mobilePhone=request.values.get('mobilePhone')
	expert.homePhone=request.values.get('homePhone')

	expert.graduateSchool=request.values.get('graduateSchool')

	expert.skill=request.values.get('skill')
	expert.achievements=request.values.get('achievements')
	expert.otherDesc=request.values.get('otherDesc')

	expert.save()
	return 'ok'


@mod.route('/regtable/submitInfo',methods=['GET','POST'])
@login_required
def submitInfo():
	expName=current_user.username
	expert=Expert.query.filter(Expert.username==expName).first()
	expert.isSubmitted=True
	expert.verifyState=u'审核中'
	expert.save()
	return 'ok'

@mod.route('/regtable/addQualification/')
@login_required
def addQualification():
	expName=current_user.username
	expertQ=Expert_Qualification.query.filter(Expert_Qualification.username==expName,\
		Expert_Qualification.qualificationID==request.values.get('qualificationID')).first()
	if expertQ:
		return 'exist'
	else:
		expertQ=Expert_Qualification(username=expName,qualificationID=request.values.get('qualificationID'),\
			qualificationName=request.values.get('qualificationName'))
		expertQ.save()
	return ''
	

@mod.route('/regtable/delQualification/')
@login_required
def delQualification():
	expName=current_user.username
	expertQ=Expert_Qualification.query.filter(Expert_Qualification.username==expName,\
		Expert_Qualification.qualificationID==request.values.get('qualificationID')).first()
	db.session.delete(expertQ)
	db.session.commit()
	return ''


@mod.route('/regtable/addAppraiseField/')
@login_required
def addAppraiseField():
	expName = current_user.username
	field1=request.values.get('appraisefield1')
	field2 = request.values.get('appraisefield2')
	expert = Expert.query.filter(Expert.username == expName).first()
	expert.appraisefield1=field1
	expert.appraisefield2=field2
	expert.save()
	return 'ok'

@mod.route('/regtable/addAppraiseExperience/')
@login_required
def addAppraiseExperience():
	expName=current_user.username
	expertAP=Expert_Appraise_Experience.query.filter(Expert_Appraise_Experience.username==expName,\
		Expert_Appraise_Experience.time==request.values.get('time'),\
		Expert_Appraise_Experience.appraiseName==request.values.get('appraiseName')).first()
	if expertAP is not None:
		return 'exist'
	else:
		expertAP=Expert_Appraise_Experience(username=expName,time=request.values.get('time'),\
			appraiseName=request.values.get('appraiseName'),\
			appraiseDesc=request.values.get('appraiseDesc'),\
			appraiseType=request.values.get('appraiseType'))
		expertAP.save()

		return 'ok'


@mod.route('/regtable/delAppraiseExperience/')
@login_required
def delAppraiseExperience():
	expName=current_user.username
	expertAE=Expert_Appraise_Experience.query.filter(Expert_Appraise_Experience.username==expName,\
		Expert_Appraise_Experience.time==request.values.get('time'),\
		Expert_Appraise_Experience.appraiseName==request.values.get('appraiseName')).first()

	db.session.delete(expertAE)
	db.session.commit()
	return 'ok'


@mod.route('/regtable/addWorkingExperience/')
@login_required
def addWorkingExperience():
	expName=current_user.username
	expertWE=Expert_Working_Experience.query.filter(Expert_Working_Experience.username==expName,\
		Expert_Working_Experience.startTime==request.values.get('startTime'),\
		Expert_Working_Experience.endTime==request.values.get('endTime'),\
		Expert_Working_Experience.workingUnit==request.values.get('workingUnit')).first()
	if expertWE is not None:
		return 'exist'
	else:
		expertWE=Expert_Working_Experience(username=expName,startTime=request.values.get('startTime'),\
			endTime=request.values.get('endTime'),workingUnit=request.values.get('workingUnit'),\
			job=request.values.get('expjob'),referee=request.values.get('referee'))
		expertWE.save()
		return 'ok'

@mod.route('/regtable/delWorkingExperience/')
@login_required
def delWorkingExperience():
	expName=current_user.username
	expertWE=Expert_Working_Experience.query.filter(Expert_Working_Experience.username==expName,\
		Expert_Working_Experience.startTime==request.values.get('startTime'),\
		Expert_Working_Experience.endTime==request.values.get('endTime'),\
		Expert_Working_Experience.workingUnit==request.values.get('workingUnit')).first()
	db.session.delete(expertWE)
	db.session.commit()
	return 'ok'

@mod.route('/regtable/addAvoidingUnit/')
@login_required
def addAvoidingUnit():
	expName=current_user.username
	expertAU=Expert_Avoiding_Unit.query.filter(Expert_Avoiding_Unit.username == expName, \
	                                           Expert_Avoiding_Unit.unitName == request.values.get('unitName')).first()
	if expertAU is not None:
		return 'exist'
	else:
		expertAU=Expert_Avoiding_Unit(username=expName,unitName=request.values.get('unitName'), \
		                              isWorkingUnit=request.values.get('isWorkingUnit'))
		expertAU.save()
		return 'ok'

@mod.route('/regtable/delAvoidingUnit/')
@login_required
def delAvoidingUnit():
	expName=current_user.username
	expertAU=Expert_Avoiding_Unit.query.filter(Expert_Avoiding_Unit.username == expName, \
	                                           Expert_Avoiding_Unit.unitName == request.values.get('unitName')).first()
	db.session.delete(expertAU)
	db.session.commit()
	return 'ok'

@mod.route('/editpsw',methods=['GET','POST'])
@login_required
def editpsw():
	form=ChangePsw(request.form)
	if request.method=="GET":
		return render_template("editpsw.html",form=form)
	if request.method=="POST":
		if form.validate_on_submit():
			expName = current_user.username
			oldpsw = request.values.get('oldpsw')
			newpsw = request.values.get('newpsw')
			user = User.query.filter(User.username == expName,User.password == oldpsw).first()
			if user is None:
				flash(u'密码错误！')
				return redirect(url_for('users.editpsw',form=form))
			else:
				user.password = newpsw
				user.save()
				logout_user()
				flash(u"成功修改密码，请重新登录")
				return redirect(url_for('users.showLogin'))
		return render_template("editpsw.html",form=form)
	return render_template("editpsw.html",form=form)


@mod.route('/mngrindex')
@login_required
def mngrindex():
	number=len(Expert.query.filter(Expert.verifyState==u"审核中").all())
	return render_template("mngrindex.html",number=number)

@mod.route('/searchexp',methods=['GET','POST'])
@login_required
def showsearch():
	expList=[]
	if request.method == "GET":
		for one in Expert.query.filter().all():
			expList.append({'username':one.username,'expCertificateID': one.expCertificateID,'expName': one.expName,'workingUnit': one.expworkingUnit, 'mobilePhone': one.mobilePhone,'type': u'注册','verifyState': one.verifyState})

	if request.method=="POST":
		field=request.values.get('field')
		status=request.values.get('status')
		if field=='' and status=='':
			for one in Expert.query.filter().all():
				expList.append({'username':one.username,'expCertificateID':one.expCertificateID,'expName':one.expName,'workingUnit':one.expworkingUnit,	'mobilePhone':one.mobilePhone,'type':u'注册','verifyState':one.verifyState})

		if field!='' and status=='':
			for one in Expert.query.filter(or_(Expert.appraisefield1==field,Expert.appraisefield2==field)).all():
				expList.append({'username':one.username,'expCertificateID':one.expCertificateID,'expName':one.expName,'workingUnit':one.expworkingUnit,'mobilePhone':one.mobilePhone,'type':u'注册','verifyState':one.verifyState})

		if field=='' and status!='':
			for one in Expert.query.filter(Expert.verifyState==status).all():
				expList.append({'username':one.username,'expCertificateID':one.expCertificateID,'expName':one.expName,'workingUnit':one.expworkingUnit,'mobilePhone':one.mobilePhone,'type':u'注册','verifyState':one.verifyState})

		if field!='' and status!='':
			for one in Expert.query.filter(Expert.verifyState==status).filter(or_(Expert.appraisefield1==field,Expert.appraisefield2==field)).all():
				expList.append({'username':one.username,'expCertificateID':one.expCertificateID,'expName':one.expName,'expworkingUnit':one.expworkingUnit,'mobilePhone':one.mobilePhone,'type':u'注册','verifyState':one.verifyState})

		return json.dumps(expList)

	return render_template('searchexp.html',expList = expList)

@mod.route('/admin/expinfo/<expname>',methods=['GET','POST'])
@login_required
def admin_expInfo(expname):
	expName=expname
	print expName
	expert=Expert.query.filter(Expert.username==expName).first()
	expQuali=Expert_Qualification.query.filter(Expert_Qualification.username==expName).all()
	expAppraiseExp=Expert_Appraise_Experience.query.filter(Expert_Appraise_Experience.username==expName).all()
	expWorkExp=Expert_Working_Experience.query.filter(Expert_Working_Experience.username==expName).all()
	expAvoid=Expert_Avoiding_Unit.query.filter(Expert_Avoiding_Unit.username == expName).all()
	return render_template("expinfo.html",expert=expert,expQuali=expQuali,expAppraiseExp=expAppraiseExp,expWorkExp=expWorkExp,expAvoid=expAvoid)


@mod.route('/expinfo/agreeExpert',methods=['GET','POST'])
@login_required
def agreeExpert():
	expert=Expert.query.filter(Expert.username==request.values.get('username')).first()
	expert.verifyState=u'可用'
	expert.verifyStateReason=''
	expert.expCertificateID='zj'+time.strftime("%Y%m%d")+str(random.randint(0,999999))
	vt=time.localtime(time.time()+VALIDATETIMEINSECOND)
	expert.certificateValidTime=time.strftime('%Y-%m-%d',vt)
	expert.save()

	return json.dumps({"certificate":expert.expCertificateID,"validTime":time.strftime('%Y-%m-%d',vt)})


@mod.route('/expinfo/denyExpert',methods=['GET','POST'])
@login_required
def denyExpert():
	expert=Expert.query.filter(Expert.username==request.values.get('username')).first()
	expert.verifyState=u'被驳回'
	expert.verifyStateReason=request.values.get('verifyStateReason')
	expert.save()

	return ''


@mod.route('/expinfo/stopExpert',methods=['GET','POST'])
@login_required
def stopExpert():
	expert=Expert.query.filter(Expert.username==request.values.get('username')).first()
	expert.verifyState=u'被终止'
	expert.verifyStateReason=request.values.get('verifyStateReason')
	expert.save()

	return ''
