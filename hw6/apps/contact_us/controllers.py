from py4web import action, request, abort, redirect, URL
from yatl.helpers import A
from .common import db, session, T, cache, auth, logger, authenticated, unauthenticated, flash
from py4web.utils.url_signer import URLSigner
from .models import get_user_email
from py4web.utils.form import Form, FormStyleBulma
from py4web.utils.grid import Grid, GridClassStyleBulma

# Complete. 
@action('index', method=['GET', 'POST'])
@action.uses('index.html', db, auth)
def index():
    form = Form(db.contact_request, formstyle=FormStyleBulma)
    if form.accepted:
        redirect(URL('index'))
    return dict(form=form)

@action('contact_requests/<path:path>', method=['GET', 'POST'])
@action('contact_requests', method=['GET', 'POST'])
@action.uses('contact_requests.html', db, session, auth)
def contact_requests(path=None):
    curr_user = get_user_email()
    if curr_user != "admin@example.com":
        redirect(URL('index'))

    grid = Grid(
        path,
        # formstyle=FormStyleBulma,
        grid_class_style=GridClassStyleBulma,
        query=(db.contact_request.id > 0),
        orderby=[~db.contact_request.id],
        search_queries=[
            ['Search by Name', lambda val: db.contact_request.name.contains(val)],
            ['Search by Message', lambda val: db.contact_request.message.contains(val)],
        ],
    )
    return dict(grid=grid)