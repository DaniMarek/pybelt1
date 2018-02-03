from __future__ import unicode_literals
from django.db import models
import re
import bcrypt

EMAIL_REGEX=re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')

class UserManager(models.Manager):
	def reggie_validation(self, POSTdata):
		errors = []
		if len(POSTdata['first_name']) < 2:
			errors.append('first name must be more than 2 characters')
		if len(POSTdata['last_name']) < 2:
			errors.append('last name must be more than 2 characters')
		if len(POSTdata['password']) < 2:
			errors.append('password must be more than 2 characters')
		if POSTdata['password'] != POSTdata['password_confirmation']:
			errors.append('passwords must match!')
		if re.match(EMAIL_REGEX, POSTdata['email']):
			if len(POSTdata['email']) < 11:
				errors.append('not a valid email address!')
		if not re.match(EMAIL_REGEX, POSTdata['email']):
			errors.append('not a valid email address!')
		return errors

	def login_validation(self, POSTdata):
		errors = []
		user = User.objects.filter(email=POSTdata['email']).first()

		if re.match(EMAIL_REGEX, POSTdata['email']):
			if len(POSTdata['email']) < 11:
				errors.append('not a valid email address!')
		if not re.match(EMAIL_REGEX, POSTdata['email']):
			errors.append('not a valid email address!')
		if len(POSTdata['password']) < 2:
			errors.append('incorrect password')
		if user:
			user_password = POSTdata['password'].encode()
			db_password = user.password.encode()
			if bcrypt.checkpw(user_password, db_password):
				return {'user':user}
		return {'errors':errors}

		return errors
		
	def create_user(self, POSTdata):
		hashedpw = bcrypt.hashpw(POSTdata['password'].encode(), bcrypt.gensalt())
		return User.objects.create(
			first_name = POSTdata['first_name'],
			last_name = POSTdata['last_name'],
			email = POSTdata['email'],
			password = hashedpw,
			)

class QuoteManager(models.Manager):
	def quote_validation(self, POSTdata):
		errors = []
		if len(POSTdata['author']) < 3:
			errors.append('author name must be more than 3 characters')
		if len(POSTdata['quote']) < 10:
			errors.append('quote must be more than 10 characters')
		return errors

	def create_quote(self, POSTdata):
		return Quote.objects.create(
	  		author = POSTdata['author'],
			quote = POSTdata['quote'],
	  		)
	# def add_fave(self, POSTdata):
	# 	Quote.objects.favorite.add('POSTdata')

class User(models.Model):
  first_name = models.CharField(max_length=255)
  last_name = models.CharField(max_length=255)
  email = models.CharField(max_length=255)
  password = models.CharField(max_length=255)

  objects=UserManager()

  def __unicode__(self):
  	return  'first_name:{}, last_name:{}, email:{}, password:{}, id:{}'.format(self.first_name, self.last_name, self.email, self.password, self.id)

class Quote(models.Model):
  author = models.CharField(max_length=255)
  quote = models.TextField(max_length=255)
  user = models.ForeignKey(User, related_name="user")
  favorite = models.ManyToManyField(User, related_name="faves")
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  objects=QuoteManager()

  def __unicode__(self):
  	return  'author:{}, quote:{}, favorite:{}, id:{}, user:{}'.format(self.author, self.quote, self.favorite, self.id, self.user)