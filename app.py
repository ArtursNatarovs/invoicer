from project import app
from flask_login import login_user
from project.users.forms import LoginForm
from project.models import Users, Stylists, Services, Texts
from flask import render_template, flash, request, url_for, redirect

@app.route('/')
def home():
    return render_template('hat.html',Stylists=Stylists, Texts=Texts, Services=Services, font_url='http://fonts.googleapis.com/css?family=Yanone+Kaffeesatz:400,200,300')

##########################################################################

@app.route('/login',methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()

        if user is not None:
            if user.check_password(form.password.data) and user is not None:

                login_user(user)
                flash('you now logged in')

                next = request.args.get('next')
                if next == None or not next[0]=='/':
                    next = url_for('users.welcome_user')
                return redirect(next)
            else:
                flash("Something din't match!")
                return redirect(url_for('login'))
        else:
            flash('We could not find your account.')
            return redirect(url_for('users.register'))
    return render_template('login.html',form=form)

#############################################################################

@app.route('/t&c')
def t_and_C():
    return render_template('t_and_c.html')


if __name__ == '__main__':
    app.run(debug=True)
