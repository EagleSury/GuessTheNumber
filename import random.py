from sqlalchemy.sql import func
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request, redirect, url_for
import random
import os
# num = random #
turn = 0
message = ""
Gif = ""
app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] =\
    'sqlite:///' + os.path.join(basedir, 'db.sqlite')

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


@app.get("/")
def home():
    Gif = db.session.query(Gif).all()
    return render_template("base.html", message = message, Gif = Gif, color = "red")


@app.get("/1")
def bye():
    return "Bye!"


class Gif(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    complete = db.Column(db.Boolean)

    def __repr__(self):
        return f'<Todo {self.id}-{self.title}-{self.complete} >'

'''
class go(guess):

    turn += 1
    if guess < num:
        print("Oops, Too low!")
    elif guess > num:
        print('Oops. Too high!')
    else:
        print("Wow! you found the number I guessed!\nGood job!")
        exit()
'''
