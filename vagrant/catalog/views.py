from models import Base, User, Category, CatalogItem
from flask import Flask, jsonify, request, url_for, abort, g, render_template
from flask import session as login_session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine, asc

from flask_httpauth import HTTPBasicAuth
import json

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
from flask import make_response
import requests

auth = HTTPBasicAuth()


engine = create_engine('sqlite:///catalog.db')

Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()
app = Flask(__name__)


# Login

# Logout


@app.route('/')
@app.route('/catalog')
def showCatalog():
    categories = session.query(Category).order_by(asc(Category.name))
    return jsonify(categories=[c.serialize for c in categories])


@app.route('/catalog/JSON')
def categoryJSON():
    categories = session.query(Category).all()
    return jsonify(categories=[c.serialize for c in categories])


# Add a Catalog Category

# Edit a Catalog Category

# Delete a Catalog Category

# Show a Catalog Category
@app.route('/catalog/<string:category>')
def showItemsInCategory(category):
    return "Items in category: %s" % category

# Add a Catalog Item

# Edit a Catalog Item

# Delete a Catalog Item


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
