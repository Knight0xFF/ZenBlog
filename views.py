__author__ = 'zend'

from flask import Flask, render_template, request
from models import Category, Post, Tag, db
from run import app
from random import shuffle
import time

app.config.from_object('config')
page_title = "Zend's Blog"
POSTS_PER_PAGE = 10


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


@app.route('/newpost', methods=['GET', 'POST'])
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
        db.session.add(newpost)
        db.session.add(category)
        db.session.commit()

        for i in post_tag:
            tags = Tag(post_id=newpost.id, tag_name=i)
            db.session.add(tags)
            db.session.commit()

    return render_template("admin-new-posts.html", categorys=categorys)