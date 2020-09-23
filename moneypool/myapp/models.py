from django.db import models

# Create your models here.
class Profile(models.Model):
    firstName = models.CharField(max_length = 20)
    lastName = models.CharField(max_length = 20)

    def save(self, *args, **kwargs):
        super(myCustomUser, self).save(*args, **kwargs)
        profile = myCustomUser(user = self)
        profile.save()
        

