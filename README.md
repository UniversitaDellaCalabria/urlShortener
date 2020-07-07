TinyURL
-------

A Django URL Shortener based on python [short_url](https://github.com/Alir3z4/python-short_url).

It uses a bit-shuffling approach is used to avoid generating consecutive, predictable URLs. However, the algorithm is deterministic and will guarantee that no collisions will occur.


Features
--------

- Full int18n support, available language english, italian
- CaPTCHA validation
- Rest-API with Basic and Token Authentication

Setup
-----

````
git clone https://gitlab.garrlab.it/peppelinux/tinyurl.git
cd tinyurl
virtualenv -p python3 env
source env/bin/activate
pip install -r requirements.txt
````

First run
---

````
cd tinyurl

# copy adn edit private/production paramenters
cp tinyurl/settingslocal.py.example tinyurl/settingslocal.py

./manage migrate
./manage createsuperuser admin
./manage collectstatic
````

Important parameters in `settingslocal.py`

````
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'uilbg9^$cs3427dhrppmgibuiof6yc-2_y#6sg^!mzmioo6=-l'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# do not use * in production, but the server hostname
ALLOWED_HOSTS = ['*']
FQDN = 'https://url.garrlab.it'

# See django documentation for a production ready RDBMS
DATABASES = {'...'}

# Change these in production use
ENCRYPTION_SECRET = b'secret'
ENCRYPTION_SALT = b'salt'

# se this to 0 to disable URL deletion
TINYURL_DURATION_DAYS = 12

# If True a landing page will be presented before redirecting to the original url
TINYURL_REDIRECT_LANDINGPAGE = True

# change this to have a different webpath to admin backend
ADMIN_PATH = 'gestione'
````

Run
---

It will listen on :8000
````
./manage.py runserver
````

Localization
------------

If you need additional languages add them in the variable `LANGUAGES`, in `settingslocal.py`.
Then create the `.po` files, edit them and compile. Follows an example with Espanish localization:

````
./manage.py makemessages -l es
./manage.py compilemessages -l es

````

API
---

OpenAPI v3 Schema
````
python manage.py generateschema --format openapi > schema.yml
````

Basic Authentication
````
curl -H 'Accept: application/json; indent=4' -u username:thatpassword http://127.0.0.1:8000/api/tinyurl/
````

Using Auth Tokens
````
# create a token linked to a user
./manage.py drf_create_token wert

# Use the token to get in
curl -X GET http://127.0.0.1:8000/api/tinyurl/ -H 'Authorization: Token 27b74b0a4dde305eda972e821de4e5823989cf39' -H 'Accept: applicaion/json; indent=4'

# POST data
curl -X POST -d "original_url=http://goal.it"  http://127.0.0.1:8000/api/tinyurl/ -H 'Authorization: Token 27b74b0a4dde305eda972e821de4e5823989cf39'
# returns
# {"original_url":"http://goal.it","shorten_url":"p9pdw","created":"2020-04-07T23:37:11.960616Z"}

# encode data url with cURL
export URL="https://smartcities-matera-clara.imaa.cnr.it/maplite/#/view/dashboard?mapID=300-50&x=16.620039939880375&y=40.65948038538384&zoom=14&baseMap=GOOGLE_SATELLITE"
curl -X POST --data-urlencode "original_url=$URL"  https://url.garrlab.it/api/tinyurl/ -H 'Authorization: Token 27b74b0a4dde305eda972e821de4e5823989cf39'
````

Play with Tokens
````
from rest_framework.authtoken.models import Token

token = Token.objects.create(user=...)
print(token.key)
````

API TroubleShooting

- "__Could not satisfy the request Accept header.__": remove `'Accept: applicaion/json; indent=4'` from request or see [Doc](https://www.django-rest-framework.org/api-guide/content-negotiation/)

Shortcuts
---------

A third-party website can use this link to let users have a easy shortcut to tinyurl
````
<button class="btn btn-primary"
        onclick="javascript:void(location.href='https://url.garrlab.it/?url='+encodeURIComponent(location.href))">
Tinify this website url
</button>
````

To create a url shortener dynamic link copy this message in your html
````
Bookmark the following <a href="javascript:void(location.href='https://url.garrlab.it/?url='+encodeURIComponent(location.href))">Tinify this URL</a>.
When you click the link in your favourites list, url.garrlab.it will provide a shortened link for the page you're on.
````


Gallery
-------

![Alt text](gallery/01.png)
--------------
![Alt text](gallery/02.png)
--------------
![Alt text](gallery/03.png)
--------------
![Alt text](gallery/04.png)

Dockerimage
-----------

Edit the admin user/pass/mail in Dockerfile.
Database connection paramenters can be configured as standard ENVironment variables, see `tinyurl/settingslocal.py.example`.

````
# please do not use standard distribution package
# apt install docker docker.io docker-compose

# use official docker repositories instead
apt-get install docker-ce docker-ce-cli containerd.io

cd urlshortener

# build the containers and run them
# sudo docker-compose up

# build without composer
docker image build --tag urlshortener:v1 .

# Run on localhost:8000
docker run -t -i -p 8000:8000 --name urlshortener urlshortener:v1
````

Author
------

Giuseppe De Marco <giuseppe.demarco@unical.it>

Credits
-------

- GarrLab Community
- Francesco Izzi (CNR IMAA)
- Elis Bertazzon (GARR)
