from models import Base, User, Category, CatalogItem
from flask import Flask, jsonify, request, redirect
from flask import url_for, abort, g, render_template
from flask import session as login_session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine, asc

from flask_httpauth import HTTPBasicAuth
import json
import random
import string
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
@app.route('/login')
def showLogin():
    # state = ''.join(random.choice(string.ascii_uppercase + string.digits)
    #                 for x in xrange(32))
    # login_session['state'] = state
    # return "The current session state is %s" % login_session['state']
    # return render_template('login.html', STATE=state)
    return "Placeholder for LOGIN"


# Logout
@app.route('/logout')
@app.route('/disconnect')
def disconnect():
    return "Placeholder for logout"


@app.route('/')
@app.route('/catalog')
def showCatalog():
    categories = session.query(Category).order_by(asc(Category.name))
    return render_template('categories.html', categories=categories)


@app.route('/catalog.json')
def categoryJSON():
    # categories = session.query(Category).all()
    # return jsonify(categories=[c.serialize for c in categories])
    items = session.query(CatalogItem).order_by(asc(CatalogItem.name))
    return jsonify(items=[i.serialize for i in items])


# Show a Catalog Category
@app.route('/catalog/<string:category>/items')
def showItemsInCategory(category):
    category_obj = session.query(Category).filter_by(name=category).one()
    items = session.query(CatalogItem).filter_by(
        category_id=category_obj.id).all()
    return render_template('catalog.html', category=category_obj, items=items)
    # return "Items in category: %s" % category


# View a Catalog Item
@app.route('/catalog/<string:category>/<string:item>')
def viewCatalogItem(category, item):
    return "View Item %s from category %s" % (item, category)


# Add a Catalog Item
@app.route('/catalog/new')
def addNewCatalogItem():
    categories = session.query(Category).all()
    return render_template('newcatalogitem.html', categories=categories)


# Edit a Catalog Item
@app.route('/catalog/<string:item>/edit', methods=['GET', 'POST'])
def editCatalogItem(item):
    categories = session.query(Category).all()
    itemToEdit = session.query(CatalogItem).filter_by(
        name=item).one()
    if request.method == 'POST':
        if request.form['name']:
            itemToEdit.name = request.form['name']
        if request.form['description']:
            itemToEdit.description = request.form['description']
        if request.form['category']:
            itemToEdit.category_id = request.form['category']
        session.add(itemToEdit)
        session.commit()
        return redirect(url_for('showCatalog'))
    else:
        return render_template('editcatalogitem.html', item=itemToEdit,
                               categories=categories)


# Delete a Catalog Item
@app.route('/catalog/<string:item>/delete')
def deleteItem(item):
    itemToDelete = session.query(CatalogItem).filter_by(name=item).one()
    return render_template('deletecatalogitem.html', item=itemToDelete)


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
