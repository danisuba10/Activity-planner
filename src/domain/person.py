import random

class Person:

    def __init__(self, name:str, phone_number:str):
        self.__id = str(random.randint(1000000, 9999999))
        self.__name = name
        self.__phone_number = phone_number

    def get_id(self):
        return self.__id

    def set_id(self, id):
        self.__id = id

    def get_name(self):
        return self.__name

    def get_phone(self):
        return self.__phone_number
