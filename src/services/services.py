from src.domain import person, activity
from src.repository import repository
from src.unique_exceptions import exceptions
from datetime import datetime
from src.services import gen
from src.services.undo import CascadedOperation, Command, Operation
class Services:

    def __init__(self, type, pers_l, act_l, undo_service):


        self._undoserv = undo_service
        self.type = type
        self.pers_l = pers_l
        self.act_l = act_l
        if self.type == "inmemory":
            self.repo = repository.ActivityMemoryRepository()
        elif self.type == "binaryfiles":
            try:
                self.repo = repository.PickleActivityMemoryRepository(pers_l, act_l)
            except exceptions.RepositoryError as reperr:
                raise exceptions.PropertiesError(f"File: {reperr.__str__()}")
        elif self.type == "text":
            self.repo = repository.TextActivityMemoryRepository(pers_l, act_l)
        else:
            raise exceptions.PropertiesError("Incorrect repository type!")
        self.gen = gen.ProceduralGeneration()

    def generate_start(self):
        pers_arr = self.gen.generate_people(20)
        activ_arr = self.gen.generate_activities(20)
        person.Person.last_id = 0
        activity.Activity.last_id = 0
        for i in range(0, 20, 1):
            #self.add_persona(pers_arr[i].get_name(), pers_arr[i].get_phone())\
            self.add_person_dom(pers_arr[i])
        for i in range(0, 20, 1):
            #self.add_activity(activ_arr[i].get_people(), activ_arr[i].get_datetime(), activ_arr[i].get_endtime(), activ_arr[i].get_description())
            self.add_activity_dom(activ_arr[i])

    def add_person(self, name:str, phone:str):
        '''
        :param name: name of person to be added
        :param phone: phone of person to be added
        :return: adds person to the repo, transmit repository exception otherwise
        '''
        pers = person.Person(name, phone)
        try:
            undo = Command(self.remove, "person", pers.get_id())
            redo = Command(self.add_person_dom, pers)
            operation = Operation(undo, redo)
            self._undoserv.record_for_undo(operation)

            self.repo.add_person(pers)
        except exceptions.RepositoryError:
            raise

    def add_person_dom(self, pers:person.Person):
        '''
        :param pers: persons to be added is object
        :return:
        '''
        try:
            self.repo.add_person(pers)
        except exceptions.RepositoryError:
            raise

    def add_activity(self, person_id:list, dt:datetime, et:datetime, description:str):
        '''
        :param person_id: ids of people associaged with activity
        :param dt: date and time of activity
        :param description: description of activity
        :return: adds activity to repository, transmits received repository error otherwise
        '''
        act = activity.Activity(person_id, dt, et, description)
        try:
            busy_persons, missing_persons = self.repo.add_activity(act)

            undo = Command(self.remove, "activity", act.get_id())
            redo = Command(self.add_activity_dom, act)
            operation = Operation(undo, redo)
            self._undoserv.record_for_undo(operation)

            return busy_persons, missing_persons
        except exceptions.ActivityError as aerr:
            raise exceptions.RepositoryError(aerr.__str__())

    def add_activity_dom(self, act:activity.Activity):
        '''
        :param act: activity to be added, object
        :return:
        '''
        try:
            busy_persons, missing_persons = self.repo.add_activity(act)
            return busy_persons, missing_persons
        except exceptions.ActivityError as aerr:
            raise exceptions.RepositoryError(aerr.__str__())

    def list(self, target):
        '''
        :param target: persons or activities
        :return: returns a list of persons or activities from repo so UI can print them
        '''
        if target == "persons":
            return self.repo.get_persons()
        elif target == "activities":
            return self.repo.get_activities()

    def remove(self, target:str, id:str):
        '''
        :param target: person or activity
        :param id: id of target to be deleted
        :return: removes target from repository
        '''
        if target == "person":
            cascaded_operations = []
            try:
                pers = self.get_person(id)

                undo = Command(self.add_person_dom, pers)
                redo = Command(self.remove, "person", id)
                operation = Operation(undo ,redo)
                cascaded_operations.append(operation)

                self.repo.remove_person(id)
                activities = self.search_with_person(id)
                for act in activities:
                    undo = Command(self.add_pers_to_act, act.get_id(), id)
                    redo = Command(self.remove_pers_from_act, act.get_id(), id)
                    operation = Operation(undo, redo)
                    cascaded_operations.append(operation)

                    self.remove_pers_from_act(act.get_id(), id)

                self._undoserv.record_for_undo(CascadedOperation(cascaded_operations))

            except exceptions.RepositoryError:
                raise
        elif target == "activity":
            act = self.get_activity(id)
            try:
                undo = Command(self.add_activity_dom, act)
                redo = Command(self.remove, "activity", id)
                operation = Operation(undo, redo)
                self._undoserv.record_for_undo(operation)
                self.repo.remove_activity(id)
            except exceptions.RepositoryError:
                raise

    def add_pers_to_act(self, id, pers_id):
        self.repo.add_pers_act(id, pers_id)

    def remove_pers_from_act(self, id, pers_id):
        self.repo.remove_pers_act(id, pers_id)

    def update_person(self, id, name:str, phone:str):
        '''
        :param id: id of person to be updated
        :param name: new name
        :param phone: new phone
        :return: updates old variables to new ones, transmits repository error otherwise
        '''
        try:
            old_pers = self.get_person(id)
            pers = person.Person(name, phone)
            pers.set_id(id)

            undo = Command(self.__update_pers_dom, id, old_pers)
            redo = Command(self.__update_pers_dom, id, pers)
            operation = Operation(undo, redo)
            self._undoserv.record_for_undo(operation)

            self.__update_pers_dom(id, pers)
        except exceptions.RepositoryError:
            raise
    def __update_pers_dom(self, id, pers:person.Person):
        '''

        :param id: id of pers
        :param pers: pers object to be updated
        :return:
        '''
        self.repo.remove_person(id)
        self.repo.add_person(pers)

    def update_activity(self, id:str, id_arr:list, dt:datetime, et:datetime, desc:str):
        '''
        :param id: id of activity to be updated
        :param id_arr: new ids of persons associated
        :param dt: new date and time
        :param desc: new description
        :return: updates old activity with new activity, transmits received repository exception otherwise
        '''
        try:
            old_activ = self.get_activity(id)
            activ = activity.Activity(id_arr, dt, et, desc)
            activ.set_id(id)

            undo = Command(self.__update_activity_dom, id, old_activ)
            redo = Command(self.__update_activity_dom, id, activ)
            operation = Operation(undo, redo)
            self._undoserv.record_for_undo(operation)

            self.__update_activity_dom(id, activ)
        except exceptions.RepositoryError:
            raise

    def __update_activity_dom(self, id, activ):
        '''
        :param id: id of act
        :param activ: activity to be updated object
        :return:
        '''
        self.repo.remove_activity(id)
        busy_persons, missing_persons = self.repo.add_activity(activ)
        return busy_persons, missing_persons

    def get_person(self, id)->person.Person:
        '''

        :param id: id of desired pers
        :return:
        '''
        try:
            return self.repo.get_person(id)
        except exceptions.RepositoryError:
            raise

    def get_activity(self, id)->activity.Activity:
        '''

        :param id: id of desired activity
        :return:
        '''
        try:
            return self.repo.get_activity(id)
        except exceptions.RepositoryError as reperr:
            raise

    def fill_none_activity(self, activ:activity.Activity, id_arr, date_time, end_time, desc):
        '''
        :param activ: old activity
        :param id_arr: new ids of associated people
        :param date_time: new start time
        :param end_time new endtime
        :param desc: new description
        :return: if some of the fields are empty, they are replaced with the old value
        '''
        if id_arr == []:
            id_arr = activ.get_people().copy()
        if date_time == "":
            date_time = activ.get_datetime()
        if end_time == "":
            end_time = activ.get_endtime()
        if desc == "":
            desc = activ.get_description()

        return id_arr, date_time, end_time, desc

    def fill_none_person(self, pers:person.Person, name:str, phone:str):
        '''
        :param pers: old person
        :param name: new name
        :param phone: new phone
        :return: if one of the fields is empty, it will be replaced with the old value
        '''
        if name == "":
            name = pers.get_name()
        if phone == "":
            phone = pers.get_phone()

        return name, phone

    def search(self, target, field, value):
        if target == "person":
            if field == "name":
                return self.repo.search_pers_name(value)
            elif field == "phone":
                return self.repo.search_pers_phone(value)
        elif target == "activity":
            if field == "description":
                return self.repo.search_activity_desc(value)
            elif field == "date-time":
                return self.repo.search_activity_dt(value)

    def search_date(self, dat:datetime.date):
        res =  self.repo.search_date(dat)

        swap = True
        steps = 0
        while swap == True:
            swap = False
            for i in range(0, len(res) - 1 - steps, 1):
                if res[i].get_datetime() > res[i+1].get_datetime():
                    temp = res[i]
                    res[i] = res[i+1]
                    res[i+1] = temp
                    swap = True
            steps += 1

        return res

    def search_with_person(self, pers_id):
        return self.repo.search_activity_person(pers_id)

    def busiest(self):
        days_activities = {}
        days_intervals = {}
        activities = self.repo.get_activities()
        for activ in activities:
            try:
                days_activities[str(activ.get_datetime().date())] += 1
                days_intervals[str(activ.get_datetime().date())].append(
                    [activ.get_datetime().time(), activ.get_endtime().time()])
            except KeyError:
                days_activities[str(activ.get_datetime().date())] = 1
                days_intervals[str(activ.get_datetime().date())] = [
                    [activ.get_datetime().time(), activ.get_endtime().time()]]
        busiest = 0
        for date, count in days_activities.items():
            if count > busiest:
                busiest = count

        b_day_count = {}
        b_interval_count = {}
        b_free_count = {}
        for day, count in days_activities.items():
            if count == busiest:
                b_day_count[day] = count
                b_interval_count[day] = days_intervals[day].copy()

        for day, intervals in b_interval_count.items():

            intervals.sort(key=lambda x: x[0])
            total_free_seconds = 0
            last_end_time = datetime.strptime("00:00", "%H:%M").time()

            for interval in intervals:
                start_time = interval[0]
                end_time = interval[1]
                if start_time > last_end_time:
                    free_interval_start = datetime.combine(datetime.today(), last_end_time)
                    free_interval_end = datetime.combine(datetime.today(), start_time)
                    free_duration = (free_interval_end - free_interval_start).total_seconds()
                    total_free_seconds += free_duration
                if end_time > last_end_time:
                    last_end_time = end_time

            if last_end_time < datetime.strptime("23:59", "%H:%M").time():
                free_interval_start = datetime.combine(datetime.today(), last_end_time)
                free_interval_end = datetime.combine(datetime.today(), datetime.strptime("23:59", "%H:%M").time())
                free_duration = (free_interval_end - free_interval_start).total_seconds()
                total_free_seconds += free_duration

            b_free_count[day] = total_free_seconds

        b_free_count = dict(sorted(b_free_count.items(), key=lambda item: item[1]))
        # b_free_count.sort(key=lambda x: x[1])
        return b_free_count


