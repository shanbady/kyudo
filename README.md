[![Stories in Ready](https://badge.waffle.io/mclumd/kyudo.png?label=ready&title=Ready)](https://waffle.io/mclumd/kyudo)
Kyudo
=====
**A research framework for goal driven query interfaces.**

## How to Run ##

In order to run the server locally, follow these steps:

1. Clone the repository into a working directory of your choice
2. Install the dependencies using pip install -r requirements.txt
    Note, it may be helpful to use a virtualenv
3. Set the following environment vars:

        $ export DJANGO_SETTINGS_MODULE=kyudo.settings.development
        $ export SECRET_KEY="super secret pass"
        $ export GOOGLE_OAUTH2_KEY="googlekey"
        $ export GOOGLE_OAUTH2_SECRET="googlesecret"

    Note that this app is enabled with Google OAuth login, you'll need to
    create your own Google credentials with the Google Developers console.

4. Create a database on postgres (on the localhost) called kyudo
    Note, you can set the envvars DB_NAME, DB_USER, DB_PASS etc.
5. Run the database migration:

        $ python kyudo/manage.py migrate

6. Run the server:

        $ make runserver

7. You should now be able to open a browser at http://127.0.0.1:8000

## Possible Parsers ##

- [Sempre](https://github.com/percyliang/sempre)
- DEANNA