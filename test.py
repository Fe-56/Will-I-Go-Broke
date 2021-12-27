# this file is just for testing purposes with no link at all to the actual code

import os
dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, 'Data/api_key.txt')
API_KEY = open(filename, 'r').read()
print(API_KEY)

from user import User

hello = User('John')
print(hello.name)

import plan

print(plan.hello('hi'))