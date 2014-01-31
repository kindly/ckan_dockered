#! /usr/bin/python
import uuid
import sys
from subprocess import call
import os
import urllib
import re

call(["/etc/init.d/postgresql", "start"])

if not os.path.exists('/etc/ckan/default/production.ini'):

    if len(sys.argv) == 1:
        page = urllib.urlopen('http://packaging.ckan.org/').read()
        name = sorted(re.findall('href="(python-ckan.*?)">', page))[-1]
        url = 'http://packaging.ckan.org/' + name
    else:
        url = sys.argv[1]

    call(["wget", url, '-O', '/tmp/ckan.deb'])
    call(["dpkg", '-i', '/tmp/ckan.deb'])
    call(["/usr/lib/ckan/default/bin/pip", 'install', '-e', 'git+https://github.com/okfn/ckan-service-provider.git#egg=ckanserviceprovider' ])
    call(['sed', '-i', 's/\$host/\$http_host/g', '/etc/nginx/sites-available/ckan'])

    password = str(uuid.uuid4()).replace('-','')
    os.rename('/etc/ckan/default/production.ini', '/etc/ckan/default/production.ini.old')

    with open('/etc/ckan/default/production.ini.old') as productionold, open('/etc/ckan/default/production.ini', 'w+') as productionew:
        for line in productionold:
            if  line.startswith('sqlalchemy.url'):
                line = 'sqlalchemy.url = postgresql://ckan:%s@localhost/ckan\n' % password
            if 'ckan.datastore.write_url' in line:
                line = 'ckan.datastore.write_url = postgresql://ckan_datastore_readwrite:%s@localhost/ckan_datastore\n' % password
            if 'ckan.datastore.read_url' in line:
                line = 'ckan.datastore.read_url = postgresql://ckan_datastore_readonly:%s@localhost/ckan_datastore\n' % password
            if 'solr_url' in line:
                line = 'solr_url = http://0.0.0.0:8983/solr \n'
            productionew.write(line)


    call(['mkdir', '-p', '/var/lib/ckan/default'])
    call(['chown', 'www-data', '-R', '/var/lib/ckan/'])
    call(['sed', '-i', 's/^#ofs.impl = pair.*/ofs.impl = pairtree/g', '/etc/ckan/default/production.ini'])
    call(['sed', '-i', 's/^ckan.datapusher.url.*/ckan.datapusher.url=http:\/\/0.0.0.0:8800/g', '/etc/ckan/default/production.ini'])
    call(['sed', '-i', 's/^#ckan.datapusher.url.*/ckan.datapusher.url=http:\/\/0.0.0.0:8800/g', '/etc/ckan/default/production.ini'])
    call(['sed', '-i', 's/^#ckan.storage_path.*/ckan.storage_path = \/var\/lib\/ckan\/default/g', '/etc/ckan/default/production.ini'])
    call(['sed', '-i', r's/^ckan.plugins.*/ckan.plugins = stats text_preview recline_preview datastore datapusher/g', '/etc/ckan/default/production.ini'])
    call(['sed', '-i', r's/^ckan.site_url.*/ckan.site_url = http:\/\/0.0.0.0\//g', '/etc/ckan/default/production.ini'])

    call(["sudo", "-u", "postgres", "psql", "-c", "alter user ckan password '%s'" % password])
    call(["sudo", "-u", "postgres", "psql", "-c", "alter user ckan_datastore_readwrite password '%s'" % password])
    call(["sudo", "-u", "postgres", "psql", "-c", "alter user ckan_datastore_readonly password '%s'" % password])

    call(["ckan", "db", "init"])

call(["service", "tomcat6", "restart"])
call(["service", "nginx", "restart"])
call(["service", "apache2", "restart"])
