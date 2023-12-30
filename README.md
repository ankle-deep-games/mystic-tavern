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

Superuser created successfully.

`python3 manage.py runserver` to start the server again.

### log in to admin and seed data

http://127.0.0.1:8000/admin to log into dobby super user

http://127.0.0.1:8000/seed to seed the data

### create a game for testing
Once signed in as dobby - create a game http://127.0.0.1:8000/create/

In another tab visit http://127.0.0.1:8000/seed/game/:id to add 3 test users to the game

Refresh game lobby page to assign roles. Then start game.

## Deployment steps

Region: us-west-1

### EC2 Security Group

3 inbound rules
- SSH port 22 0.0.0.0/0
- HTTP port 80 0.0.0.0/0
- HTTP port 80 ::/0

### Create EC2 Instance
- Ubuntu image
- Instance type t2.micro
- no key pair
- select created security group
- 30GB storage

### SSH connect to instance to install packages
- `sudo apt-get update`
- `sudo apt-get upgrade` --> y --> hit enter when prompted with outdated libraries screen
- `python3 --version`
- `sudo apt-get install python3-venv`
- `python3 -m venv env`
- `source env/bin/activate`
- `pip3 install django`
- `git clone https://github.com/philyawj/ankle-deep-games.git`
    - username: philyawj
    - password: access token
- `sudo apt-get install -y nginx` --> hit enter
- `pip install gunicorn`
- `pip list` to verify packages
- visit 52.53.149.134 and see nginx has been installed
- `sudo apt-get install supervisor` -> hit enter
- `cd /etc/supervisor/conf.d/`
- `sudo touch gunicorn.conf`
- `sudo nano gunicorn.conf`

```
[program:gunicorn]
directory=/home/ubuntu/ankle-deep-games
command=/home/ubuntu/env/bin/gunicorn --workers 3 --bind unix:/home/ubuntu/ankle-deep-games/app.sock adg.wsgi:application
autostart=true
autorestart=true
stderr_logfile=/var/log/gunicorn/gunicorn.err.log
stdout_logfile=/var/log/gunicorn/gunicorn.out.log

[group:guni]
programs:gunicorn
```
- control + O to save and control + x to exit
- `sudo mkdir /var/log/gunicorn`
- `sudo supervisorctl reread`
- `sudo supervisorctl update`
- `sudo supervisorctl status`
- `cd ../..` into `/etc`
- `sudo nano nginx.conf` --> change user on line 1 to `user root;`
- `cd sites-available`
- `sudo touch django.conf`
- `sudo nano django.conf`

```
server {
    listen 80;
    server_name 54.177.98.169;

    location /static/ {
        alias /home/ubuntu/ankle-deep-games/tavern_app/static/;
    }
    location /static/admin/ {
        alias /home/ubuntu/env/lib/python3.10/site-packages/django/contrib/admin/static/admin/;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/home/ubuntu/ankle-deep-games/app.sock;
    }
}
```

- `sudo nginx -t`
- `sudo ln django.conf /etc/nginx/sites-enabled`
- `sudo service nginx restart`