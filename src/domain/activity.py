from src.domain import person
from src.unique_exceptions import exceptions
from datetime import datetime
import random

class Activity:

    def __init__(self, id_arr:list[str], dt:datetime, et:datetime, descr:str):
        #Activity.last_id +=
        self.__activity_id = str(random.randint(100000, 999999))
        self.__person_id = id_arr.copy()
        self.__date_time = dt
        self.__end_time = et
        self.__date = self.__date_time.date()
        self.__time = self.__date_time.time()
        self.__description = descr

    def get_id(self):
        return self.__activity_id

    def set_id(self, id):
        self.__activity_id = id

    def get_people(self)->list[person.Person]:
        return self.__person_id

    def set_people(self, id_arr):
        self.__person_id = id_arr.copy()

    def add_person(self, id):
        self.__person_id.append(id)

    def remove_person(self, id):
        self.__person_id.remove(id)

    def get_datetime(self)->datetime:
        return self.__date_time

    def get_endtime(self):
        return self.__end_time

    def set_datetime(self, dt:datetime):
        self.__date_time = dt
        self.__date = dt.date()
        self.__time = dt.time()

    def set_endtime(self, et):
        self.__end_time = et

    def get_date(self):
        return self.__date

    def get_time(self):
        return self.__time

    def get_description(self):
        return self.__description

    def set_description(self, desc):
        self.__description = desc

    def add_person(self, pers_id:int):
        if not(pers_id in self.__person_id):
            self.__person_id.append(pers_id)
        else:
            raise exceptions.PersonHasActivityException()

    def remove_person(self, id):
        new_arr = []
        for i in range(0, len(self.__person_id), 1):
            if not(self.__person_id[i] == id):
                new_arr.append(self.__person_id[i])
        self.__person_id = new_arr.copy()

    def set_description(self, description):
        self.__description = description

    def set_date(self, date):
        self.__date = date

    def set_time(self, time):
        self.__time = time


