from rest_framework import serializers
from .models.merge import Merge
from .models.merge_options import MergeOptions
from .models.input import Input
from typing import Dict

from django.contrib.auth.models import User


class MergeOptionsSerializer(serializers.ModelSerializer):

  def create(self, validated_data: Dict):
    return MergeOptionsSerializer(**validated_data)

  class Meta:
    model = MergeOptions
    fields = ( 'input_delimiter', 'output_delimiter', 'remove_stop_words',
                'porter_stemmer', 'wordnet_lemmatizer', 'lowercase',
                'alphanumeric_filter', 'alpha_filter', 'numeric_filter')


class InputSerializer(serializers.ModelSerializer):
  #http://stackoverflow.com/questions/36473795/django-rest-framework-model-id-field-in-nested-relationship-serializer
  id = serializers.ModelField(model_field=Input()._meta.get_field('id'), required=False)
  text = serializers.CharField(max_length=2000, required=False, allow_blank=True)
  def create(self, validated_data):
    return InputSerializer(**validated_data)

  class Meta:
    model = Input
    fields = ('text','id')


class MergeSerializer(serializers.ModelSerializer):
  owner = serializers.ReadOnlyField(source='owner.username')
  merge_options = MergeOptionsSerializer()
  inputs = InputSerializer(many=True, required=False)
  
  def create(self, validated_data: Dict) -> Merge:
    merge_options_data = validated_data.pop('merge_options')
    inputs_data = validated_data.pop('inputs')
    merge = Merge.objects.create(**validated_data)
    merge_options = MergeOptions.objects.create(merge=merge, **merge_options_data)
    #Create input objects
    for input_data in inputs_data:
      Input.objects.create(merge=merge, **input_data)

    return merge

  '''
    Updates a Merge instance and the associated MergeOptions and Input.
  '''
  def update(self, instance: Merge, validated_data: Dict) -> Merge:
    merge_options_data = validated_data.pop('merge_options')
    merge_options = instance.merge_options
    self.update_merge_options(merge_options, merge_options_data)

    instance.name = validated_data.get('name', instance.name)
    instance.result = validated_data.get('result', instance.result)
    instance.save()

    request_inputs_data = validated_data.pop('inputs')
    instance = self.update_input(request_inputs_data, instance)

    return instance

  '''
    Update Input.
  '''
  def update_input(self, request_inputs_data, instance: Merge):
    request_ids= []
    # If the Input already exists in the db update it, otherwise create an Input instance.
    for request_input in request_inputs_data:
      input_id = request_input.get('id', None)
      if input_id:
        request_ids.append(input_id)
        input_instance = Input.objects.get(id=input_id, merge=instance)
        input_instance.text = request_input.get('text', input_instance.text)
        input_instance.save()
      else:
        new_input = Input.objects.create(merge=instance, **request_input)
        request_ids.append(new_input.id)

      for instance_input in instance.inputs.all():
        if instance_input.id not in request_ids:
          instance_input.delete()

    return instance

  '''
    Update MergeOptions.
  '''
  def update_merge_options(self, merge_options, merge_options_data):
    # http://stackoverflow.com/questions/37240621/django-rest-framework-updating-nested-object
    merge_options.input_delimiter = merge_options_data.get('input_delimiter', merge_options.input_delimiter)
    merge_options.output_delimiter = merge_options_data.get('output_delimiter', merge_options.output_delimiter)
    merge_options.remove_stop_words = merge_options_data.get('remove_stop_words', merge_options.remove_stop_words)
    merge_options.porter_stemmer = merge_options_data.get('porter_stemmer', merge_options.porter_stemmer)
    merge_options.wordnet_lemmatizer = merge_options_data.get('wordnet_lemmatizer', merge_options.wordnet_lemmatizer)
    merge_options.lowercase = merge_options_data.get('lowercase', merge_options.lowercase)
    merge_options.alphanumeric_filter = merge_options_data.get('alphanumeric_filter', merge_options.alphanumeric_filter)
    merge_options.alpha_filter = merge_options_data.get('alpha_filter', merge_options.alpha_filter)
    merge_options.numeric_filter = merge_options_data.get('alpha_filter', merge_options.numeric_filter)
    merge_options.save()

  class Meta:
    model = Merge
    fields = ('id','created', 'name', 'result', 'owner', 'merge_options', 'inputs')





class UserSerializer(serializers.ModelSerializer):
  merges = serializers.PrimaryKeyRelatedField(many=True, queryset=Merge.objects.all(), required=False)
  #https://github.com/tomchristie/django-rest-framework/issues/3736
    
  class Meta:
    model = User
    fields = ('id', 'username', 'password', 'merges')
    write_only_fields = ('password',)
    read_only_fields = ('id',)

  def create(self, validated_data: Dict) -> User:
    user = User(username=validated_data['username'])
    user.set_password(validated_data['password'])
    user.save()
    return user
