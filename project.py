from flask import (Flask,
                   request,
                   redirect,
                   render_template,
                   url_for,
                   flash,
                   jsonify,
                   abort,
                   g,
                   session)
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, CategoryItem, User
from random import randint
from flask_httpauth import HTTPBasicAuth
from flask import session as login_session
import random
import string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests
from functools import wraps

auth = HTTPBasicAuth()
# Flask Instance
app = Flask(__name__)

# GConnect Client Id
CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Item Catalog Application"

# Connect to Database
engine = create_engine('sqlite:///itemcatelogwithusers.db')
Base.metadata.bind = engine
# Creating session
DBSession = sessionmaker(bind=engine)
session = DBSession()


# Flask login decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in login_session:
            return redirect('/login')
        return f(*args, **kwargs)
    return decorated_function


# Login route and creates anti-forgery token
@app.route('/login', methods=['GET', 'POST'])
def login():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    '''Users can login if he/she logged in before
     using google account just by entering email.'''
    if request.method == 'POST':
        email = request.form['Email']
        exists = session.query(User) \
            .filter_by(email=email).scalar() is not None
        if exists:
            user = session.query(User).filter_by(email=email).one()
            login_session['username'] = user.name
            login_session['picture'] = user.picture
            login_session['email'] = email
            flash("you are now logged in as %s" % login_session['username'])
            return redirect('categories')
        else:
            flash("Wrong E-mail")
    return render_template('login.html', STATE=state)


# GConnect
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
    result = json.loads(h.request(url, 'GET')[1])
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
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None \
    and gplus_id == stored_gplus_id:
        response = make_response(
            json.dumps('Current user is already connected.'), 200)
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

    # see if user exists, if it doesn't make a new one.

    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    return output


# GDisconnect - Revokes current user's token and resets their login session
@app.route('/gdisconnect')
def gdisconnect():
    access_token = login_session.get('access_token')
    if (access_token is None and 'username' not in login_session):
        print 'Access Token is None'
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    elif (access_token is None and 'username' in login_session):
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        return redirect(url_for('categories'))

    print 'In gdisconnect access token is %s', access_token
    print 'User name is: '
    print login_session['username']
    url = 'https://accounts.google.com/o \
    /oauth2/revoke?token=%s' % login_session['access_token']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print 'result is '
    print result
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return redirect(url_for('categories'))
    else:
        response = make_response(
            json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


# Helper functions to create and get user info
def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session[
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
    except:
        return None


# Route to homepage
@app.route('/')
@app.route('/categories')
def categories():
    categories = session.query(Category).all()
    recentItems = session.query(CategoryItem) \
        .order_by(CategoryItem.id.desc()).limit(6)
    if 'username' not in login_session:
        return render_template(
            'publicitemcatalog.html',
            categories=categories, recentItems=recentItems)
    else:
        return render_template(
            'itemcatalog.html',
            categories=categories, recentItems=recentItems)


# Page displays list of specific category items
@app.route('/categories/<int:category_id>/')
def categoryItems(category_id):
    categories = session.query(Category).all()
    category = session.query(Category).filter_by(id=category_id).one()
    items = session.query(CategoryItem) \
        .filter_by(category_id=category_id)
    count = session.query(CategoryItem) \
        .filter_by(category_id=category_id).count()
    if 'username' not in login_session:
        return render_template(
            'publicitemlist.html',
            category=category,
            items=items, categories=categories, count=count)
    else:
        return render_template(
            'itemlist.html',
            category=category,
            items=items, categories=categories, count=count)


# Displays a specific item description
@app.route('/categories/<int:category_id>/<int:item_id>/')
def itemDescription(category_id, item_id):
    item = session.query(CategoryItem) \
        .filter_by(category_id=category_id, id=item_id).first()
    if 'username' not in login_session:
        return render_template(
            'publicdescription.html',
            item=item, category_id=category_id, item_id=item_id)
    else:
        return render_template(
            'description.html',
            item=item, category_id=category_id, item_id=item_id)


# Add new Item
@app.route('/additem', methods=['GET', 'POST'])
@login_required
def addNewItem():
    categories = session.query(Category).all()
    if request.method == 'POST':
        category = session.query(Category) \
            .filter_by(name=request.form['Category']).first()
        newItem = CategoryItem(
            name=request.form['Title'],
            description=request.form['Description'],
            user_id=login_session['user_id'], category=category)
        session.add(newItem)
        session.commit()
        flash("New Item Added!")
        return redirect(url_for('categoryItems', category_id=category.id))
    else:
        return render_template('additem.html', categories=categories)


# Edit a specific Item
@app.route(
    '/categories/<int:category_id>/<int:item_id>/edititem',
    methods=['GET', 'POST'])
@login_required
def editItem(category_id, item_id):
    item = session.query(CategoryItem) \
        .filter_by(category_id=category_id, id=item_id).first()
    category = session.query(Category).filter_by(id=category_id).one()
    if item.user_id != login_session['user_id']:
        return " < script > function myFunction() \
        {alert('You are not authorized to edit this item.\
               Please create your own item in order edit.');} \
            < /script > < body onload = 'myFunction()'' > "

    if request.method == 'POST':
        if request.form['Title']:
            item.name = request.form['Title']
            item.description = request.form['Description']
        session.add(item)
        session.commit()
        flash("Item Edited!")
        return redirect(url_for(
            'itemDescription',
            category_id=category_id, item_id=item_id))
    else:
        return render_template(
            'edititem.html',
            item=item, category=category,
            category_id=category_id, item_id=item_id)


# Deletes a specific Item
@app.route(
    '/categories/<int:category_id>/<int:item_id>/deleteitem',
    methods=['GET', 'POST'])
@login_required
def deleteItem(category_id, item_id):
    item = session.query(CategoryItem) \
        .filter_by(category_id=category_id, id=item_id).first()
    category = session.query(Category).filter_by(id=category_id).one()
    if item.user_id != login_session['user_id']:
        return " < script > function myFunction() {alert('You are not\
        authorized to delete this item.\
        Please create your own item in order to delete.\
        ');}</script><body onload='myFunction()'' > "
    if request.method == 'POST':
        session.delete(item)
        session.commit()
        flash("Item Deleted!")
        return redirect(url_for('categoryItems', category_id=category_id))
    else:
        return render_template(
            'deleteitem.html',
            category_id=category_id, item_id=item_id)


# JSON
@app.route('/catalog.json')
def catalogJSON():
    items = session.query(CategoryItem).all()
    return jsonify(CategoryItems=[i.serialize for i in items])

if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.run(host='0.0.0.0', port=5000)
    app.debug = True
