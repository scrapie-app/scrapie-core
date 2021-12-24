from random import random
import math
# valid characters range from ascii 33 to 126
# exclude special characters 34, 39, 58, 59, 91-96
exclude_characters = [34, 39, 58, 59, 91, 92, 93, 94, 95, 96]

def generate_api_key(keyLength):
  if keyLength < 0:
    raise Exception("Invalid API Key length")
  api_key = ""
  while len(api_key) != keyLength:
    randomCharAscii = 33 + math.floor(93 * random())
    if randomCharAscii not in exclude_characters:
      api_key += chr(randomCharAscii)
  return api_key
