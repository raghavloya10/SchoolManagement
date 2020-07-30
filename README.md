# School Management Project

###### To get started...

- Clone the repository
- Make sure pip and python are installed in the system
- Type the following commands one by one in the command prompt or terminal having the project folder as the current working directory (cwd)
    1. __pip install -r requirements.txt__  (_To install all dependencies of the project_)
    2. __python manage.py makemigrations__    (_To create tables for all the models_)
    3. __python manage.py migrate__           (_To migrate the tables to the database)_
    4. __python population_script.py__        (_To populate the tables with some dummy_)
    5. __python manage.py createsuperuser__   (_To create a superuser that can access the database directly_)
       (_Remember the email and password for later usage_)
    6. __python manage.py runserver__         (_To get the server up and running_)
    
- Open any web browser and type the following url:
    http://localhost:8000 (To get to login page)
    http://localhost:8000/db (To get access to database after typing the credentials for superuser)
    
    
