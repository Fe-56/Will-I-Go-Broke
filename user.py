# this file is to store the User class, where it stores all the information that the user enters via /plan

class User:
    def __init__(self, name):
        self._name = name

    @property
    def name(self):
        return self._name