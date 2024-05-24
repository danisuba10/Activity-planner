import datetime

from src.domain import activity, person
from src.unique_exceptions import exceptions
import pickle

class MemoryPersonRepositoryFunctions():
    def valid_person_add(self, people:list[person.Person], pers:person.Person):
        '''
        :param people: people in repository
        :param pers: person to be added to repository
        :return: raises repository exception if person cannot be added to repository
        '''
        for current in people:
            if pers.get_id() == current.get_id():
                raise exceptions.PersonAlreadyInRepo()
            if pers.get_phone() == current.get_phone():
                raise exceptions.RepositoryError("A person already has this phone number!")

    def valid_person_remove(self, persons:list[person.Person], id):
        '''
        :param persons: persons in repo
        :param id: id of person to be removed
        :return: removes person from repo if possible, raises repository exception otherwise
        '''
        found = False
        for pers in persons:
            if id == pers.get_id():
                found = True
        if not found:
            raise exceptions.RepositoryError("Person not found!")


class MemoryActivityRepositoryFunctions():

    def __init__(self):
        pass

    def __remove_busy_persons(self, activities:list[activity.Activity], activ:activity.Activity):
        '''
        :param activities: existing activites in repo
        :param activ: current activity
        :return: activity to be added, with busy persons removed, array of busy persons
        '''
        removed_persons = []

        for current in activities:
            curr_persons = current.get_people()
            if activ.get_id() == current.get_id():
                raise exceptions.ActivityAlreadyInRepo()
            if current.get_datetime() <= activ.get_datetime() <= current.get_endtime():
                activity_persons = activ.get_people()
                for i in range(0, len(activity_persons), 1):
                    if activity_persons[i] in curr_persons:
                        activ.remove_person(activity_persons[i])
                        removed_persons.append(activity_persons[i])

        return activ, removed_persons

    def __remove_missing_persons(self, persons:list[person.Person], activ:activity.Activity):
        '''
        :param persons: existing persons
        :param activ: current activity to be added to repo
        :return: activity, with missing people removed, array of missing
        people
        '''
        removed_persons = []

        activity_persons = activ.get_people()
        for i in range(0, len(activity_persons), 1):
            found = False
            for pers in persons:
                if activity_persons[i] == pers.get_id():
                    found = True
            if not found:
                activ.remove_person(activity_persons[i])
                removed_persons.append(activity_persons[i])

        return activ, removed_persons

    def valid_activity_add(self, activities:list[activity.Activity], persons:list[person.Person], activ:activity.Activity)->tuple[activity.Activity,list[person.Person],list[person.Person]]:
        '''
        :param activities: existing activities in repo
        :param persons: existing persons in repo
        :param activ: activity to be added
        :return: raises repository exception if invalid activity to be added
        '''

        if not(activ.get_date() != None and activ.get_endtime() != None):
            raise exceptions.ActivityError("Activity not complete!")

        if activ.get_endtime() < activ.get_datetime():
            raise exceptions.ActivityError("End time is before start time!")

        for current in activities:
            if activ.get_id() == current.get_id():
                raise exceptions.ActivityAlreadyInRepo()

        activ, busy_persons = self.__remove_busy_persons(activities, activ)

        activ, missing_persons = self.__remove_missing_persons(persons, activ)

        return activ, busy_persons, missing_persons

    def valid_activity_remove(self, activites:list[activity.Activity], id):
        '''
        :param activites: activities in repo
        :param id: id of activity to be removed
        :return: removes activity with said id, raises exception otherwise
        '''
        found = False
        for activ in activites:
            if id == activ.get_id():
                found = True
        if not found:
            raise exceptions.ActivityError("Activity not found!")


class PersonMemoryRepository:

    def __init__(self):
        self.__people = []
        self.__func = MemoryPersonRepositoryFunctions()

    def get_person(self, id):
        for pers in self.__people:
            if pers.get_id() == id:
                return pers
        raise exceptions.RepositoryError("Person with such id nout found!")

    def get_persons(self):
        return self.__people

    def add_person(self, person:person.Person):
        '''
        :param person: person to be added to repo
        :return: adds person to repo, raises repository exception if not possible
        '''
        try:
            self.__func.valid_person_add(self.get_persons(), person)
            self.__people.append(person)
        except exceptions.RepositoryError:
            raise
    def remove_person(self, id):
        '''
        :param id: id of person to be removed
        :return: removes person from repository
        '''
        try:
            self.__func.valid_person_remove(self.get_persons(), id)
            for i in range(0, len(self.__people), 1):
                if self.__people[i].get_id() == id:
                    self.__people.pop(i)
                    break
        except exceptions.RepositoryError:
            raise

    def search_pers_name(self, name)->list[person.Person]:
        search_result = []
        persons = self.get_persons()
        for pers in persons:
            if name in pers.get_name().lower():
                search_result.append(pers)
        return search_result

    def search_pers_phone(self, phone)->list[person.Person]:
        search_result = []
        persons = self.get_persons()
        for pers in persons:
            if phone in pers.get_phone():
                search_result.append(pers)
        return search_result

class ActivityMemoryRepository(PersonMemoryRepository):

    def __init__(self):
        super().__init__()
        self.__activities = []
        self.__func = MemoryActivityRepositoryFunctions()

    def get_activity(self, id):
        for activ in self.__activities:
            if activ.get_id() == id:
                return activ
        raise exceptions.RepositoryError("Activity with such ID not found!")

    def get_activities(self)->list[activity.Activity]:
        return self.__activities

    def add_activity(self, activity:activity.Activity):
        '''
        :param activity: activity to be added to repo
        :return: adds activity to repo, returns busy people removed and missing people removed
        '''
        try:
            activ, busy_persons, missing_persons = self.__func.valid_activity_add(self.get_activities(),
                                                                                  self.get_persons(), activity)
            self.__activities.append(activ)
            return busy_persons, missing_persons
        except exceptions.ActivityError:
            raise

    def remove_activity(self, id):
        '''
        :param id: id of activity to be removed
        :return: removes activity from repository
        '''
        try:
            self.__func.valid_activity_remove(self.get_activities(), id)
            for i in range(0, len(self.__activities), 1):
                if self.__activities[i].get_id() == id:
                    self.__activities.pop(i)
                    break
        except exceptions.ActivityError as aerr:
            raise exceptions.RepositoryError(aerr.__str__())

    def add_pers_act(self, id, pers_id):
        for i in range(0, len(self.__activities), 1):
            if self.__activities[i].get_id() == id:
                self.__activities[i].add_person(pers_id)

    def remove_pers_act(self, id, pers_id):
        for i in range(0, len(self.__activities), 1):
            if self.__activities[i].get_id() == id:
                self.__activities[i].remove_person(pers_id)

    def search_activity_desc(self, desc)->list[activity.Activity]:
        search_result = []
        activities = self.get_activities()
        for act in activities:
            if desc in act.get_description().lower():
                search_result.append(act)
        return search_result

    def search_activity_dt(self, dt):
        res = []
        activities = self.get_activities()
        for activ in activities:
            if activ.get_datetime() <= dt <= activ.get_endtime():
                res.append(activ)
        return res

    def search_activity_person(self, pers_id):
        res = []
        activities = self.get_activities()
        for activ in activities:
            if pers_id in activ.get_people():
                res.append(activ)
        return res

    def search_date(self, dat:datetime.date):
        res = []
        activities = self.get_activities()
        for activ in activities:
            if activ.get_date() == dat:
                res.append(activ)
        return res


class PickleActivityMemoryRepository(ActivityMemoryRepository):

    def __init__(self, person_p, activities_p):
        super().__init__()
        self.activ_p = activities_p
        self.person_p = person_p
        self.__valid_files()
        try:
            self.load_from_pickle()
        except:
            pass

    def __valid_files(self):
        '''

        :return: checks if files valid
        '''
        pers = self.person_p
        activ = self.activ_p
        if not(pers.count(".") == 1 and activ.count(".") == 1):
            raise exceptions.RepositoryError("Incorrect file to save domain! Missing extension!")
        pers = pers.split(".")
        activ = activ.split(".")
        if not(pers[1] == "pickle" and activ[1] == "pickle"):
            raise exceptions.RepositoryError("Incorrect file to save domain! Incorrect extension!")

    def save_to_pickle(self):
        '''
        :return: saves to pickle
        '''
        with open(self.activ_p, 'wb') as file:
            data_to_pickle = {
                'activities': self.get_activities(),
            }
            pickle.dump(data_to_pickle, file)

        with open(self.person_p, 'wb') as file:
            data_to_pickle = {
                'people': self.get_persons(),
            }
            pickle.dump(data_to_pickle, file)

    def load_from_pickle(self):
        '''

        :return: loads from pickle
        '''
        with open(self.activ_p, 'rb') as file:
            data = pickle.load(file)
            self._ActivityMemoryRepository__activities = data['activities']
            #activity.Activity.last_id = data['last_act_id']
        with open(self.person_p, 'rb') as file:
            data = pickle.load(file)
            self._PersonMemoryRepository__people = data['people']

    def after_op(self):
        '''

        :return: after operation saves to picke
        '''
        self.save_to_pickle()

    def add_activity(self, activity:activity.Activity):
        '''
        :param activity: activity to be added to repo
        :return: adds activity to repo, returns busy people removed and missing people removed
        '''
        busy_persons, missing_persons = super().add_activity(activity)
        self.after_op()
        return busy_persons, missing_persons

    def remove_activity(self, id):
        '''
        :param id: id of activity to be removed
        :return: removes activity from repository
        '''
        super().remove_activity(id)
        self.after_op()

    def add_person(self, person:person.Person):
        '''

        :param person: pers
        :return: ads pers
        '''
        super().add_person(person)
        self.after_op()

    def remove_person(self, id):
        '''

        :param id: id of pers
        :return: removes pers
        '''
        super().remove_person(id)
        self.after_op()

class TextActivityMemoryRepository(ActivityMemoryRepository):

    def __init__(self, person_t, activities_t):
        super().__init__()
        self.activ_t = activities_t
        self.person_t = person_t
        try:
            self.load_from_textfile()
        except:
            pass

    def save_activity(self, activ:activity.Activity, file):
        '''

        :param activ: activ
        :param file: file
        :return: saves pers to file
        '''
        file.write(f"{activ.get_id()}|{activ.get_datetime()}|{activ.get_endtime()}|"
              f"{activ.get_description()}|")

        people = activ.get_people()
        for i in range(0, len(people), 1):
            file.write(people[i])
            if i != len(people) - 1:
                file.write(",")
        file.write("|\n")

    def save_person(self, pers:person.Person, file):
        '''

        :param pers: pers
        :param file: file
        :return: saves person to file
        '''
        file.write(f"{pers.get_id()}|{pers.get_name()}|{pers.get_phone()}|\n")

    def save_to_textfile(self):
        '''
        :return: saves to txt
        '''
        with open(self.activ_t, "w") as activ_file:
            for activ in self.get_activities():
                self.save_activity(activ, activ_file)

        with open(self.person_t, 'w') as pers_file:
            for pers in self.get_persons():
                self.save_person(pers, pers_file)

    def load_from_textfile(self):
        '''

        :return: loads data from txt
        '''
        with open(self.activ_t, "r") as activ_file:
            lines = activ_file.readlines()
            activities = []

            for line in lines:
                if "|" in line:
                    line = line.split("|")
                    id = line[0]
                    start_date = datetime.datetime.strptime(line[1], '%Y-%m-%d %H:%M:%S')
                    end_date = datetime.datetime.strptime(line[2], '%Y-%m-%d %H:%M:%S')
                    description = line[3]
                    people = line[4]
                    people = people.split(",")
                    activ = activity.Activity(people, start_date, end_date, description)
                    activ.set_id(id)
                    activities.append(activ)

            a = 1
            self._ActivityMemoryRepository__activities = activities

        with open(self.person_t, "r") as text_file:
            lines = text_file.readlines()
            people = []

            for line in lines:
                if "|" in line:
                    line = line.split("|")
                    id = line[0]
                    name = line[1]
                    phone = line[2]
                    pers = person.Person(name, phone)
                    pers.set_id(id)
                    people.append(pers)

            self._PersonMemoryRepository__people = people

    def after_op(self):
        '''
        :return: saves after any operation
        '''
        self.save_to_textfile()

    def add_activity(self, activity:activity.Activity):
        '''
        :param activity: activity to be added to repo
        :return: adds activity to repo, returns busy people removed and missing people removed
        '''
        busy_persons, missing_persons = super().add_activity(activity)
        self.after_op()
        return busy_persons, missing_persons

    def remove_activity(self, id):
        '''
        :param id: id of activity to be removed
        :return: removes activity from repository
        '''
        super().remove_activity(id)
        self.after_op()

    def add_person(self, person:person.Person):
        '''

        :param person: person to be added
        :return: adds person
        '''
        super().add_person(person)
        self.after_op()

    def remove_person(self, id):
        '''

        :param id: id
        :return: removes pers
        '''
        super().remove_person(id)
        self.after_op()