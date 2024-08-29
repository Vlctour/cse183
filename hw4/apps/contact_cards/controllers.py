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
from .models import get_user_email


@action('index')
@action.uses('index.html', db, session, auth.user)
def index():
    return dict(
        get_contacts_url = URL('get_contacts'),
        add_contacts_url = URL('add_contacts'),
        update_contacts_url = URL('update_contacts'),
        file_upload_url = URL('file_upload'),
        del_contacts_url = URL('del_contacts'),
        # Complete. 
    )

@action('get_contacts', method="GET")
@action.uses(db, session, auth.user)
def get_contacts():
    contacts = db(db.contact_card.user_email == get_user_email()
                  ).select().as_list()
    return dict(contacts=contacts)

# You can add more methods. 
@action('add_contacts')
@action.uses(db, session, auth.user)
def add_contacts():
    id = db.contact_card.insert(user_email=get_user_email,
                            contact_name="",
                            contact_affiliation="",
                            contact_description="",
                            contact_image="https://bulma.io/assets/images/placeholders/96x96.png")
    return dict(id=id,
                user_email=get_user_email,
                contact_name="",
                contact_affiliation="",
                contact_description="",
                contact_image="https://bulma.io/assets/images/placeholders/96x96.png")

@action('update_contacts', method="POST")
@action.uses(db, session, auth.user)
def update_contacts():
    id = request.json.get('id')
    field = request.json.get('field')
    field_data = request.json.get('field_data')
    # print("THIS IS FIELD", field)
    item = db.contact_card[id]
    assert item.user_email == get_user_email()
    item[field] = field_data
    item.update_record()
    return dict(status=200)

@action('file_upload', method="POST")
@action.uses(db, session, auth.user)
def file_upload():
    # file_name = request.params.get("file_name")
    # file_type = request.params.get("file_type")
    id = request.json.get("id")
    item = db.contact_card[id]
    assert item.user_email == get_user_email()
    contact_image = request.json.get("contact_image")
    item.contact_image = contact_image
    item.update_record()
    # Diagnostics
    # print("Uploaded", file_name, "of type", file_type)
    # print("Content:", uploaded_file.read())
    return dict(status=200)

@action('del_contacts', method="POST")
@action.uses(db, session, auth.user)
def del_contacts():
    id = request.json.get('id')
    item = db.contact_card[id]
    assert item.user_email == get_user_email()
    db(db.contact_card.id == id).delete()
    return dict(status=200)