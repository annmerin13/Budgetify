from django.db import models

# Create your models here.
class tbl_incometype(models.Model):
    incometype_name = models.CharField(max_length=30)
class tbl_expensetype(models.Model):
    expensetype_name = models.CharField(max_length=30)
class tbl_adminregistration(models.Model):
    admin_name = models.CharField(max_length=30)
    admin_email = models.EmailField(max_length=30)
    admin_password = models.CharField(max_length=30)
