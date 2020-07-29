"# SchoolManagement Project" 

To get started...

- Clone the repository
- Make sure pip and python are installed in the system
- Type the following commands one by one in the command prompt or terminal 
    1. pip install -r requirements.txt    (To install all dependencies of the project)
    2. python manage.py makemigrations    (To create tables for all the models)
    3. python manage.py migrate           (To migrate the tables to the database)
    4. python population_script.py        (To populate the tables with some dummy data)
    5. python manage.py createsuperuser   (To create a superuser that can access the database directly)
       (Remember the email and password for later usage)
    6. python manage.py runserver         (To get the server up and running)
    
- Open any web browser and type the following url:
    http://localhost:2000 (To get to login page)
    http://localhost:2000/db (To get access to database after typing the credentials for superuser)
    
    
