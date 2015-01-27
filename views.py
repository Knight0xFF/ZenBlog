__author__ = 'zend'

from flask import Flask, render_template, request, Response, session,  redirect, flash, url_for
from flask.ext.login import login_user, logout_user, login_required, LoginManager
from models import Category, Post, Tag, User, db
from run import app
from random import shuffle
import time


app.config.from_object('config')
page_title = "Zend's Blog"
POSTS_PER_PAGE = 5

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
    posts = Post.query.order_by(Post.post_date.desc()).paginate(pageid, POSTS_PER_PAGE)
    return render_template("index.html",
                           page_title=page_title,
                           posts=posts,
                           categorys=categorys,)


@app.route('/archives')
def archives():
    categorys = Category.query.all()
    posts = Post.query.order_by(Post.post_date.desc())
    mon = []
    for p in posts:
        mon.append(p.post_date.strftime('%B'))
    mon = list(set(mon))
    archives = {}
    for y in xrange(2014, 2016):
        mon_has_post = {}
        for m in mon:
            temp = []
            for p in posts:
                if p.post_date.strftime('%B') == m and p.post_date.strftime('%Y') == str(y):
                    temp.append(p)
            mon_has_post[m] = temp
        archives[str(y)] = mon_has_post
    return render_template("archives.html",
                           archives=archives,
                           posts=posts,
                           categorys=categorys,)


@app.route('/about')
def about():
    categorys = Category.query.all()
    return render_template("about.html",
                           categorys=categorys)


@app.route('/search')
@app.route('/search/page/<int:pageid>')
def search(pageid=1):
    categorys = Category.query.all()
    keywords = request.args.get('keywords', '')
    searchresult = Post.query.search(keywords)

    posts = searchresult.order_by(Post.post_date.desc()).paginate(pageid, 3)

    return render_template("search.html",
                           posts=posts,
                           categorys=categorys,
                           )


@app.route('/category/')
def category():
    category_has_posts = []
    categorys = Category.query.all()
    for c in categorys:
        posts = Post.query.filter_by(category_name=c.category_name).all()
        category_has_posts.append(posts)
    return render_template("category.html",
                           categorys=categorys,
                           category_has_posts=category_has_posts)



@app.route('/tag')
def tag():
    categorys = Category.query.all()
    tags = Tag.query.group_by(Tag.tag_name).all()
    tag_has_posts = {}
    for t in tags:
        posts = []
        tagss = Tag.query.filter_by(tag_name=t.tag_name).all()
        for i in tagss:
            post = Post.query.filter_by(id=i.post_id).all()
            posts.append(post)
        tag_has_posts[t.tag_name] = posts
    return render_template("tag.html",
                           tags=tags,
                           categorys=categorys,
                           tag_has_posts=tag_has_posts)


@app.route('/article/<int:postid>')
def article(postid):
    categorys = Category.query.all()
    post = Post.query.filter_by(id=postid).first()
    post_tags = Tag.query.filter_by(post_id=postid).all()
    post.post_view_count += 1
    db.session.add(post)
    db.session.commit()
    return render_template("post.html",
                           post=post,
                           categorys=categorys,
                           post_tags=post_tags)
