### helpful commands

- TBD

### wiping the DB clean and starting over with dobby superuser
Fist, delete the `sqlite` database file on your computer. Then run:

`python3 manage.py makemigrations`

`python3 manage.py migrate`

`python3 manage.py createsuperuser`

Username (leave blank to use 'jordan'): `dobby`
Email address: `enter blank`
Password: `socks`
Password (again): `socks`
This password is too short. It must contain at least 8 characters.
Bypass password validation and create user anyway? [y/N]: y `hit y`
Superuser created successfully.

Finally, `python3 manage.py runserver` to start the server again.