import unittest
from datetime import datetime

from src.domain import activity, person
from src.services import services
from src.repository import repository

class TestAdd(unittest.TestCase):

    def test_person_add(self):
        serv = services.Services()

        name = "Loka Kju"
        phone = "123"
        pers1 = person.Person(name, phone)
        person.Person.last_id -= 1
        serv.add_person(name, phone)
        self.assertEquals(serv.repo.get_persons()[0].get_name(), pers1.get_name())
        name = "Liku Kuja"
        phone = "124"
        pers2 = person.Person(name, phone)
        person.Person.last_id -= 1
        serv.add_person(name, phone)
        self.assertEquals(serv.repo.get_persons()[1].get_phone(), pers2.get_phone())

    def test_person_remove(self):
        serv = services.Services()
        person.Person.last_id = 0
        name = "Loka Kju"
        phone = "123"
        pers1 = person.Person(name, phone)
        person.Person.last_id -= 1
        serv.add_person(name, phone)
        name = "Liku Kuja"
        phone = "124"
        pers2 = person.Person(name, phone)
        person.Person.last_id -= 1
        serv.add_person(name, phone)
        serv.remove("person", "1")
        self.assertEquals(serv.repo.get_persons()[0].get_phone(), pers2.get_phone())

    def test_person_update(self):
        serv = services.Services()
        person.Person.last_id = 0
        name = "Loka Kju"
        phone = "123"
        pers1 = person.Person(name, phone)
        person.Person.last_id -= 1
        serv.add_person(name, phone)
        serv.update_person("1", "Kjuy", "431")
        self.assertEquals(serv.repo.get_persons()[0].get_name(), "Kjuy")
        self.assertEquals(serv.repo.get_persons()[0].get_phone(), "431")

    def test_person_list(self):
        serv = services.Services()
        self.assertEquals(serv.list("persons"), serv.repo.get_persons())

    def test_activity_list(self):
        serv = services.Services()
        self.assertEquals(serv.list("activities"), serv.repo.get_activities())

    def test_add_activity(self):
        serv = services.Services()
        desc = "Lorem ipsum"
        start_date = datetime(2023,12,12,00,00,00)
        end_date = datetime(2023,12,12,5,00,5)
        id_pers = ["1", "2"]
        serv.add_activity(id_pers, start_date, end_date, desc)
        self.assertEquals(serv.repo.get_activities()[0].get_datetime(), start_date)
        self.assertEquals(serv.repo.get_activities()[0].get_endtime(), end_date)

    def test_remove_activity(self):
        activity.Activity.last_id = 0
        serv = services.Services()
        desc = "Lorem ipsum"
        start_date = datetime(2023, 12, 12, 00, 00, 00)
        end_date = datetime(2023, 12, 12, 5, 00, 5)
        id_pers = ["1", "2"]
        serv.add_activity(id_pers, start_date, end_date, desc)
        desc = "Lorem Dolore"
        start_date = datetime(2023, 10, 12, 00, 00, 00)
        end_date = datetime(2023, 10, 12, 5, 00, 5)
        id_pers = ["1", "3"]
        serv.add_activity(id_pers, start_date, end_date, desc)
        serv.remove("activity", "1")
        self.assertEquals(serv.repo.get_activities()[0].get_datetime(), start_date)
        self.assertEquals(serv.repo.get_activities()[0].get_endtime(), end_date)
        self.assertEquals(serv.repo.get_activities()[0].get_description(), "Lorem Dolore")
        self.assertEquals(serv.repo.get_activities()[0].get_people(), [])

    def test_update_activity(self):
        activity.Activity.last_id = 0
        serv = services.Services()
        desc = "Lorem ipsum"
        start_date = datetime(2023, 12, 12, 00, 00, 00)
        end_date = datetime(2023, 12, 12, 5, 00, 5)
        id_pers = ["1", "2"]
        serv.add_activity(id_pers, start_date, end_date, desc)
        serv.update_activity("1", [], start_date, end_date, "Nughju")
        self.assertEquals(serv.repo.get_activities()[0].get_description(), "Nughju")