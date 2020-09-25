from django.db import models

# Create your models here.
class User(models.Model):
    firstName = models.CharField(max_length = 20)
    lastName = models.CharField(max_length = 20)
    email = models.CharField(max_length = 50)
    username = models.CharField(max_length = 20)
    password = models.CharField(max_length = 20)

    def save(self, *args, **kwargs):
        super(myCustomUser, self).save(*args, **kwargs)
        profile = myCustomUser(user = self)
        profile.save()
        

