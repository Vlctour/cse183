"""
This file defines the database models
"""
import datetime
import re

from .common import db, Field, auth
from pydal.validators import *

def get_user_email():
    return auth.current_user.get('email') if auth.current_user else None

def get_user():
    return auth.current_user.get('id') if auth.current_user else None

def get_time():
    time = datetime.datetime.utcnow()
    new_time = time.replace(microsecond=0)
    return new_time

def get_regex_tags(post):
    regex = r'\#[a-zA-Z0-9_]+'
    tags = re.findall(regex, post)
    stripped_tags = [tag[1:] for tag in tags]
    return stripped_tags

# Complete.
db.define_table(
    'posts',
    Field('user_email', 'string', default=get_user_email),
    Field('post', 'string'),
    Field('date_time', 'datetime', default=get_time),
)

db.define_table(
    'post_tags',
    Field('posts_id', 'reference posts', ondelete='CASCADE'),
    Field('user_email', 'string'),
    Field('tag', 'string'),
)

db.commit()