# Contingent  ![contingent](contingent.jpg) 

## About project
The repository contains the server-side implementation of the Contingent project.

##### What is the Contingent?
Contingent is a project for automation tasks of university workers, which helps to make their work easier. Оne of the main tasks of working with data at universities is the task of maintaining the university's student body - the contingent. The processes of obtaining, processing and using academic data at Kuban State University are quite hard and poorly automated. Contingent is an effective solution of difficulties with working university data, which helps to keep all necessary information in one place and provides convenient tools for working with it.

##### Who is the target audience of the Contingent?
Contingent was created for university administrative staff or for university structures which can be faculty, the mobilisation departments or the human resources department.

##### Which problems does the Contingent solve?
The currently used analogues have disadvantages, for example:
- local storage limitations
- difficulties with importing data (data is keeps in several files in different formats)
- desktop-only access
- requires highly trained staff
- long and complex integration process
- necessity of hiring an external specialists for installation and support the sistem
The Contingent don't have the disadvantages of analog systems and uses its own effective solutions based on modern technologies.

### Technology Stack
The server part of the project was made with using popular and stable technologies:
- To provide users authentication and authorisation in service used **JWT** standard with refresh and access tokens.
- **Python** was chosen because of its simpleness, which increases the speed of development. Also **Python** is one of the most suitable languages for web-development.
- To implement the API, **FastAPI** framework was chosen, which stand out among its analogues due its advantages. One of the important advantage is the height efficiency provided by asynchrony, which is especially important for processing constantly updated academic data.
- To provide work with database was used **SQLAlchemy**, which uses Python to work with the database. Using **SQLAlchemy**, we aren't limited to a single database such as postgres and we can switch it if necessary. **SQLAlchemy** also has an asynchronous engine, which is important for maintaining the architecture of the project.
- **Docker** was used to create isolated environments for development and testing processes.

### Functionality
For every functionality of project was created necessity CRUD operations
- *Students cards*. Each student card is a separate unit of information and includes several structured sections: person data, contacts, data on education, benefits, military service data and data on current studies.
- *Import students cards with one file*. At the moment, student data is keeps in several files in different formats. In the Contingent project, the user needs to fill one excel file, which contains a list of student cards.
- *Student lists*. The one of the main functionality of the project is the creation of students lists that support filtering by many parameters. The following lists are currently available: the Named list - keeps all information about students, the Current Numerical list - shows calculated data on numer of students in study catigories, the Planned numerical list - contains information on planned directions, the number of courses, groups and subgroupts.
- *Structures*. The Structure in Contingent is predefined data about faculties that are used to fill in data about groups, subgroups and other objects of study in university.
- *Authentication and authorisation*. The project implements JWT authentication and authorisation which allow to set the access level to functions by user role.

## Quick start 

```bash
git clone https://github.com/pococonut/Contingent.git
```

Fill the **.env** and **docker-compose.yaml** files. You can find the examples in:
- app/.env.example
- docker/docker-compose_example.yaml

```bash
cd docker
docker compose --env-file ../app/.env up --build
```

Access API documentation at: http://127.0.0.1:8000/docs