__author__ = 'Zend'

from flask import Blueprint, Flask, render_template, request, Response, url_for, redirect
from flask.ext.login import login_user, logout_user, login_required, LoginManager
from models import Category, Post, Tag, User, db
from app import app

admin = Blueprint("admin", __name__, template_folder='templates', static_folder='static',
                  static_url_path='/static')

POSTS_PER_PAGE = app.config["PER_PAGE"]

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


@admin.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if not User.query.filter_by(username=username, password=password):
            flash("login success!")
        else:
            user = User.query.filter_by(username=username).first()
            login_user(user)
            return redirect(url_for('admin.admins'))
    return render_template('admin/login.html')


@admin.route('/admin')
@login_required
def admins():
    return render_template("admin/admin.html")



@admin.route('/newpost', methods=['GET', 'POST'])
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

        db.session.add(newpost)
        db.session.add(category)
        db.session.commit()

        for i in post_tag:
            tags = Tag(post_id=newpost.id, tag_name=i)
            db.session.add(tags)
            db.session.commit()

    return render_template("admin/admin-new-posts.html", categorys=categorys)


@admin.route('/posts_list')
@admin.route('/posts_list/<int:pageid>')
@login_required
def posts_list(pageid=1):
    posts = Post.query.order_by(Post.post_date.desc()).paginate(pageid, POSTS_PER_PAGE)
    if not posts.total:
        pagination = [0]
    elif posts.total % POSTS_PER_PAGE:
        pagination = range(1, posts.total / POSTS_PER_PAGE + 2)
    else:
        pagination = range(1, posts.total / POSTS_PER_PAGE + 1)
    return render_template("admin/admin-posts-list.html",
                           posts=posts,
                           pageid=pageid,
                           pagination=pagination)


@admin.route('/post_edit/<int:post_id>', methods=["GET", "POST"])
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

    return render_template("admin/admin-posts-edit.html",
                           posts=posts,
                           categorys=categorys)


@admin.route("/post_delete/<int:post_id>")
@login_required
def post_delete(post_id):
    post = Post.query.filter_by(id=post_id).first()
    category = Category.query.filter_by(category_name=post.category_name).first()
    category.category_post_count -= 1
    tag = Tag.query.filter_by(post_id=post_id).all()
    for t in tag:
        db.session.delete(t)
    db.session.delete(post)
    db.session.add(category)
    db.session.commit()

    return Response("OK")


@admin.route('/admin_search')
@login_required
def admin_search():
    keywords = request.args.get('keywords', '')
    searchresult = Post.query.search(keywords)
    posts = searchresult.order_by(Post.post_date.desc())
    return render_template("admin/admin-search.html",
                           posts=posts)


@admin.route('/logout')
@login_required
def logout():
    logout_user()
    #flash('You were logged out')
    return redirect(url_for('admin.login'))