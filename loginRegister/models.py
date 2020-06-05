from django.db import models
import re

class userManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

        if not EMAIL_REGEX.match(postData['email']):       
            errors['email'] = "Invalid email address!"
        if len(postData['fname']) < 2:
            errors["fname"] = "First Name should be at least 2 characters"
        if len(postData['lname']) < 2:
            errors["lname"] = "Lirst Name should be at least 2 characters"
        if len(postData['pwd']) < 8:
            errors["pwd_length"] = "Password Must be 10 character long"
        if postData['pwd'] != postData['confirm_pwd']:
            errors["pwd"] = "Password Do Not Match"
        return errors

class user(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.CharField(max_length=45)
    password = models.CharField(max_length=80)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = userManager()

class message(models.Model):
    content = models.TextField()
    User = models.ForeignKey(user, related_name="messages", on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class comment(models.Model):
    content = models.TextField()
    Message = models.ForeignKey(message, related_name="comments", on_delete = models.CASCADE)
    User = models.ForeignKey(user, related_name="comments", on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    