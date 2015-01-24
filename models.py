__author__ = 'zend'

from flask.ext.sqlalchemy import SQLAlchemy, BaseQuery
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand
from datetime import datetime
from run import app

db = SQLAlchemy(app)
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)


class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    password = db.Column(db.String(120))
    role = db.Column(db.SmallInteger)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    def __repr__(self):
        return '<User %r>' % (self.nickname)


class PostQuery(BaseQuery):
    def get_category_name(self):
        return Category.query.filter_by(id=self.category_id).first()

    def search(self, keywords):
        criteria = []
        keyword = '%' + keywords + '%'
        criteria.append(db.or_(Post.post_title.ilike(keyword), Post.post_content.ilike(keyword)))

        res = reduce(db.and_, criteria)

        return self.filter(res).distinct()


class Post(db.Model):
    __tablename__ = "post"
    query_class = PostQuery
    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    category_name = db.Column(db.String(120), nullable=False)
    post_title = db.Column(db.String(120), unique=True)
    post_date = db.Column(db.DateTime, default=datetime.utcnow)
    post_excerpt = db.Column(db.Text)
    post_content = db.Column(db.Text)
    post_view_count = db.Column(db.Integer, default=0)
    post_comment_count = db.Column(db.Integer, default=0)
    post_love_count = db.Column(db.Integer, default=0)

    def __init__(self, *args, **kwargs):
        super(Post, self).__init__(*args, **kwargs)

    def __repr__(self):
        return '<Post title %r>' % self.post_title


class Category(db.Model):
    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(100), unique=True)
    category_post_count = db.Column(db.Integer, default=0)

    def __init__(self, *args, **kwargs):
        super(Category, self).__init__(*args, **kwargs)

    def __repr__(self):
        return '<category name %r>' % self.category_name


class Link(db.Model):
    __tablename__ = "link"
    id = db.Column(db.Integer, primary_key=True)
    link_url = db.Column(db.String(100), unique=True)
    link_name = db.Column(db.String(100))
    link_updated = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, *args, **kwargs):
        super(Link, self).__init__(*args, **kwargs)

    def __repr__(self):
        return '<link name %r>' % self.link_name


class Tag(db.Model):
    __tablename__ = "tag"
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer)
    tag_name = db.Column(db.String(100))

    def __init__(self, *args, **kwargs):
        super(Tag, self).__init__(*args, **kwargs)

    def __repr__(self):
        return '<Tag name %r>' % self.tag_name


if __name__ == '__main__':
    manager.run()