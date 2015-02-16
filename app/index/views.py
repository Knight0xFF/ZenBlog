# -*- coding: utf-8 -*-
__author__ = 'Zend'


from flask import Blueprint, render_template, session,  request, redirect, flash, url_for
from models import Category, Post, Tag, User, db
from random import shuffle
from app import app
import time


index = Blueprint("index", __name__, template_folder='templates', static_folder='static',
                  static_url_path='index/static',)  # 蓝图url+static_url_path, 以app创建的目录为根目录

page_info = dict()
POSTS_PER_PAGE = app.config["PER_PAGE"]


@index.route('/')
@index.route('index')
@index.route("page/<int:pageid>")
def indexs(pageid=1):
    page_info = default_info()
    page_info["title"] = u"首页" + app.config["NAME"]
    categorys = Category.query.all()
    posts = Post.query.order_by(Post.post_date.desc()).paginate(pageid, POSTS_PER_PAGE)
    return render_template("index/index.html",
                           page_info=page_info,
                           posts=posts,
                           categorys=categorys,)


@index.route('archives')
def archives():
    page_info = default_info()
    page_info["title"] = u"文章归档" + app.config["NAME"]
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
    return render_template("index/archives.html",
                           page_info=page_info,
                           archives=archives,
                           posts=posts,
                           categorys=categorys,)


@index.route('about')
def about():
    page_info = default_info()
    page_info["title"] = u"关于" + app.config["NAME"]
    categorys = Category.query.all()
    return render_template("index/about.html",
                           page_info=page_info,
                           categorys=categorys)


@index.route('search')
@index.route('search/page/<int:pageid>')
def search(pageid=1):
    page_info = default_info()
    categorys = Category.query.all()
    keywords = request.args.get('keywords', '')
    searchresult = Post.query.search(keywords)

    posts = searchresult.order_by(Post.post_date.desc()).paginate(pageid, 3)

    return render_template("index/search.html",
                           page_info=page_info,
                           posts=posts,
                           categorys=categorys,
                           )


@index.route('category/')
def category():
    page_info = default_info()
    page_info["title"] = u"文章分类" + app.config["NAME"]
    category_has_posts = []
    categorys = Category.query.all()
    for c in categorys:
        posts = Post.query.filter_by(category_name=c.category_name).all()
        category_has_posts.append(posts)
    return render_template("index/category.html",
                           page_info=page_info,
                           categorys=categorys,
                           category_has_posts=category_has_posts)



@index.route('tag')
def tag():
    page_info = default_info()
    page_info["title"] = u"标签" + app.config["NAME"]
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
    return render_template("index/tag.html",
                           page_info=page_info,
                           tags=tags,
                           categorys=categorys,
                           tag_has_posts=tag_has_posts)


@index.route('article/<int:postid>')
def article(postid):
    categorys = Category.query.all()
    post = Post.query.filter_by(id=postid).first()
    post_tags = Tag.query.filter_by(post_id=postid).all()
    tag = ""
    for i in post_tags:
        tag += i.tag_name
    print tag
    page_info["title"] = post.post_title + app.config["NAME"]
    page_info["description"] = post.post_excerpt[3:-3]
    page_info["keywords"] = tag
    post.post_view_count += 1
    db.session.add(post)
    db.session.commit()
    return render_template("index/post.html",
                           page_info=page_info,
                           post=post,
                           categorys=categorys,
                           post_tags=post_tags)


def default_info():
    page_info["title"] = "Zend's Blog"
    page_info["keywords"] = "Linux Pentest Python Golang Web"
    page_info["description"] = ""
    return page_info
