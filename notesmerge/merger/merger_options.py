from typing import Dict

'''
  Class to hold and provide defaults for merge options.
'''
class MergerOptions():
  INPUT_DELIMITER = 'input_delimiter'
  OUTPUT_DELIMITER = 'output_delimiter'
  REMOVE_STOP_WORDS = 'remove_stop_words'
  PORTER_STEMMER = 'porter_stemmer'
  WORDNET_LEMMATIZER = 'wordnet_lemmatizer'
  LOWERCASE = 'lowercase'
  ALPHANUMERIC_FILTER = 'alphanumeric_filter'
  ALPHA_FILTER = 'alpha_filter'
  NUMERIC_FILTER = 'numeric_filter'

  def __init__(self, options: Dict):
    self.options = options

  @property
  def input_delimiter(self) -> str:
    return self.default_on_empty(
              self.options[MergerOptions.INPUT_DELIMITER], "\n\n")

  @property
  def output_delimiter(self) -> str:
    return self.default_on_empty(
            self.options[MergerOptions.OUTPUT_DELIMITER], "\n\n")

  @property
  def remove_stop_words(self) -> str:
    return self.default_on_empty(
            self.options[MergerOptions.REMOVE_STOP_WORDS], False)

  @property
  def porter_stemmer(self) -> str:
    return self.default_on_empty(
            self.options[MergerOptions.PORTER_STEMMER], False)

  @property
  def wordnet_lemmatizer(self) -> str:
    return self.default_on_empty(
        self.options[MergerOptions.WORDNET_LEMMATIZER], False)

  @property
  def lowercase(self) -> str:
    return self.default_on_empty(
            self.options[MergerOptions.LOWERCASE], False)

  @property
  def alphanumeric_filter(self) -> str:
    return self.default_on_empty(
            self.options[MergerOptions.ALPHANUMERIC_FILTER], False)

  @property
  def alpha_filter(self) -> str:
    return self.default_on_empty(
            self.options[MergerOptions.ALPHA_FILTER], False)

  @property
  def numeric_filter(self) -> str:
    return self.default_on_empty(
            self.options[MergerOptions.NUMERIC_FILTER], False)

  def default_on_empty(self, value : str, default : str) -> str:
    if not value:
      return default
    else:
      return value