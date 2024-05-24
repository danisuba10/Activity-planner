from src.datagen import datagen
from src.domain import person, activity

class ProceduralGeneration:

    def __init__(self):
        self.__gen_functions = datagen.Generate()

    def generate_people(self, length)->list[person.Person]:
        arr_pers = []
        for i in range(0, length, 1):
            pers = self.__gen_functions.generate_person()
            arr_pers.append(pers)
        return arr_pers
    def generate_activities(self, activity_length)->list[activity.Activity]:
        arr_activ = []
        for i in range(0, activity_length, 1):
            activ = self.__gen_functions.generate_activity()
            arr_activ.append(activ)
        return arr_activ