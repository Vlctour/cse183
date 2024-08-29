"""
This file defines the database models
"""

import datetime
from .common import db, Field, auth
from pydal.validators import *


def get_user_email():
    return auth.current_user.get('email') if auth.current_user else None

def get_time():
    return datetime.datetime.utcnow()

db.define_table(
    'contact_request',
    Field('name', requires=IS_NOT_EMPTY(error_message='cannot be empty')),
    Field('email', requires = IS_EMAIL(error_message='invalid email!')), # maybe add default params
    Field('phone', requires=IS_NOT_EMPTY(error_message='cannot be empty')), #validate phone number format?
    Field('message', 'text')
) # default=get_user_email, default=get_time

db.commit()
