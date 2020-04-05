tinyurl
-------

A Django URL Shortener.


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

# copy adn edit private/production paramenters
cp tinyurl/settingslocal.py.example tinyurl/settingslocal.py

./manage migrate
./manage createsuperuser admin
./manage collectstatic
````

run
---

It will listen on :8000
````
./manage.py runserver
````

author
------

Giuseppe De Marco <giuseppe.demarco@unical.it>

credits
-------

GarrLab community
