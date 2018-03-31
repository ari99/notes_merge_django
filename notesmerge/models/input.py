from django.db import models
from .merge import Merge

'''
  Input model.
'''
class Input(models.Model):
  text = models.TextField(blank=True)
  merge = models.ForeignKey(Merge, related_name='inputs', on_delete=models.CASCADE)
