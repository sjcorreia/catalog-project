#!/usr/bin/python

activate_this = '/var/www/catalog-project/vagrant/catalog/application.py'
with open(activate_this) as file_:
    exec(file_.read(), dict(__file__=activate_this))
