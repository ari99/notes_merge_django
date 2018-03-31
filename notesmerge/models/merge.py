from django.db import models

'''
  Merge model.
'''
class Merge(models.Model):
  created = models.DateTimeField(auto_now_add=True)
  name = models.CharField(max_length=100, blank=True, default='')
  result = models.TextField(blank=True)
  owner = models.ForeignKey('auth.User', related_name='merges', on_delete=models.CASCADE, default=1)

  def __str__(self):
    return '%s' % (self.name)

  class Meta:
    ordering = ('created',)