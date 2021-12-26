# with open ('commands_and_descriptions.txt') as commands_and_descriptions:
#     lines = commands_and_descriptions.readlines()

# print(lines)

# API_KEY = open('api_key.txt', 'r').read()
# print(API_KEY)

import os
dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, 'Data/api_key.txt')
API_KEY = open(filename, 'r').read()
print(API_KEY)