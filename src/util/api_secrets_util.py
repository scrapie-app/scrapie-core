from random import random
import math
# valid characters range from ascii 33 to 126
# exclude special characters 34, 39, 58, 59, 91-96
exclude_characters_set_one = [34, 39, 58, 59, 91, 92, 93, 94, 95, 96]
exclude_characters_set_two = [42, 43, 44, 45, 46, 47, 60, 61, 62, 63]
exclude_characters_all = exclude_characters_set_one + exclude_characters_set_two

def generate_secret(secret_name, exclude_characters=[], secret_length=0):
  if secret_length < 0:
        raise Exception(f'Invalid {secret_name} length')
  secret_key = ''
  while len(secret_key) != secret_length:
    random_char_ascii = 33 + math.floor(93 * random())
    if random_char_ascii not in exclude_characters:
      secret_key += chr(random_char_ascii)
  return secret_key

def generate_api_key(key_length):
  api_key = generate_secret('api key', exclude_characters_set_one, key_length)
  return api_key

def generate_bearer_token(token_length = 16):
  bearerToken = generate_secret('api key', exclude_characters_all, token_length)
  return bearerToken
