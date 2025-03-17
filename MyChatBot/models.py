from django.db import models

class Register(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    contact = models.CharField(max_length=20)
    email = models.EmailField()
    address = models.TextField()

    class Meta:
        db_table = 'register'
