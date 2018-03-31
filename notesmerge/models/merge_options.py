from django.db import models
from .merge import Merge

'''
  MergeOptions model.
'''
class MergeOptions(models.Model):
  input_delimiter = models.CharField(max_length=100, blank=True, default='\n\n')
  output_delimiter = models.CharField(max_length=100, blank=True, default='\n\n')
  remove_stop_words = models.BooleanField(default=False)
  porter_stemmer = models.BooleanField(default=False)
  wordnet_lemmatizer = models.BooleanField(default=False)
  lowercase = models.BooleanField(default=False)
  alphanumeric_filter = models.BooleanField(default=False)
  alpha_filter = models.BooleanField(default=False)
  numeric_filter = models.BooleanField(default=False)
  merge = models.OneToOneField(
        Merge,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name="merge_options"
  )