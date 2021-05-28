from django.db import models


class Results(models.Model):
    Alpha = models.FloatField()
    Beta = models.FloatField()
    Mental_state = models.CharField(max_length=20)
    