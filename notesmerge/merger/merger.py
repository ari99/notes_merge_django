from .token_converter import TokenConverter
from .merger_options  import MergerOptions
from typing import List, Dict

'''
  Performs the merge across inputs.
'''
class Merger():

  def __init__(self, inputs: Dict, merger_options: Dict):
    self.inputs = inputs
    self.merger_options = MergerOptions(merger_options)

  def merge(self) -> Dict:
    token_lists = self.create_token_lists()
    tokens = self.merge_lists(token_lists)
    result_dictionary = self.merge_tokens(tokens)
    return result_dictionary

  '''
    Splits the inputs into an array of lists tokens.
  '''
  def create_token_lists(self) -> List[List[str]]:
    token_lists = []
    for key,value in self.inputs.items():
      text = value['text']
      tokens = text.split(self.merger_options.input_delimiter)
      stripped_tokens = list(map(lambda s: s.strip(), tokens))
      token_lists.append(stripped_tokens)
    return token_lists

  '''
    Combines the array of lists of tokens into an array of tokens.
  '''
  def merge_lists(self, token_lists: List[List[str]]) -> List[str]:
    merge_result = []
    converted_merge_result = []
    token_converter = TokenConverter(self.merger_options)
    for tokens in token_lists:
      for token in tokens:
        converted_token = token_converter.convert_token(token)
        if converted_token and converted_token not in converted_merge_result:
          converted_merge_result.append(converted_token)
          merge_result.append(token)
    return merge_result

  '''
    Combines all tokens into a single result using merger_options.output_delimiter.
  '''
  def merge_tokens(self, tokens: List[str]) -> Dict[str, str]:
    result = {"result": str.join(self.merger_options.output_delimiter, tokens)}
    return result



