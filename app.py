from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import json

names = [{'ID':1, 'fName':'John', 'lName':'Smith'},{'ID':2,'fName':'Mary', 'lName':'Jones'},{'ID':3,'fName':'Laura', 'lName':'Jukez'}]
j_names = json.dumps(names)
class DB:
    def __init__(self, fName, lName):
        self.name = fName
        self.lastname = lName

x = DB(names[0]['fName'],names[0]['lName'])
print(x)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username




@app.route('/')
def index():
    return render_template("index.html", names = names)

@app.route('/background_process', methods = ['POST'])
def background_process():
    return('', 204)


if __name__ == '__main__':
    app.run(debug=True)
