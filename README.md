# 💻 Assignment 08 - Layered Architecture I
## Requirements
- Provide a menu-driven console-based user interface. Implementation details are up to you
- Employ layered architecture and classes
- Have at least 20 procedurally generated items **for each domain class** in your application at startup (e.g., at least 20 students, 20 disciplines and 20 grades)
- Provide specifications and **[PyUnit test cases](https://realpython.com/python-testing/)** for all non-UI classes and methods for the first functionality
- Implement and use your own exception classes.
- Deadline for maximum grade is **week 11**.

## Bonus possibility (0.1p, deadline week 11)
- 95% unit test code coverage for all modules except the UI (use *PyCharm Professional*, the *[coverage](https://coverage.readthedocs.io/en/coverage-5.3/)* or other modules)

## Bonus possibility (0.2p, deadline week 11)
- Implement a graphical user interface, in addition to the required menu-driven UI
- The program can be started with either UI

## Problem Statements
### 5. Activity Planner
The following information is stored in a personal activity planner:
- **Person**: `person_id`, `name`, `phone_number`
- **Activity**: `activity_id`, `person_id` - list, `date`, `time`, `description`

Create an application to:
1. Manage persons and activities. The user can add, remove, update, and list both persons and activities.
2. Add/remove activities. Each activity can be performed together with one or several other persons, who are already in the user’s planner. Activities must not overlap (user cannot have more than one activity at a given time).
3. Search for persons or activities. Persons can be searched for using name or phone number. Activities can be searched for using date/time or description. The search must work using case-insensitive, partial string matching, and must return all matching items.
4. Create statistics:
    - Activities for a given date. List the activities for a given date, in the order of their start time.
    - Busiest days. This will provide the list of upcoming dates with activities, sorted in ascending order of the free time in that day (all intervals with no activities).
    - Activities with a given person. List all upcoming activities to which a given person will participate.



# 💻 Assignment 09 - Layered Architecture II
## Requirements
There are some new requirements for the program you've implemented for **A8**. 

1. Implement persistent storage for all entities using file-based repositories. For each entity, you will implement a text-file based repository and a binary-file based repository (using [Pickle](https://docs.python.org/3/library/pickle.html)). These will work alongside the existing repository that stores entities in memory. The program must work the same way using in-memory repositories, text-file repositories and binary file repositories. You can use inheritance in order to reuse existing repository source code.
2. Implement a `settings.properties` file to configure the application. The decision of which repositories are employed, as well as the location of the repository input files will be made in the program’s `settings.properties` file. An example is below:

    a. `settings.properties` for working with repositories that store entities in memory (in this case there are no input files):
    ```
    repository = inmemory
    cars = “”
    clients = “”
    rentals = “”
    ```
    b. `settings.properties` for working with repositories that store entities to binary files:
    ```
    repository = binaryfiles
    cars = “cars.pickle”
    clients = “clients.pickle”
    rentals = “rentals.pickle”
    ```
    
    **NB!** If your solution to **A8** uses layered architecture properly, these are the only places where source code needs to change:
    - *Repository layer* – for implementing the required code.
    - *Application start module* – to load the properties file and start the required repositories.

3. Implement unlimited undo/redo functionality using the [Command design pattern](https://refactoring.guru/design-patterns/command), which ensures a memory-efficient implementation of undo/redo operations. Each step will undo/redo the previous operation performed by the user. Undo/redo operations must cascade (e.g., deleting a student must also delete their grades; undoing the deletion must restore all deleted objects).

deadline for maximum grade is **week 12**.
