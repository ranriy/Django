from django.db import models
import bcrypt
import re
from datetime import date
from time import strftime


email_regex = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')

class UserManager(models.Manager):
	def registration_validator(self, postData):
		print(postData)
		errors = {}
		if(len(postData['name']) < 2):
			errors['name'] = "Name should have atleat 2 characters"
		if(len(postData['alias']) < 2):
			errors['alias'] = "Alias should have atleat 2 characters"
		if(not re.match(email_regex,postData['email'])):
			errors['email'] = "Invalid Email"
		if len(self.filter(email = postData['email'])) != 0:
			errors['repeat'] = "Email already exists"
		if(len(postData['password']) < 8):
			errors['password'] = "Passwords must have atleat 8 character"
		if postData['password'] != postData['cpassword']:
			errors['mismatch'] = "passwords donot match"
		if postData['dob'] > date.today().strftime("%Y-%m-%d"):
			errors['birthday'] = "Date of Birth cannot be in future"
		if len(errors)==0:
			userpassword = postData['password']
			userpassword = userpassword.encode('utf-8')
			hashpw = bcrypt.hashpw(userpassword, bcrypt.gensalt()) 
			return hashpw
		return errors
	def login_validator(self, postData):
		errors ={}
		if(len(self.filter(email = postData['email'])) == 0):
			errors['noemail'] = "Email doesnot exists"
		else:
			u = self.filter(email = postData['email'])[0]
			userpassword = postData['password']
			if not bcrypt.checkpw(userpassword.encode('utf-8'), u.password.encode()):
				errors['password'] = "Incorrect password"
		if(len(errors) != 0):
			return errors
		return self.filter(email = postData['email'])[0]


class User(models.Model):
	name = models.CharField(max_length=100)
	alias = models.CharField(max_length=100)
	email = models.EmailField()
	password = models.CharField(max_length=255)
	dob = models.DateField()
	friend_of = models.ManyToManyField('self', related_name = "friend_to")
	objects = UserManager()

