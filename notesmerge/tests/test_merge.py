import json
from ..merger.merger import Merger
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from typing import Dict




class MergeTests(APITestCase):
  def test_merge_different_strings(self):
    data_str = '{"inputs":{"1":{"id":13,"text":"aa"},"2":{"id":14,"text":"bb"}},"merge_options":{"porter_stemmer":true,"remove_stop_words":false,"alphanumeric_filter":false,"output_delimiter":"\\n\\n","numeric_filter":false,"lowercase":false,"input_delimiter":"\\n\\n","wordnet_lemmatizer":false,"alpha_filter":false}}'
    data  = json.loads(data_str)
    inputs = data['inputs']
    options = data['merge_options']
    merger = Merger(inputs, options)
    result = merger.merge()
    self.assertTrue(result["result"] == "aa\n\nbb" or
                        result["result"] == "bb\n\naa")

  def test_merge_same_strings(self):
    data_str = '{"inputs":{"1":{"id":13,"text":"aa"},"2":{"id":14,"text":"aa"}},"merge_options":{"porter_stemmer":true,"remove_stop_words":false,"alphanumeric_filter":false,"output_delimiter":"\\n\\n","numeric_filter":false,"lowercase":false,"input_delimiter":"\\n\\n","wordnet_lemmatizer":false,"alpha_filter":false}}'
    data  = json.loads(data_str)
    inputs = data['inputs']
    options = data['merge_options']
    merger = Merger(inputs, options)
    result = merger.merge()
    self.assertEqual(result["result"], "aa")

  def get_merge_result(self, data_str: str) -> Dict:
    data = json.loads(data_str)
    inputs = data['inputs']
    options = data['merge_options']
    merger = Merger(inputs, options)
    result = merger.merge()
    return result

  #only compare numic part of inputs
  def test_merge_numeric_filter(self):
    # aa22 and 22 filter to be the same string when numeric filter is applied
    # so only one will be in the result
    data_str = '{"inputs":{"1":{"id":13,"text":"aa22"},"2":{"id":14,"text":"33\\n\\n22"}},"merge_options":{"porter_stemmer":false,"remove_stop_words":false,"alphanumeric_filter":false,"output_delimiter":"\\n\\n","numeric_filter":true,"lowercase":false,"input_delimiter":"\\n\\n","wordnet_lemmatizer":false,"alpha_filter":false}}'
    result = self.get_merge_result(data_str)
    # any combination is valid
    self.assertTrue(result["result"] == "aa22\n\n33" or
                        result["result"] == "22\n\n33" or
                        result["result"] == "33\n\n22" or
                        result["result"] == "33\n\naa22")

  #  python manage.py test notesmerge.tests.test_merge.MergeTests.test_merge_alpha_filter
  def test_merge_alpha_filter(self):
    data_str = '{"inputs":{"1":{"id":13,"text":"aa22"},"2":{"id":14,"text":"bb\\n\\naa33"}},"merge_options":{"porter_stemmer":false,"remove_stop_words":false,"alphanumeric_filter":false,"output_delimiter":"\\n\\n","numeric_filter":false,"lowercase":false,"input_delimiter":"\\n\\n","wordnet_lemmatizer":false,"alpha_filter":true}}'
    result = self.get_merge_result(data_str)
    self.assertTrue(result["result"] == "aa22\n\nbb" or
                  result["result"] == "aa33\n\nbb" or
                  result["result"] == "bb\n\naa22" or
                  result["result"] == "bb\n\naa33")

  def test_merge_alphanumeric_filter(self):
    data_str = '{"inputs":{"1":{"id":13,"text":"aa,22"},"2":{"id":14,"text":"bb\\n\\naa22"}},"merge_options":{"porter_stemmer":false,"remove_stop_words":false,"alphanumeric_filter":true,"output_delimiter":"\\n\\n","numeric_filter":false,"lowercase":false,"input_delimiter":"\\n\\n","wordnet_lemmatizer":false,"alpha_filter":false}}'
    result = self.get_merge_result(data_str)
    self.assertTrue(result["result"] == "aa,22\n\nbb" or
                  result["result"] == "aa22\n\nbb" or
                  result["result"] == "bb\n\naa,22" or
                  result["result"] == "bb\n\naa22")

  def test_merge_porter_stemmer(self):
    data_str = '{"inputs":{"1":{"id":13,"text":"cat"},"2":{"id":14,"text":"cats\\n\\nword"}},"merge_options":{"porter_stemmer":true,"remove_stop_words":false,"alphanumeric_filter":false,"output_delimiter":"\\n\\n","numeric_filter":false,"lowercase":false,"input_delimiter":"\\n\\n","wordnet_lemmatizer":false,"alpha_filter":false}}'
    result = self.get_merge_result(data_str)
    self.assertTrue(result["result"] == "word\n\ncats" or
                  result["result"] == "word\n\ncat" or
                  result["result"] == "cats\n\nword" or
                  result["result"] == "cat\n\nword")

  def test_merge_wordnet_lemmatizer(self):
    data_str = '{"inputs":{"1":{"id":13,"text":"abaci"},"2":{"id":14,"text":"abacus\\n\\nword"}},"merge_options":{"porter_stemmer":false,"remove_stop_words":false,"alphanumeric_filter":false,"output_delimiter":"\\n\\n","numeric_filter":false,"lowercase":false,"input_delimiter":"\\n\\n","wordnet_lemmatizer":true,"alpha_filter":false}}'
    result = self.get_merge_result(data_str)
    self.assertTrue(result["result"] == "word\n\nabaci" or
                  result["result"] == "word\n\nabacus" or
                  result["result"] == "abaci\n\nword" or
                  result["result"] == "abacus\n\nword")

  def test_merge_remove_stop_words(self):
    data_str = '{"inputs":{"1":{"id":13,"text":"the dog"},"2":{"id":14,"text":"dog\\n\\nword"}},"merge_options":{"porter_stemmer":false,"remove_stop_words":true,"alphanumeric_filter":false,"output_delimiter":"\\n\\n","numeric_filter":false,"lowercase":false,"input_delimiter":"\\n\\n","wordnet_lemmatizer":false,"alpha_filter":false}}'
    result = self.get_merge_result(data_str)
    # removes "the" for the merge
    self.assertTrue(result["result"] == "word\n\nthe dog" or
                  result["result"] == "word\n\ndog" or
                  result["result"] == "the dog\n\nword" or
                  result["result"] == "dog\n\nword")

  def test_merge_output_delimiter(self):
    data_str = '{"inputs":{"1":{"id":13,"text":"the dog"},"2":{"id":14,"text":"dog\\n\\nword"}},"merge_options":{"porter_stemmer":false,"remove_stop_words":true,"alphanumeric_filter":false,"output_delimiter":"aa","numeric_filter":false,"lowercase":false,"input_delimiter":"\\n\\n","wordnet_lemmatizer":false,"alpha_filter":false}}'
    result = self.get_merge_result(data_str)
    self.assertTrue(result["result"] == "wordaathe dog" or
                  result["result"] == "wordaadog" or
                  result["result"] == "the dogaaword" or
                  result["result"] == "dogaaword")

  def test_do_merge_api(self):
    url = reverse('do_merge')
    data_str = '{"inputs":{"1":{"id":13,"text":"aa"},"2":{"id":14,"text":"bb"}},"merge_options":{"porter_stemmer":true,"remove_stop_words":false,"alphanumeric_filter":false,"output_delimiter":"\\n\\n","numeric_filter":false,"lowercase":false,"input_delimiter":"\\n\\n","wordnet_lemmatizer":false,"alpha_filter":false}}'
    response = self.client.post(url, data_str, content_type='application/json')
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertTrue(response.data["result"] == "aa\n\nbb" or
                        response.data["result"] == "bb\n\naa")

