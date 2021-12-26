with open ('commands_and_descriptions.txt') as commands_and_descriptions:
    lines = commands_and_descriptions.readlines()

print(lines)

API_KEY = open('api_key.txt', 'r').read()
print(API_KEY)

