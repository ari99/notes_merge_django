from nltk.corpus import stopwords
import nltk
from .merger_options import MergerOptions
from typing import List

'''
  Converts an individual token to a new form based on merge options.
'''
class TokenConverter():
  def __init__(self, merger_options: MergerOptions):
    self.merger_options = merger_options

  def convert_token(self, original_token: str) -> str:
    token = self.convert_string(original_token)
    tokens = nltk.word_tokenize(token)

    tokens = self.convert_list(tokens)
    combined = ''.join(tokens) #maybe join with a space
    return combined

  def convert_list(self, tokens: List[str]) -> List[str]:
    if self.merger_options.remove_stop_words:
      tokens = self.remove_stop_words(tokens)

    if self.merger_options.porter_stemmer:
      tokens = self.porter_stemmer(tokens)

    if self.merger_options.wordnet_lemmatizer:
      tokens = self.wordnet_lemmatizer(tokens)

    return tokens

  def convert_string(self, token: str) -> str:
        
    if self.merger_options.lowercase:
      token = token.lower()
    # to include spaces : list(filter(lambda x: x.isalnum() or x.isspace(), token))
    if self.merger_options.alphanumeric_filter:
      token = ''.join(filter(str.isalnum, token))

    if self.merger_options.alpha_filter:
      token = ''.join(filter(str.isalpha, token))

    if self.merger_options.numeric_filter:
      token = ''.join(filter(str.isdigit, token))

    return token

  def remove_stop_words(self, tokens: List[str]) -> List[str]:
    filtered_token = [word for word in tokens if word not in stopwords.words('english')]
    return filtered_token

  def porter_stemmer(self, tokens: List[str]) -> List[str]:
    porter = nltk.PorterStemmer()
    ported = [porter.stem(token) for token in tokens]
    return ported

  def wordnet_lemmatizer(self, tokens: List[str]) -> List[str]:
    wnl = nltk.WordNetLemmatizer()
    lemmatized = [wnl.lemmatize(t) for t in tokens]
    return lemmatized

