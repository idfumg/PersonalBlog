from flask import (
    render_template,
    redirect,
    url_for,
    g,
    request,
    session,
    abort,
    jsonify
)
from app import app, oidc, db
from .models import Post

from functools import wraps


def login_required(func):
    @wraps(func)
    def wrap(*args, **kwargs):
        if not 'email' in session:
            return abort(404)
        return func(*args, **kwargs)
    return wrap

@app.route('/login/')
@oidc.check
def login():
    email = g.oidc_id_token['email']

    if not email or email != app.config['ADMIN_EMAIL']:
        return abort(404)

    session['email'] = email
    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.pop('email', None)
    return redirect(url_for('index'))

@app.route('/')
@app.route('/index')
@app.route('/index/<path:domain>')
def index(domain=None):
    if domain:
        posts = Post.query.filter(Post.domain == domain)
    else:
        posts = Post.query

    logged = session.get('email', None)
    if not logged:
        posts = posts.filter(Post.deleted == False)
    posts = posts.order_by(Post.time.desc()).all()

    return render_template('index.html',
                           posts=posts,
                           logged=logged)

@app.route('/post/show/<int:id>')
def post_show(id):
    post = Post.query.filter(Post.id == id).first()
    if not post:
        return abort(404)

    return render_template('post.html',
                           post=post,
                           logged=session.get('email', None))

@app.route('/post/edit')
@app.route('/post/edit/<int:id>')
@login_required
def post_edit(id=None):
    edit_post = None

    if id:
        edit_post = Post.query.filter(Post.id == id).first()

        if not edit_post:
            abort(404)

    return render_template('edit.html',
                           post=edit_post,
                           logged=session.get('email', None))

@app.route('/post/save', methods=['POST'])
@app.route('/post/save/<int:id>', methods=['POST'])
@login_required
def post_save(id=None):
    def post_from_data(id, domain, header, intro, text):
        if id:
            post = Post.query.get(id)
        else:
            post = Post()

        post.header = header
        post.intro = intro
        post.text = text
        post.domain = domain

        import datetime
        if not post.time:
            post.time = datetime.datetime.now()

        return post

    post = post_from_data(id,
                          request.form['domain'].lower() or 'other',
                          request.form['header'],
                          request.form['intro'],
                          request.form['text'])

    db.session.add(post)
    db.session.commit()

    return jsonify({'result': 'post_saved'})

@app.route('/post/del/<int:id>', methods=['POST'])
@login_required
def post_del(id):
    post = Post.query.filter(Post.id == id).first()
    if not post:
        abort(404)

    post.deleted = True
    db.session.add(post)
    db.session.commit()

    return jsonify({'result': 'post_deleted'})

@app.route('/post/erase/<int:id>', methods=['POST'])
@login_required
def post_erase(id):
    post = Post.query.filter(Post.id == id).first()
    if not post:
        return abort(404)

    db.session.delete(post)
    db.session.commit()

    return jsonify({'result': 'post_erased'})

@app.route('/post/restore/<int:id>', methods=['POST'])
@login_required
def post_restore(id):
    post = Post.query.filter(Post.id == id).first()
    if not post:
        return abort(404)

    post.deleted = False
    db.session.add(post)
    db.session.commit()

    return jsonify({'result': 'post_restored'})

@app.route('/about')
def about():
    return render_template('about.html')
