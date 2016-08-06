# -*- coding: utf-8 -*-

from flask_login import UserMixin
from sqlalchemy.orm import relationship

from expapp import db

class User(db.Model,UserMixin):
	"""docstring for User"""
	
	__tablename__='user'
	username=db.Column(db.String(20),primary_key=True)
	password=db.Column(db.String(256))
	userType=db.Column(db.Boolean)

	expert=relationship("Expert", back_populates="user")
	expert_quali=relationship("Expert_Qualification", back_populates="user")
	expert_app_exp=relationship("Expert_Appraise_Experience", back_populates="user")
	expert_work_exp=relationship("Expert_Working_Experience", back_populates="user")
	expert_avoid_unit=relationship("Expert_Avoiding_Unit", back_populates="user")

	# for flask_login--user class
	def is_authenticated(self):
		return True

	def is_active(self):
		return True

	def is_anonymous(self):
		return False

	def get_id(self):
		return unicode(self.username)

	def save(self):
		db.session.add(self)
		db.session.commit()


class Expert(db.Model):
	"""docstring for Expert"""
	__tablename__="Expert"

	username=db.Column(db.String(20),db.ForeignKey(User.username), primary_key=True)

	expCertificateID=db.Column(db.String(20),unique=True)
	verifyState=db.Column(db.String(10))
	verifyStateReason=db.Column(db.String(600))
	certificateValidTime=db.Column(db.Date)

	expName=db.Column(db.String(20))
	expSex=db.Column(db.String(2))
	expPhoto=db.Column(db.String(50)) # for image url
	birthday=db.Column(db.Date)
	politicalStatus=db.Column(db.String(10))

	IDType=db.Column(db.String(10))
	authority=db.Column(db.String(50))
	IDNumber=db.Column(db.String(50))

	highestSchooling=db.Column(db.String(10))
	highestDegree=db.Column(db.String(10))
	title=db.Column(db.String(10))
	titleID=db.Column(db.String(50))
	expjob=db.Column(db.String(10))
	workingLength=db.Column(db.String(10))
	isRetired=db.Column(db.String(2))
	isPart_time=db.Column(db.String(2))
	expworkingUnit=db.Column(db.String(50))
	address=db.Column(db.String(100))
	zipcode=db.Column(db.String(50))

	email=db.Column(db.String(50))
	mobilePhone=db.Column(db.String(20))
	homePhone=db.Column(db.String(20))

	graduateSchool=db.Column(db.String(50))
	appraisefield1=db.Column(db.String(50))
	appraisefield2=db.Column(db.String(50))

	skill=db.Column(db.String(600))
	achievements=db.Column(db.String(600))
	otherDesc=db.Column(db.String(600))

	isSubmitted=db.Column(db.Boolean)

	user=relationship("User",back_populates="expert")

	def save(self):
		db.session.add(self)
		db.session.commit()


class Expert_Qualification(db.Model):

	__tablename__="ExpertQualification"

	username=db.Column(db.String(20),db.ForeignKey(User.username), primary_key=True)
	qualificationID=db.Column(db.String(50), primary_key=True)
	qualificationName=db.Column(db.String(20))

	user=relationship("User",back_populates="expert_quali")

	def save(self):
		db.session.add(self)
		db.session.commit()
		

class Expert_Appraise_Experience(db.Model):

	__tablename__="ExpertAppraiseExperience"

	username=db.Column(db.String(20),db.ForeignKey(User.username), primary_key=True)
	time=db.Column(db.Date,primary_key=True)
	appraiseName=db.Column(db.String(20),primary_key=True)
	appraiseDesc=db.Column(db.String(100))
	appraiseType=db.Column(db.String(20))

	user=relationship("User",back_populates="expert_app_exp")

	def save(self):
		db.session.add(self)
		db.session.commit()


class Expert_Working_Experience(db.Model):

	__tablename__="ExpertWorkingExperience"

	username=db.Column(db.String(20),db.ForeignKey(User.username), primary_key=True)
	startTime=db.Column(db.Date,primary_key=True)
	endTime=db.Column(db.Date,primary_key=True)
	workingUnit=db.Column(db.String(50),primary_key=True)
	job=db.Column(db.String(20))
	referee=db.Column(db.String(20))

	user=relationship("User",back_populates="expert_work_exp")

	def save(self):
		db.session.add(self)
		db.session.commit()


class Expert_Avoiding_Unit(db.Model):

	__tablename__="ExpertAvoidingUnit"

	username=db.Column(db.String(20),db.ForeignKey(User.username), primary_key=True)
	unitName=db.Column(db.String(50),primary_key=True)
	isWorkingUnit=db.Column(db.String(2))

	user=relationship("User",back_populates="expert_avoid_unit")

	def save(self):
		db.session.add(self)
		db.session.commit()

	
# the class manager isn't established now