from src.ui import ui
from src.unique_exceptions import exceptions

def get_settings(settings):
    type = settings.readline()
    type = type.replace(" ", "")
    type = type.split("=")
    type = type[1].strip("\n")
    person_path = settings.readline()
    person_path = person_path.strip("\n")
    person_path = person_path.replace(" ", "")
    person_path = person_path.strip('"')
    person_path = person_path.split("=")
    person_path = person_path[1].strip('"')

    activity_path = settings.readline()
    activity_path = activity_path.replace(" ", "")
    activity_path = activity_path.split("=")
    activity_path = activity_path[1].strip('"')
    activity_path = activity_path.strip("\n")

    return type, person_path, activity_path

if __name__ == "__main__":

    settings = open("settings.properties", "r")
    type, person_path, activity_path = get_settings(settings)

    try:
        ui = ui.Ui(type, person_path, activity_path)
        ui.start()
    except exceptions.PropertiesError as properr:
        print(properr)