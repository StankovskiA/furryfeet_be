# UIKTP

## Project setup
To setup the project, first create a virtual environment using the following commands:
    
    python -m venv furryfeet_env

Then, activate the created env with the command

    furryfeet_env/bin/activate  # Unix/Mac

    furryfeet_env/Scripts/activate  # Windows

Finally, run the following command to install all the needed dependencies that are needed for this project:

    pip install -r requirements.txt

Important! **Do not commit the furryfeet_env directory.** It is set by default to be ignored by git.

Before starting to work on the project, run the following command to apply all migrations that have been made previously:

    python manage.py migrate

For more info on Django, visit https://docs.djangoproject.com/en/4.2/ 

## Running the project

Retrieve secret key from team leads and insert it furryfeet_be\settings.py 

    SECRET_KEY = "XXXXXX"

Make sure that you are in the furryfeet_be subfolder 
    
    cd furryfeet_be

To start the local server run:
    
    python manage.py runserver

To run on a specific port run:

    python manage.py runserver 8080