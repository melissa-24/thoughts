from django.db import models
import re
from django.db.models.deletion import CASCADE

from django.db.models.fields.related import ForeignKey

class UserManager(models.Manager):
    def validate(self, form):
        errors = {}

        if len(form['firstName']) < 2:
            errors['firstName'] = 'First Name must contain at least 2 characters'

        if len(form['lastName']) < 2:
            errors['lastName'] = "Last Name must contain at least 2 characters"

        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(form['email']):
            errors['email'] = 'Invalid Email Address'

        emailCheck = self.filter(email=form['email'])
        if emailCheck:
            errors['email'] = 'Email Address already in use'

        if len(form['password']) < 8:
            errors['password'] = 'Password must be at least 8 characters'

        if form['password'] != form['confirm']:
            errors['password'] = 'Passwords do not match'

        return errors

class User(models.Model):
    firstName = models.CharField(max_length=45)
    lastName = models.CharField(max_length=45)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=45)

    objects = UserManager()

    userCreatedAt = models.DateTimeField(auto_now_add=True)
    userUpdatedAt = models.DateTimeField(auto_now=True)

class ThoughtManager(models.Manager):
    def val(self, form):
        errors = {}

        if len(form['thought']) < 5:
            errors['thought'] = 'Please have at least 5 characters for your thought'

        return errors

class Thought(models.Model):
    thought = models.TextField()
    poster = models.ForeignKey(User, related_name='users', on_delete=CASCADE)
    like = models.ManyToManyField(User, related_name='likes')
    thoughtAdded = models.DateTimeField(auto_now_add=True)
    thoughtUpdated = models.DateTimeField(auto_now=True)

    objects = ThoughtManager()