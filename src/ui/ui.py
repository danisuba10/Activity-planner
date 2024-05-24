from src.datagen import datagen
from src.services import services, gen
from src.unique_exceptions import exceptions
from datetime import datetime
from src.services.undo import UndoService

class UI_Validations:

    def __init__(self):
        pass

    def __valid_menu_input(self, input: str) -> bool:
        '''
        :param input: type string, user input stripped of spaces and made
        lowercase
        :return: true if user input valid(a,b,c,d or e) or false otherwise
        '''
        if len(input) != 1:
            raise exceptions.InputError("Incorrect input length!")
        if not ('a' <= input <= 'g'):
            raise exceptions.InputError("Incorrect input character!")

    def valid_optiona_input(self, input_arr):
        options = ["add", "remove", "update", "list"]
        if not(input_arr[0] in options):
            raise exceptions.InputError("Incorrect command!")
        if input_arr[0] == "add":
            if len(input_arr) != 2:
                raise exceptions.InputError("Invalid no. of "
                                            "parameters for command!")
            if not(input_arr[1] == "person" or input_arr[1] == "activity"):
                raise exceptions.InputError("Invalid second parameter!")
        if input_arr[0] == "remove" or input_arr[0] == "update":
            if len(input_arr) != 3:
                raise exceptions.InputError("Invalid no. of parameters"
                                            "for command!")
            if not(input_arr[1] == "person" or input_arr[1] == "activity"):
                raise exceptions.InputError("Invalid second parameter!")
        if input_arr[0] == "list":
            if len(input_arr) != 2:
                raise exceptions.InputError("Invalid no. of "
                                            "parameters for command!")
            if not (input_arr[1] == "persons" or input_arr[1] == "activities"):
                raise exceptions.InputError("Invalid second parameter!")

    def valid_optionb_input(self, input_arr):
        options = ["add", "remove"]
        if not (input_arr[0] in options):
            raise exceptions.InputError("Incorrect command!")
        if input_arr[0] == "add":
            if len(input_arr) != 2:
                raise exceptions.InputError("Invalid no. of "
                                            "parameters for command!")
            if not (input_arr[1] == "person" or input_arr[1] == "activity"):
                raise exceptions.InputError("Invalid second parameter!")
        if input_arr[0] == "remove":
            if len(input_arr) != 3:
                raise exceptions.InputError("Invalid no. of parameters"
                                            "for command!")
            if not (input_arr[1] == "activity"):
                raise exceptions.InputError("Invalid second parameter!")

    def valid_optionc_input(self, input_arr):
        if len(input_arr) != 3:
            raise exceptions.InputError("Incorrect no. of parameters!")
        if input_arr[0] != "search":
            raise exceptions.InputError("Incorrect command!")
        if not(input_arr[1] == "person" or input_arr[1] == "activity"):
            raise exceptions.InputError("Incorrect second command!")
        if input_arr[1] == "person":
            if not(input_arr[2] == "name" or input_arr[2] == "phone"):
                raise exceptions.InputError("Incorrect field to search for!")
        if input_arr[1] == "activity":
            if not(input_arr[2] == "date-time" or input_arr[2] == "description"):
                raise exceptions.InputError("Incorrect field to search for!")

    def valid_optiond_input(self, input_arr):
        if len(input_arr) != 1:
            raise exceptions.InputError("Invalid length!")
        commands = ["a", "b", "c"]
        if input_arr[0] not in commands:
            raise exceptions.InputError("Invalid command!")

    def valid_idarr_input(self, input_arr):
        try:
            for element in input_arr:
                integer = int(element)
        except Exception:
            raise exceptions.InputError("One of the IDs is incorrect!(Not an integer)")

    def format_input_string(self, input: str) -> str:
        '''
        :param input: type string, gets the raw input of user
        :return: correct user input without spaces, raises error otherwise
        if user input not correct
        '''
        formatted_input = input.replace(" ", "")
        formatted_input = formatted_input.lower()
        try:
            self.__valid_menu_input(formatted_input)
            return formatted_input
        except exceptions.InputError as ierr:
            raise

    def format_input_menu_array_string(self, input:str, valid)->list:
        '''
        :param input: type string, raw input string for menu option B
        :param valid: function, checks if input is valid for menu option B
        raises exception otherwise
        :return: input split into array if input is correct, None otherwise
        '''
        input_array = input.strip().lower()
        input_array = input_array.split(" ")
        try:
            valid(input_array)
            return input_array
        except exceptions.InputError as ierr:
            raise

class OptionA:

    def __init__(self, serv):
        self._validations = UI_Validations()
        self._services = serv
    def __get_option_a_text(self):
        lines = "_____________________________________\n"
        syntax_person = ("Syntax persons:\n"
                         "add person\n"
                         "remove person <id>\n"
                         "update person <id>\n"
                         "list persons\n")
        syntax_activity = ("Syntax activity:\n"
                           "add activity\n"
                           "remove activity <id>\n"
                           "update activity <id>\n"
                           "list activities\n")
        option_a_text = lines + syntax_person + lines + syntax_activity + lines
        return option_a_text

    def __get_menu_input(self):
        input_string = input(">>>")
        try:
            input_arr = self._validations.format_input_menu_array_string(input_string, self._validations.valid_optiona_input)
            return input_arr
        except exceptions.InputError as ierr:
            print(f"Error occured: {ierr}")
            return None

    def _get_id_input(self, func):
        print("Which people are doing it? Syntax: <id1> <id2> ...\n")
        id_arr = input(">>>")
        id_arr = id_arr.strip()
        if func == "update" and id_arr == "":
            return []

        try:
            id_arr = self._validations.format_input_menu_array_string(id_arr, self._validations.valid_idarr_input)
            return id_arr
        except exceptions.InputError as ierr:
            print(f"Error occured: {ierr}")
            return None

    def __get_datetime_input(self, func:str):
        user_input = input("Please enter a date and time in the format 'YYYY-MM-DD HH:MM:SS':\n")
        user_input = user_input.strip()
        if func == "update" and user_input == "":
            return ""
        try:
            valid_datetime = datetime.strptime(user_input, '%Y-%m-%d %H:%M:%S')
            return valid_datetime
        except ValueError:
            raise exceptions.InputError("Not a valid date and time!")

    def get_name(self):
        print("What is the person's name?")
        name = input(">>>")
        name = name.strip()
        return name

    def get_phone(self):
        print("What is the person's phone number?")
        phone = input(">>>")
        phone = phone.strip()
        return phone

    def get_datetime(self, func:str):
        print("Syntax: <YYYY-MM-DD HH:MM:SS>: 2023-12-14 13:57:43")
        dt = None
        while dt is None:
            try:
                dt = self.__get_datetime_input(func)
                return dt
            except exceptions.InputError as ierr:
                print(f"Error: {ierr}")

    def get_description(self):
        print("What is it's description?")
        desc = input(">>>")
        return desc

    def print_busy_persons(self, busy_persons:list):

        if len(busy_persons) != 0:
            print("Some of the users were removed from the activity as they already"
                  " participate in an activity at the given time. Their ids are:")
            for i in range(0, len(busy_persons), 1):
                print(busy_persons[i], end="")
                if i != len(busy_persons) - 1:
                    print(", ", end="")
            print()

    def print_missing_persons(self, missing_persons:list):

        if len(missing_persons) != 0:
            print("Some of the users were removed from the activity as they "
                  "do not exist.. Their ids are:")
            for i in range(0, len(missing_persons), 1):
                print(missing_persons[i], end="")
                if i != len(missing_persons) - 1:
                    print(", ", end="")
            print()

    def print_person(self, pers):
        print(f"id: {pers.get_id()} || name: {pers.get_name()} || phone: {pers.get_phone()}")
    def print_activity(self, activ):
        print(f"id: {activ.get_id()} || start-time: {activ.get_datetime()},\n"
              f"end-time: {activ.get_endtime()}"
              f" description:{activ.get_description()} \n"
              f"id of associated people: {activ.get_people()}")

    def menu(self):
        menu_text = self.__get_option_a_text()
        print(menu_text)
        input_array = self.__get_menu_input()
        while input_array == None:
            input_array = self.__get_menu_input()

        if input_array[0] == "add":
            if input_array[1] == "person":
                name = self.get_name()
                phone = self.get_phone()
                try:
                    self._services.add_person(name, phone)
                except exceptions.RepositoryError as reperr:
                    print(f"Error: {reperr}")
            if input_array[1] == "activity":
                id_arr = self._get_id_input("add")
                while id_arr == None:
                    id_arr = self._get_id_input("add")

                print("Start time?")
                dt = self.get_datetime("add")
                print("End time?")
                et = self.get_datetime("add")
                desc = self.get_description()

                try:
                    busy_persons, missing_persons = self._services.add_activity(id_arr, dt, et, desc)
                    self.print_busy_persons(busy_persons)
                    self.print_missing_persons(missing_persons)
                except exceptions.RepositoryError as reperr:
                    print(f"Error: {reperr}")
        elif input_array[0] == "list":
            if input_array[1] == "persons":
                pass
                persons = self._services.list("persons")
                for pers in persons:
                    self.print_person(pers)
            elif input_array[1] == "activities":
                pass
                activities = self._services.list("activities")
                for activ in activities:
                    self.print_activity(activ)
        elif input_array[0] == "remove":
            target = input_array[1]
            id = input_array[2]
            try:
                self._services.remove(target, id)
            except exceptions.RepositoryError as reperr:
                print(f"Error: {reperr}")
        elif input_array[0] == "update":
            target = input_array[1]
            id = input_array[2]
            if target == "person":
                pers = self._services.get_person(id)
                name = self.get_name()
                phone = self.get_phone()
                name, phone = self._services.fill_none_person(pers, name, phone)
                try:
                    self._services.update_person(id, name, phone)
                except exceptions.RepositoryError as reperr:
                    print(f"Error: {reperr}")
            elif target == "activity":
                activ = self._services.get_activity(id)
                id_arr = self._get_id_input("update")
                print("Start time?")
                date_time = self.get_datetime("update")
                print("Start time?")
                end_time = self.get_datetime("update")
                description = self.get_description()
                id_arr, date_time, end_time, description = self._services.fill_none_activity(activ, id_arr, date_time, end_time, description)
                try:
                    busy_persons, missing_persons = self._services.update_activity(id, id_arr, date_time, end_time, description)
                    self.print_busy_persons(busy_persons)
                    self.print_missing_persons(missing_persons)
                except exceptions.RepositoryError as reperr:
                    print(f"Error: {reperr}")

class OptionB(OptionA):

    def __init__(self, serv):
        super().__init__(serv)

    def __get_option_b_text(self):
        lines = "_____________________________________\n"
        syntax_activity = ("Syntax activity:\n"
                           "add activity\n"
                           "remove activity <id>\n")

        option_b_text = lines + syntax_activity + lines
        return option_b_text

    def __get_menu_input(self):
        input_string = input(">>>")
        try:
            input_arr = self._validations.format_input_menu_array_string(input_string, self._validations.valid_optionb_input)
            return input_arr
        except exceptions.InputError as ierr:
            print(f"{ierr}")
            return None

    def menu(self):

        menu_text = self.__get_option_b_text()
        print(menu_text)
        input_array = self.__get_menu_input()
        while input_array == None:
            input_array = self.__get_menu_input()

        if input_array[0] == "add":
            if input_array[1] == "activity":
                id_arr = self._get_id_input("add")
                while id_arr == None:
                    id_arr = self._get_id_input("add")

                dt = self.get_datetime("add")
                desc = self.get_description()

                try:
                    busy_persons, missing_persons = self._services.add_activity(id_arr, dt, desc)
                    self.print_busy_persons(busy_persons)
                    self.print_missing_persons(missing_persons)
                except exceptions.RepositoryError as reperr:
                    print(f"Error: {reperr}")
        elif input_array[0] == "remove":
            target = input_array[1]
            id = input_array[2]
            try:
                self._services.remove(target, id)
            except exceptions.RepositoryError as reperr:
                print(f"Error: {reperr}")

class OptionC(OptionA):
    def __get_option_c_text(self):
        lines = "_____________________________________\n"
        syntax_activity = ("Syntax activity:\n"
                           "search person name\n"
                           "search person phone\n"
                           "search activity date-time\n"
                           "search activity description\n")

        option_c_text = lines + syntax_activity + lines
        return option_c_text

    def __get_menu_input(self):
        input_string = input(">>>")
        try:
            input_arr = self._validations.format_input_menu_array_string(input_string, self._validations.valid_optionc_input)
            return input_arr
        except exceptions.InputError as ierr:
            print(f"{ierr}")
            return None

    def menu(self):
        menu_text = self.__get_option_c_text()
        print(menu_text)
        input_array = self.__get_menu_input()
        while input_array == None:
            input_array = self.__get_menu_input()

        target = input_array[1]
        field = input_array[2]
        if target == "person":
            if field == "name":
                input_str = input("Name to search for:\n>>>")
            if field == "phone":
                input_str = input("Phone to search for:\n>>>")

            input_str = input_str.lower()
            input_str = input_str.strip()
            res = self._services.search(target, field, input_str)
            for pers in res:
                self.print_person(pers)
        elif target == "activity":
            if field == "description":
                input_str = input("Description to search for:\n>>>")
                input_str = input_str.lower()
                input_str = input_str.strip()
                res = self._services.search(target, field, input_str)
            if field == "date-time":
                print("Date-time to search for:")
                dt = self.get_datetime("add")
                res = self._services.search(target, field, dt)

            for activ in res:
                self.print_activity(activ)

class OptionD(OptionA):

    def __init__(self, serv):
        super().__init__(serv)

    def __get_option_d_text(self):
        lines = "_____________________________________\n"
        syntax_activity = ("(A.) Activities for a given date\n"
                           "(B.) Busiest days\n"
                           "(C.) Activities with a given person\n")


        option_d_text = lines + syntax_activity + lines
        return option_d_text

    def __get_menu_input(self):
        input_string = input(">>>")
        try:
            input_arr = self._validations.format_input_menu_array_string(input_string, self._validations.valid_optiond_input)
            return input_arr
        except exceptions.InputError as ierr:
            print(f"{ierr}")
            return None

    def __get_date_input(self):

        user_input = input("Please enter a date in the format 'YYYY-MM-DD':\n")
        user_input = user_input.strip()

        try:
            valid_date = datetime.strptime(user_input, '%Y-%m-%d').date()
            return valid_date
        except ValueError:
            raise exceptions.InputError("Not a valid date!")

    def get_date(self) -> datetime.date:

        dat = None
        while dat is None:
            try:
                dat = self.__get_date_input()
                return dat
            except exceptions.InputError as ierr:
                print(ierr)

    def get_int(self, message):
        try:
            integer = int(input(message))
            return integer
        except:
            raise exceptions.InputError("Invalid id!")

    def menu(self):
        menu_text = self.__get_option_d_text()
        print(menu_text)
        input_array = self.__get_menu_input()
        while input_array == None:
            input_array = self.__get_menu_input()

        if input_array[0] == "a":
            dat = self.get_date()
            res = self._services.search_date(dat)
            for activ in res:
                    self.print_activity(activ)
        elif input_array[0] == "b":
            res = self._services.busiest()
            for day, free_time in res.items():
                print(f"{day} -> {free_time}seconds free", end=", ")
            print()
        elif input_array[0] == "c":
            id = str(self.get_int("Enter ID:\n>>>"))
            res = self._services.search_with_person(id)
            for activ in res:
                    self.print_activity(activ)

class Ui:

    def __init__(self, type, pers_l, act_l):
        self.__validations = UI_Validations()
        try:
            self._undoserv = UndoService()
            self.__services = services.Services(type, pers_l, act_l, self._undoserv)
        except exceptions.RepositoryError as reperr:
            raise exceptions.PropertiesError(reperr)
        self.__option_a = OptionA(self.__services)
        self.__option_b = OptionB(self.__services)
        self.__option_c = OptionC(self.__services)
        self.__option_d = OptionD(self.__services)
    def __get_menu_text(self):
        lines = "_____________________________________\n"
        option_a = "(A.) Manage persons and activites\n"
        option_b = "(B.) Add/remove activities\n"
        option_c = "(C.) Search\n"
        option_d = "(D.) Statistics\n"
        option_e = "(E.) Undo\n"
        option_f = "(F.) Redo\n"
        option_g = "(G.) Exit\n"
        menu_text = (lines + option_a + option_b + option_c + option_d + option_e + option_f
                     + option_g + lines)
        return menu_text

    def __print_menu_text(self):
        menu_text = self.__get_menu_text()
        print(menu_text)

    def __get_menu_input(self):
        input_string = input(">>>")
        try:
            formatted_string = self.__validations.format_input_string(input_string)
            return formatted_string
        except exceptions.InputError as ierr:
            print(f"Error occured: {ierr}")
            return None

    def start(self):

        #self.__services.generate_start()

        app_running = True
        while app_running:
            self.__print_menu_text()
            option = self.__get_menu_input()
            while option == None:
                option = self.__get_menu_input()
            if option == "a":
                self.__option_a.menu()
            elif option == "b":
                self.__option_b.menu()
            elif option == "c":
                self.__option_c.menu()
            elif option == "d":
                self.__option_d.menu()
            elif option == "e":
                try:
                    result = self._undoserv.undo()
                    if result is None:
                        busy_persons, missing_persons = None, None
                    else:
                        busy_persons, missing_persons = result
                    if busy_persons is not None and missing_persons is not None:
                        self.__option_a.print_busy_persons(busy_persons)
                        self.__option_a.print_missing_persons(missing_persons)
                except exceptions.RepositoryError as reperr:
                    print(f"{reperr}")
                except exceptions.UndoRedoException as urerr:
                    print(f"{urerr}")
            elif option == "f":
                try:
                    result = self._undoserv.redo()
                    if result is None:
                        busy_persons, missing_persons = None, None
                    else:
                        busy_persons, missing_persons = result
                    if busy_persons is not None and missing_persons is not None:
                        self.__option_a.print_busy_persons(busy_persons)
                        self.__option_a.print_missing_persons(missing_persons)
                except exceptions.RepositoryError as reperr:
                    print(f"{reperr}")
                except exceptions.UndoRedoException as urerr:
                    print(f"{urerr}")
            elif option == "g":
                app_running = False