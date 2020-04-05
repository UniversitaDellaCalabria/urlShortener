tinyurl
-------

A Django URL Shortener


setup
-----

````
git clone https://gitlab.garrlab.it/peppelinux/tinyurl.git
cd tinyurl
virtualenv -p python3 env
source env/bin/activate
pip install -r requirements.txt
````

first run
---

````
cd tinyurl
./manage migrate
./manage createsuperuser admin
````

run
---

It will listen on :8000
````
./manage.py runserver
````

