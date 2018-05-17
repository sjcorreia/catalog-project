from __future__ import print_function
from catalog.models import Base, User, Category, CatalogItem
from flask import Flask, jsonify, request, redirect
from flask import url_for, abort, g, render_template, flash
from flask import session as login_session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy import create_engine, asc
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
from flask import make_response
from io import StringIO
import requests
import json
import random
import string

# CLIENT_ID = json.loads(
#     open('client_secrets.json', 'r').read())['web']['client_id']

CLIENT_ID = "641303818172-2pr2brlfhib56rroe19ekendj8hd9p7s.apps.googleusercontent.com"

# engine = create_engine('sqlite:///catalog.db')
engine = create_engine('postgresql://catalog:udacity@localhost/catalog_db')

Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()
app = Flask(__name__)


def verify_password(username_or_token, password):
    # Try to see if it's a token first
    user_id = User.verify_auth_token(username_or_token)
    if user_id:
        user = session.query(User).filter_by(id=user_id).one()
    else:
        user = session.query(User).filter_by(
            username=username_or_token).first()
        if not user or not user.verify_password(password):
            return False
    g.user = user
    return True


# Login
@app.route('/login', methods=['POST', 'GET'])
def showLogin():
    if request.method == 'POST':
        if request.form['usr']:
            username = request.form['usr']
        if request.form['pwd']:
            password = request.form['pwd']

        if username is None or password is None:
            flash("Missing Arguments, not properly logged in")
        if session.query(User).filter_by(username=username).first() is \
           not None:
            # Existing User
            user = session.query(User).filter_by(
                username=username).first()
            if verify_password(user.username, password):
                # Password Verified
                login_session['username'] = user.username
                login_session['email'] = user.email
                # Add provider to login_session
                login_session['provider'] = 'internal'
                user_id = getUserID(user.email)
                if not user_id:
                    print("need to get user_id")
                login_session['user_id'] = user_id
                user_token = user.generate_auth_token(600)
                login_session['user_token'] = user_token
            else:
                # Password NOT verified
                flash("Access Denied! Username or Password Incorrect")
                return redirect('/login')
        else:
            flash("Please create a new user account")
            return redirect('/newuseraccount')

        flash("You are logged in as %s" % request.form['usr'])
        return redirect('/catalog')
    else:
        state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                        for x in range(32))
        login_session['state'] = state
        # return "The current session state is %s" % login_session['state']
        return render_template('login.html', STATE=state)


# Handles the OAuth from Google
@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    response, content = h.request(url, 'GET')
    result = json.loads(content.decode('latin1'))
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print("Token's client ID does not match app's.")
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']
    # Add provider to the login_session
    login_session['provider'] = 'google'

    # see if user exists, if it doesn't make a new one
    user_id = getUserID(data["email"])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    user = getUserInfo(user_id)
    user_token = user.generate_auth_token(600)
    login_session['user_token'] = user_token
    print("User token: %s" % user_token)

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: '
    output += '150px;-webkit-border-radius: '
    output += '150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print("done!")
    return output


# User Helper Functions
def createUser(login_session):
    if login_session['provider'] == 'google':
        newUser = User(username=login_session['username'], email=login_session[
                       'email'], picture=login_session['picture'])
        session.add(newUser)
        session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except NoResultFound:
        return None


# DISCONNECT - Revoke a current user's token and reset their login_session
@app.route('/gdisconnect')
def gdisconnect():
    # Only disconnect a connected user.
    access_token = login_session.get('access_token')
    if access_token is None:
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    if result['status'] == '200':
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        response = make_response(json.dumps(
            'Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


# Logout
@app.route('/logout')
@app.route('/disconnect')
def disconnect():
    if 'provider' in login_session:
        if login_session['provider'] == 'google':
            gdisconnect()
            del login_session['gplus_id']
            del login_session['access_token']
            del login_session['picture']
        del login_session['user_token']
        del login_session['username']
        del login_session['email']
        del login_session['user_id']
        del login_session['provider']
        flash("You have successfully been logged out.")
        return redirect(url_for('showCatalog'))
    else:
        flash("You were not logged in")
        return redirect(url_for('showCatalog'))


@app.route('/')
@app.route('/catalog')
def showCatalog():
    categories = session.query(Category).order_by(asc(Category.name))
    items = session.query(CatalogItem).order_by(asc(CatalogItem.name)).limit(5)
    return render_template('categories.html',
                           categories=categories, items=items)


@app.route('/catalog.json')
def categoryJSON():
    categories = session.query(Category).all()
    items = session.query(CatalogItem).order_by(asc(CatalogItem.name))
    categoryList = []
    for category in categories:
        categoryList.append(category.serialize)
        item_list = []
        for item in items:
            if item.category.name == category.name:
                item_list.append(item.serialize)
        categoryList.append({"items": item_list})
    completeJson = {"Category": categoryList}
    return jsonify(completeJson)


# Show a Catalog Category
@app.route('/catalog/<string:category>/items')
def showItemsInCategory(category):
    category_obj = session.query(Category).filter_by(name=category).one()
    items = session.query(CatalogItem).filter_by(
        category_id=category_obj.id).all()
    return render_template('catalog.html', category=category_obj, items=items,
                           session=login_session)


# View a Catalog Item
@app.route('/catalog/<string:category>/<string:item>')
def viewCatalogItem(category, item):
    itemToDisplay = session.query(CatalogItem).filter_by(name=item).one()
    categoryToDisplay = session.query(Category).filter_by(name=category).one()
    return render_template('viewcatalogitem.html', category=categoryToDisplay,
                           item=itemToDisplay, session=login_session)


# Add a Catalog Item
@app.route('/catalog/new', methods=['GET', 'POST'])
def addNewCatalogItem():
    if ('user_token' in login_session and
            verify_password(login_session['user_token'], None)):
        categories = session.query(Category).all()
        if request.method == 'POST':
            newItem = CatalogItem()
            if request.form['name']:
                newItem.name = request.form['name']
            if request.form['description']:
                newItem.description = request.form['description']
            if request.form['category']:
                newItem.category_id = request.form['category']
            newItem.user_id = login_session['user_id']
            session.add(newItem)
            session.commit()
            flash('Catalog Item %s Successfully Added' % newItem.name)
            return redirect(url_for('showCatalog'))
        else:
            return render_template('newcatalogitem.html',
                                   categories=categories)
    else:
        flash("Please Log In")
        return redirect('/login')


# Edit a Catalog Item
@app.route('/catalog/<string:item>/edit', methods=['GET', 'POST'])
def editCatalogItem(item):
    if ('user_token' in login_session and
            verify_password(login_session['user_token'], None)):
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
    else:
        flash("Please Log In")
        return redirect('/login')


# Delete a Catalog Item
@app.route('/catalog/<string:item>/delete', methods=['GET', 'POST'])
def deleteItem(item):
    if ('user_token' in login_session and
            verify_password(login_session['user_token'], None)):
        itemToDelete = session.query(CatalogItem).filter_by(name=item).one()
        if request.method == 'POST':
            session.delete(itemToDelete)
            session.commit()
            flash('Catalog Item Successfully Deleted')
            return redirect(url_for('showCatalog'))
        else:
            return render_template('deletecatalogitem.html', item=itemToDelete)
    else:
        flash("Please Log In")
        return redirect('/login')


# Create a new user account
@app.route('/newuseraccount', methods=['POST', 'GET'])
def newUserAccount():
    if request.method == 'POST':
        if request.form['usr']:
            username = request.form['usr']
            try:
                user = session.query(User).filter_by(username=username).one()
                print("username already exists in db")
                flash('Username already exists, please choose another')
                return render_template('createnewuser.html')
            except NoResultFound:
                print("username does not exists in db")
        if request.form['email']:
            email = request.form['email']
            try:
                user = session.query(User).filter_by(email=email).one()
                print("email already exists in db")
                flash('This E-Mail address is already associated with \
                another account, please choose another one')
                return render_template('createnewuser.html')
            except NoResultFound:
                print("email does not exists in db")
        if request.form['pwd']:
            password = request.form['pwd']
        if username is None or password is None or email is None:
            flash("Missing Arguments, Please Enter all Information")
        user = User(username=username)
        user.email = email
        user.hash_password(password)
        session.add(user)
        session.commit()
        flash('New User Account Created! Please Log-In')
        return redirect('/login')
    else:
        return render_template('createnewuser.html')


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
