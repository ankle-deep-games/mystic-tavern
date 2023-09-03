### wiping the DB clean and starting over with dobby superuser
Fist, delete the `sqlite` database file on your computer and files within `tavern_app/migrations` besides the init file. Then run:

`python3 manage.py makemigrations`

`python3 manage.py migrate`

`python3 manage.py createsuperuser`

Or, all in 1 go:
`python3 manage.py makemigrations && python3 manage.py migrate && python3 manage.py createsuperuser`

Username: `dobby`

Email address: `enter blank`

Password: `socks`

Password (again): `socks`

This password is too short. It must contain at least 8 characters.
Bypass password validation and create user anyway? [y/N]: y `hit y`

Superuser created successfully.

`python3 manage.py runserver` to start the server again.

### log in to admin and seed data

http://127.0.0.1:8000/admin to log into dobby super user

http://127.0.0.1:8000/seed to seed the data

### create a game for testing
Once signed in as dobby - create a game http://127.0.0.1:8000/create/

In another tab visit http://127.0.0.1:8000/seed/game/:id to add 3 test users to the game

Refresh game lobby page to assign roles. Then start game.