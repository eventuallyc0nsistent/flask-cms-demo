import os
from flask import Flask, render_template, redirect, request
from flask.ext.sqlalchemy import SQLAlchemy

# Flask app
app = Flask(__name__)
app.debug = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///%s/cms.db' % os.getcwd()
db = SQLAlchemy(app)

# SQLAlchemy models
class Pages(db.Model):
    __tablename__ = 'pages'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(1000))
    content = db.Column(db.BLOB)

    def __init__(self, title, content):
        self.title = title
        self.content = content

    def __repr__(self):
        return '<Pages : id=%r, title=%s, content=%s>' \
              % (self.id, self.title, self.content)

# app views
@app.route('/')
def index():
    pages = db.session.query(Pages).all()
    return render_template('index.html', pages=pages)

@app.route('/page/<int:page_id>')
def view_page(page_id):
    page = db.session.query(Pages).filter_by(id=page_id).first()
    return render_template('page.html', 
                            id=page.id, title=page.title, content=page.content)

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
    return redirect('/')

