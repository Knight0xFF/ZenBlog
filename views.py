__author__ = 'zend'

from flask import Flask, render_template, request, Response, session,  redirect, flash, url_for
from flask.ext.login import login_user, logout_user, login_required, LoginManager
from models import Category, Post, Tag, User, db
from functools import wraps
from run import app
from random import shuffle
import time

app.config.from_object('config')
page_title = "Zend's Blog"
POSTS_PER_PAGE = 3

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.route('/')
@app.route('/index')
@app.route("/page/<int:pageid>")
def index(pageid=1):
    categorys = Category.query.all()
    tags = Tag.query.group_by(Tag.tag_name).all()
    shuffle(tags)
    tags = tags[:10]
    posts = Post.query.order_by(Post.post_date.desc()).paginate(pageid, POSTS_PER_PAGE)
    hot_posts = Post.query.order_by(Post.post_view_count.desc()).all()[0:5]
    return render_template("index.html",
                           page_title=page_title,
                           posts=posts,
                           categorys=categorys,
                           hot_posts=hot_posts,
                           tags=tags)


@app.route('/archives')
def archives():
    categorys = Category.query.all()
    posts = Post.query.all()
    tags = Tag.query.group_by(Tag.tag_name).all()
    shuffle(tags)
    tags = tags[:10]
    hot_posts = Post.query.order_by(Post.post_view_count.desc()).all()[0:5]
    return render_template("archives.html",
                           page_title=page_title,
                           posts=posts,
                           categorys=categorys,
                           hot_posts=hot_posts,
                           tags=tags)


@app.route('/about')
def about():
    categorys = Category.query.all()
    tags = Tag.query.group_by(Tag.tag_name).all()
    shuffle(tags)
    tags = tags[:10]
    hot_posts = Post.query.order_by(Post.post_view_count.desc()).all()[0:5]
    return render_template("about.html",
                           page_title=page_title,
                           categorys=categorys,
                           hot_posts=hot_posts,
                           tags=tags)


@app.route('/search')
@app.route('/search/page/<int:pageid>')
def search(pageid=1):
    categorys = Category.query.all()
    tags = Tag.query.group_by(Tag.tag_name).all()
    shuffle(tags)
    tags = tags[:10]
    hot_posts = Post.query.order_by(Post.post_view_count.desc()).all()[0:5]
    keywords = request.args.get('keywords', '')
    searchresult = Post.query.search(keywords)

    posts = searchresult.order_by(Post.post_date.desc()).paginate(pageid, 3)

    return render_template("search.html",
                           page_title=page_title,
                           posts=posts,
                           categorys=categorys,
                           hot_posts=hot_posts,
                           tags=tags)


@app.route('/category/<category_name>')
@app.route('/category/<category_name>/page/<int:pageid>')
def category(category_name, pageid=1):
    hot_posts = Post.query.order_by(Post.post_view_count.desc()).all()[0:5]
    categorys = Category.query.all()
    tags = Tag.query.group_by(Tag.tag_name).all()
    shuffle(tags)
    tags = tags[:10]
    posts = Post.query.filter_by(category_name=category_name).\
        order_by(Post.post_date.desc()).paginate(pageid, POSTS_PER_PAGE)
    return render_template("category.html",
                           page_title=page_title,
                           posts=posts,
                           categorys=categorys,
                           category_name=category_name,
                           hot_posts=hot_posts,
                           tags=tags)


@app.route('/tag/<tag_name>')
def tag(tag_name):
    hot_posts = Post.query.order_by(Post.post_view_count.desc()).all()[0:5]
    tags = Tag.query.filter_by(tag_name=tag_name).all()
    tagss = Tag.query.group_by(Tag.tag_name).all()
    shuffle(tags)
    tagss = tagss[:10]
    categorys = Category.query.all()
    posts = []
    for i in tags:
        posts.append(Post.query.filter_by(id=i.post_id).first())
    return render_template("tag.html",
                           page_title=page_title,
                           posts=posts,
                           categorys=categorys,
                           hot_posts=hot_posts,
                           tags=tagss)


@app.route('/article/<int:postid>')
def article(postid):
    hot_posts = Post.query.order_by(Post.post_view_count.desc()).all()[0:5]
    categorys = Category.query.all()
    tags = Tag.query.group_by(Tag.tag_name).all()
    shuffle(tags)
    tags = tags[:10]
    post = Post.query.filter_by(id=postid).first()
    post.post_view_count += 1
    db.session.add(post)
    db.session.commit()
    return render_template("post.html",
                           page_title=post.post_title,
                           post=post,
                           categorys=categorys,
                           hot_posts=hot_posts,
                           tags=tags)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if not User.query.filter_by(username=username, password=password):
            flash('emh, A wrong was happened~~~')
        else:
            user = User.query.filter_by(username=username).first()
            login_user(user)
            flash('loggin success~~~~')
            return redirect('/admin')
    return render_template('login.html')


@app.route('/admin')
@login_required
def admin():
    return render_template("admin.html")


@app.route('/newpost', methods=['GET', 'POST'])
@login_required
def new_post():
    categorys = Category.query.all()
    if request.method == 'POST':
        post_title = request.form.get('post_title').strip()
        post_excerpt = request.form.get('post_excerpt')
        post_content = request.form.get('post_content')
        post_category_name = request.form.get('post_category_name')
        post_tag = request.form.get('post_tags').split(",")

        category = Category.query.filter_by(category_name=post_category_name).first()
        newpost = Post(post_title=post_title, post_content=post_content, post_excerpt=post_excerpt,
                       category_id=category.id, category_name=post_category_name)

        category.category_post_count += 1

        if request.form.get('post-preview') == '1':
            post_data = {"title": post_title, "content": post_content}
            session['post-preview'] = post_data
            return redirect('/preview')
        else:
            session.pop('post-preview', None)
        db.session.add(newpost)
        db.session.add(category)
        db.session.commit()

        for i in post_tag:
            tags = Tag(post_id=newpost.id, tag_name=i)
            db.session.add(tags)
            db.session.commit()

    return render_template("admin-new-posts.html", categorys=categorys)


@app.route('/preview')
@login_required
def preview():
    post = session.get('post-preview')
    return render_template('admin-posts-preview.html', post=post)


@app.route('/posts_list')
@app.route('/posts_list/page/<int:pageid>')
@login_required
def posts_list(pageid=1):
    posts = Post.query.order_by(Post.post_date.desc()).paginate(pageid, POSTS_PER_PAGE)
    if not posts.total:
        pagination = [0]
    elif posts.total % POSTS_PER_PAGE:
        pagination = range(1, posts.total / POSTS_PER_PAGE + 2)
    else:
        pagination = range(1, posts.total / POSTS_PER_PAGE + 1)
    return render_template("admin-posts-list.html",
                           posts=posts,
                           pageid=pageid,
                           pagination=pagination)


@app.route('/post_edit/<int:post_id>', methods=["GET", "POST"])
@login_required
def post_edit(post_id):
    categorys = Category.query.all()
    posts = Post.query.filter_by(id=post_id).first()
    if request.method == "POST":
        post_title = request.form.get('post_title').strip()
        post_excerpt = request.form.get('post_excerpt')
        post_content = request.form.get('post_content')
        #post_category_name = request.form.get('post_category_name')
        #category = Category.query.filter_by(category_name=post_category_name).first()
        posts = Post.query.filter_by(id=post_id).first()
        posts.post_title = post_title
        posts.post_excerpt = post_excerpt
        posts.post_content = post_content

        db.session.add(posts)
        db.session.commit()

    return render_template("admin-posts-edit.html",
                           posts=posts,
                           categorys=categorys)


@app.route('/admin_search')
@login_required
def admin_search():
    keywords = request.args.get('keywords', '')
    searchresult = Post.query.search(keywords)
    posts = searchresult.order_by(Post.post_date.desc())
    return render_template("admin-search.html",
                           posts=posts)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You were logged out')
    return redirect('/index')