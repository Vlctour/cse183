"""
This file defines actions, i.e. functions the URLs are mapped into
The @action(path) decorator exposed the function at URL:

    http://127.0.0.1:8000/{app_name}/{path}

If app_name == '_default' then simply

    http://127.0.0.1:8000/{path}

If path == 'index' it can be omitted:

    http://127.0.0.1:8000/

The path follows the bottlepy syntax.

@action.uses('generic.html')  indicates that the action uses the generic.html template
@action.uses(session)         indicates that the action uses the session
@action.uses(db)              indicates that the action uses the db
@action.uses(T)               indicates that the action uses the i18n & pluralization
@action.uses(auth.user)       indicates that the action requires a logged in user
@action.uses(auth)            indicates that the action requires the auth object

session, db, T, auth, and tempates are examples of Fixtures.
Warning: Fixtures MUST be declared with @action.uses({fixtures}) else your app will result in undefined behavior
"""

from py4web import action, request, abort, redirect, URL
from yatl.helpers import A
from .common import db, session, T, cache, auth, logger, authenticated, unauthenticated, flash
from py4web.utils.url_signer import URLSigner
from .models import get_user_email

url_signer = URLSigner(session)

@action('index')
@action.uses('index.html', db, auth.user)
def index():
    return dict(
        # For example...
        load_data_url = URL('load_data'),
        add_data_url = URL('add_data'),
        change_item_url = URL('change_item'),
        delete_item_url = URL('delete_item')
        # Add other things here.
    )

@action('load_data', method='GET')
@action.uses(db, session, auth.user)
def load_data():
    # Complete.
    # rows = [
    #     dict(id=1, item_name='doritos', purchased=False),
    #     dict(id=2, item_name='cheetos', purchased=False),
    # ]
    rows = db(
            db.shopping_list.user_email == get_user_email()
        ).select(
            orderby=[db.shopping_list.purchased, ~db.shopping_list.id]
        ).as_list()
    return dict(shopping_list=rows)

# You can add other controllers here.

# DAL QUERY SYNTAX
# db(query & query | query).select(projection | orderby | etc).as_list()
# .first()
# db(query).select(fields and orderby and limit of results)...
@action('add_data', method='POST')
@action.uses(db, session, auth.user)  # and something else, check later
def add_data():
    item_name = request.json.get('item_name')
    purchased = request.json.get('purchased')
    # insertions produces an id
    id = db.shopping_list.insert(item_name=item_name, purchased=purchased)
    return dict(id=id)

@action('change_item', method='POST')
@action.uses(db, session, auth.user)
def change_item():
    id = request.json.get('id')
    # apparently equivalent
    # item = db(db.shopping_list.id == id).select().first()
    item = db.shopping_list[id]
    assert item.user_email == get_user_email()
    item.purchased = not item.purchased
    # this updates the db
    item.update_record()
    # return dict(status=200)
    return dict(id=id, item_name=item.item_name, purchased=item.purchased, user_email=item.user_email)

@action('delete_item', method='POST')
@action.uses(db, session, auth.user)
def delete_item():
    id = request.json.get('id')
    item = db.shopping_list[id]
    assert item.user_email == get_user_email()
    db(db.shopping_list.id == id).delete()
    return dict(status=200)
