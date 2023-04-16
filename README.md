# UIKTP

## Project setup
To setup the project, first create a virtual environment using the following commands:
    
    python -m venv furryfeet_env

Then, activate the created env with the command

    furryfeet_env\Scripts\activate  

Finally, run the following command to install all the needed dependencies that are needed for this project:

    pip install -r requirements.txt

Important! **Do not commit the furryfeet_env directory.** It is set by default to be ignored by git.

Before starting to work on the project, run the following command to apply all migrations that have been made previously:

    python manage.py migrate

For more info on Django, visit https://docs.djangoproject.com/en/4.2/
