# Currently not being used 5/12/21
from django.db import models

# Create your models here.
class GuiSetup(models.Model):
    num_hosts = models.IntegerField()
    num_switches = models.IntegerField()
    num_controllers = models.IntegerField()
