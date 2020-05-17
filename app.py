from project import app
from flask_login import login_user
from project.users.forms import LoginForm
from project.models import Users, Stylists, Services, Texts
from flask import render_template, flash, request, url_for, redirect

@app.route('/')
def home():
    return 'changed it in github'




if __name__ == '__main__':
    app.run(debug=True)
