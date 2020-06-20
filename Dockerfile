# DOCKER-VERSION 17.10.0-ce
FROM python:slim
MAINTAINER Giuseppe De Marco <giuseppe.demarco@unical.it>

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV APPNAME urlshortener
ENV ADMINUSER admin
ENV ADMINPASS adminpass
ENV ADMINMAIL admin@example.org

# install dependencies
RUN pip install --upgrade pip

# install dependencies
RUN apt update \
    && apt install -y git locales \
                          libmariadbclient-dev \
                          net-tools \
                          curl iproute2

# RUN apt upgrade

# clean up
RUN apt clean && rm -rf /var/lib/apt/lists/*

RUN pip3 install virtualenv
RUN virtualenv -ppython3 ${APPNAME}.env
RUN . ${APPNAME}.env/bin/activate

# generate chosen locale
RUN sed -i 's/# it_IT.UTF-8 UTF-8/it_IT.UTF-8 UTF-8/' /etc/locale.gen
RUN locale-gen it_IT.UTF-8
# set system-wide locale settings
ENV LANG it_IT.UTF-8
ENV LANGUAGE it_IT
ENV LC_ALL it_IT.UTF-8

COPY . /${APPNAME}
WORKDIR /${APPNAME}/tinyurl
RUN pip3 install -r ../requirements.txt
RUN cp tinyurl/settingslocal.py.example tinyurl/settingslocal.py

## Add the wait script to the image
ADD https://github.com/ufoscout/docker-compose-wait/releases/download/2.7.2/wait /wait
RUN chmod +x /wait

# check with
# docker inspect --format='{{json .State.Health}}' urlshortener
HEALTHCHECK --interval=3s --timeout=2s --retries=1 CMD curl --fail http://localhost:8000/ || exit 1

RUN python manage.py migrate
RUN python manage.py shell -c "from django.contrib.auth import get_user_model; get_user_model().objects.filter(username='${ADMINUSER}').exists() or get_user_model().objects.create_superuser('${ADMINUSER}', '${ADMINMAIL}', '${ADMINPASS}')"
EXPOSE 8000
CMD /wait && python manage.py runserver 0.0.0.0:8000
