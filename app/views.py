import os
from flask import Flask, render_template, redirect, request
# from flask.ext.sqlalchemy import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy
import re

# Flask app
app = Flask(__name__)
app.debug = True

if(app.debug):
    from werkzeug.debug import DebuggedApplication
    app.swgi_app = DebuggedApplication(app.wsgi_app, True)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///%s/cms.db' % os.getcwd()
db = SQLAlchemy(app)


class Pages(db.Model):
    __tablename__ = 'pages'

    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(1000))
    title = db.Column(db.String(1000))
    content = db.Column(db.BLOB)

    def __init__(self, title, content):
        self.title = title
        self.slug = re.sub(r'[^\w]+', '-', title.lower())
        self.content = content

    def __repr__(self):
        return '<Pages : id=%r, title=%s, slug=%s>' \
              % (self.id, self.title, self.slug)


# Views that without login
@app.route('/')
def index():
    pages = db.session.query(Pages).all()
    return render_template('index.html', pages=pages, title="home")


@app.route('/test-db/')
def test_db():
    pages = db.session.query(Pages)
    print("\n".join(repr(x) for x in pages))
    return "success"


@app.route('/post/<int:page_id>')
def view_page(page_id):
    page = db.session.query(Pages).filter_by(id=page_id).first()
    return render_template('page.html',
                           id=page.id, title=page.title, content=page.content)


"""
# Views that require login
@app.route('/edit-page/<int:page_id>')
def edit_page(page_id):
    page = db.session.query(Pages).filter_by(id=page_id).first()
    return render_template('edit-page.html',
                           id=page.id, title=page.title, content=page.content)


@app.route('/update-page/', methods=['POST'])
def update_page():
    page_id = request.form['id']
    title = request.form['title']
    content = request.form['content']
    db.session.query(Pages).filter_by(id=page_id).update({'title': title,
                                                          'content': content})
    db.session.commit()
    return redirect('/page/'+page_id)


@app.route('/new-page/')
def new_page():
    return render_template('new-page.html')


@app.route('/save-page/', methods=['POST'])
def save_page():
    page = Pages(title=request.form['title'],
                 content=request.form['content'])
    db.session.add(page)
    db.session.commit()
    return redirect('/page/%d' % page.id)


@app.route('/delete-page/<int:page_id>')
def delete_page(page_id):
    db.session.query(Pages).filter_by(id=page_id).delete()
    db.session.commit()
    return redirect('/news')

"""
