FROM ubuntu:12.04

MAINTAINER David Raznick

RUN  echo "deb http://archive.ubuntu.com/ubuntu precise main universe multiverse restricted" > /etc/apt/sources.list && \
     apt-get update && apt-get install build-essential sudo python-dev python-setuptools python-pycurl python-apt vim -y &&\
     easy_install pip && \
     pip install ansible

ADD setupdb.yml /tmp/setupdb.yml
ADD inventory /tmp/inventory
ADD dbprivs.sql /tmp/dbprivs.sql

WORKDIR /tmp

RUN ansible-playbook -c local -i inventory setupdb.yml

ADD setupweb.yml /tmp/setupweb.yml

RUN ansible-playbook -c local -i inventory setupweb.yml

ADD startup.py /usr/lib/ckan/startup.py
ADD startup.sh /usr/lib/ckan/startup.sh

WORKDIR /usr/lib/ckan/

CMD ["bash", "startup.sh"]
