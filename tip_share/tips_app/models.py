from django.db import models
import re
from datetime import date
from django.db.models.deletion import CASCADE

from django.db.models.fields.related import ForeignKey
    
# Create your models here.
class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9.+_-]+\.[a-zA-Z]+$')
        users = User.objects.all()
        if len(postData['first_name']) < 2:
            errors['first_name'] = 'First name must be at least 2 characters'
        if len(postData['last_name']) < 2:
            errors['last_name'] = 'Last name must be at least 2 characters'
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = 'Invalid email address'
        for user in users:
            if (postData ['email']) == user.email:
                errors['email'] = 'Email already exists'
        for user in users:
            if (postData ['username']) == user.username:
                errors['username'] = 'User already exists'
        if (postData ['pass_confirm']) != (postData ['password']):
            errors['pass_confirm'] = 'Passwords must match'
        return errors

    def login_validator(self, postData):
        errors = {}
        if len(postData['username']) < 1:
            errors['username'] = 'Please enter a username'
        user = User.objects.filter(username = (postData ['username']))
        if not user:
            errors['username'] = 'Username not yet registered'
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    restaurant = models.CharField(max_length=255)
    hours_worked = models.CharField(max_length=255)
    tips = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # related fields
    # pool_group = models.ManyToManyField
    # groups = models.ManyToManyField
    # objects
    objects = UserManager()

# Working on profile picture
    # class ImageField(FileField):
        # attr_class = ImageFieldFile
        # descriptor_class = ImageFileDescriptor
        # description = _("Image")
    
class Transaction(models.Model):
    amount = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # related fields
    # user who is sending processing the transaction (one-to-one)
    sender = models.CharField(max_length=255)
    # users who will recieve the transaction (one-to-many)
    recipients = models.ForeignKey(User, related_name="recipients", on_delete=CASCADE)
    # I gotta play around with this, I feel like I'm missing something with the relationships.