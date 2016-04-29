#!/usr/bin/env python # coding: utf-8
import sys
from sqlalchemy import create_engine
from flask import Flask, render_template, request, flash, url_for, redirect
from models import db, Book
from flask.ext.script import Manager, Server
from flask.ext.migrate import Migrate, MigrateCommand

reload(sys)
sys.setdefaultencoding('utf-8')

app = Flask(__name__)
#デバッグ
app.config['DEBUG'] = True
#秘密キー
app.secret_key = 'development key'
#データベースを指定
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///diary.db'
app.config['SQLALCHEMY_NATIVE_UNICODE'] = 'utf-8'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db.init_app(app)
db.app = app

@app.route('/')
def index():
    return render_template('index.html',books = Book.query.all())


@app.route('/new', methods=['GET', 'POST'])
def new():
    if request.method == 'POST':
        if not request.form['title'] or not request.form['author'] or not request.form['publisher']:
            flash('Please enter all the fields', 'error')
        else:
            book_ps = Book(request.form['title'],request.form['author'],request.form['publisher'])

            db.session.add(book_ps)
            db.session.commit()
            flash('Success')
            return redirect(url_for('index'))
    return render_template('new.html')



migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)
manager.add_command('runserver', Server(host='localhost', port='8080'))

if __name__ == "__main__":
    manager.run()