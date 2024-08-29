from py4web import action, request, URL
from .common import auth, session
from .models import db, get_user_email, get_time, get_regex_tags

# Complete. 
@action('index')
@action.uses('index.html', db, session, auth.user)
def index():
    return dict(
        get_posts_url = URL('get_posts'),
        get_tags_url = URL('get_tags'),
        add_post_url = URL('add_post'),
        delete_post_url = URL('delete_post'),
    )

@action('get_posts', method="GET")
@action.uses(db, session, auth.user)
def get_posts():
    q = None
    tag_name_len = request.params.get('len')
    if tag_name_len != None:
        for i in range(int(tag_name_len)):
            tag_name = request.params.get(f'tags[{i}][tag]')
            if q is None:
                q = (db.posts.post.contains(tag_name))
            else:
                q |= (db.posts.post.contains(tag_name))

    posts = db(q).select(orderby=~db.posts.date_time).as_list()
    email = get_user_email()
    return dict(curr_user=email, posts=posts)

@action('get_tags', method="GET")
@action.uses(db, session, auth.user)
def get_tags():
    tags = db(db.post_tags).select(db.post_tags.tag, distinct=True).as_list()
    return dict(tags=tags)

@action('add_post', method="POST")
@action.uses(db, session, auth.user)
def add_post():
    post = request.json.get('post')
    email = get_user_email()
    time = get_time()
    tags = get_regex_tags(post)
    # should duplicate posts be duplicated? im going to guess no
    # so we leave this as insert instead of update_or_insert
    id = db.posts.insert(
        user_email=email,
        post=post,
        date_time=time
    )
    for tag in tags:
        db.post_tags.update_or_insert(
            (db.post_tags.tag == tag) & (db.post_tags.posts_id == id),
            posts_id=id,
            user_email=email,
            tag=tag
        )
    
    return dict(
        id=id,
        user_email=email,
        post=post,
        date_time=time,
        tags=tags
    )

@action('delete_post', method="POST")
@action.uses(db, session, auth.user)
def delete_post():
    id = request.json.get('id')
    post = db.posts[id]
    assert post.user_email == get_user_email()
    db(db.posts.id == id).delete()
    return dict(status=200)