from random import random
import math
# valid characters range from ascii 33 to 126

def generate_api_key(keyLength):
  if keyLength < 0:
    raise Exception("Invalid API Key length")
  api_key = ""
  for i in range(0, keyLength):
    randomChar = chr(33 + math.floor(93 * random()))
    api_key += randomChar
  return api_key
