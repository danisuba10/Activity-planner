
class ActivityError(Exception):

    def __init__(self, msg):
        self.__msg = msg

    def __str__(self):
        return "Activity Exception: " + self.__msg


class PersonHasActivityException(ActivityError):

    def __init__(self):
        ActivityError.__init__(self, "User already added to activity!")

class ActivityAlreadyInRepo(ActivityError):

    def __init__(self):
        ActivityError.__init__(self, "Activity already exists in repo with this ID!")

class RepositoryError(Exception):

    def __init__(self, msg):
        self.__msg = msg

    def __str__(self):
        return "Repository error: " + self.__msg

class PersonAlreadyInRepo(RepositoryError):

    def __init__(self):
        RepositoryError.__init__(self, "User already exists with this ID!")

class InputError(Exception):

    def __init__(self, msg):
        self.__msg = msg

    def __str__(self):
        return "Input Exception: " + self.__msg

class ServiceError(Exception):

    def __init__(self, msg):
        self.__msg = msg

    def __str__(self):
        return "Service exception: " + self.__msg

class PropertiesError(Exception):

    def __init__(self, msg):
        self.__msg = msg

    def __str__(self):
        return "Property file exception: " + self.__msg


class UndoRedoException(Exception):

    def __init__(self, msg):
        self.__msg = msg

    def __str__(self):
        return "Undo exception: " + self.__msg