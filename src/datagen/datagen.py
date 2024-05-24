import random
from src.domain import person, activity
import datetime as dt


class Generate:

    def __init__(self):
        self.__family_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez",
                        "Martinez",
                        "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson", "Thomas", "Taylor", "Moore", "Jackson",
                        "Martin", "Lee", "Perez", "Thompson", "White", "Harris", "Sanchez", "Clark", "Ramirez",
                        "Lewis", "Robinson", "Walker", "Young", "Hall", "Allen", "King", "Wright", "Scott", "Torres",
                        "Nguyen", "Hill"]
        self.__first_names = ["Emma", "Liam", "Olivia", "Noah", "Ava", "William", "Sophia", "James", "Isabella", "Oliver",
                       "Charlotte",
                       "Benjamin", "Amelia", "Mia", "Lucas", "Harper", "Mason", "Evelyn", "Logan", "Abigail",
                       "Alexander", "Emily", "Ethan", "Elizabeth", "Jacob", "Mila", "Michael", "Ella", "Daniel",
                       "Avery",
                       "Henry", "Sofia", "Jackson", "Camila", "Sebastian", "Scarlett", "Aiden", "Victoria", "Matthew",
                       "Luna"]
        self.__activities = ["Reading", "Hiking", "Cooking", "Painting", "Swimming", "Gardening", "Yoga", "Photography",
                             "Writing", "Dancing", "Fishing", "Camping", "Singing", "Running", "Drawing", "Meditation",
                             "Cycling", "Knitting", "Playing Chess", "Playing Guitar", "Traveling", "Watching Movies",
                             "Bird Watching", "Pottery", "Rock Climbing", "Volunteering", "Skydiving", "Scuba Diving",
                             "Woodworking", "Skiing", "Baking", "Surfing", "Calligraphy", "Bowling", "Ice Skating",
                             "Golfing", "Juggling", "Horseback Riding", "Sudoku", "Candle Making"]

        self.person_ids = []

    def generate_person(self)->person.Person:
        first_name = self.__first_names[random.randint(0, 39)]
        family_name = self.__family_names[random.randint(0, 39)]
        phone = str(random.randint(1000000000, 9999999999))
        pers = person.Person(family_name + " " + first_name, phone)
        self.person_ids.append(pers.get_id())
        return pers

    def generate_activity(self)->activity.Activity:
        desc = self.__activities[random.randint(0, 39)]
        start_date = dt.datetime(2023,1, 1, 00, 00, 00)
        end_date = dt.datetime(2024, 12, 31, 23, 59, 59)
        random_seconds = random.randint(0, int((end_date - start_date).total_seconds()))
        datett = start_date + dt.timedelta(seconds=random_seconds)
        start_seconds = datett.time().hour * 3600 + datett.time().minute * 60 + datett.time().second
        etime = datett + dt.timedelta(seconds=random.randint(0, 86400 - start_seconds))
        id_arr = [self.person_ids[random.randint(0, 19)] for i in range(5)]
        id_arr = list(set(id_arr))
        activ = activity.Activity(id_arr, datett, etime, desc)
        return activ

#gen = Generate()
#act = gen.generate_activity()
#a = 1
