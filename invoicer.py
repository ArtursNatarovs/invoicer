from flask import Flask, render_template, request, session, redirect, url_for
from flask_mail import Mail, Message
import os
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail
from datetime import datetime
import json
from flask_wtf import FlaskForm
from wtforms import (StringField, BooleanField, DateTimeField,
                     RadioField,SelectField,TextField,
                     TextAreaField,SubmitField)
from wtforms.validators import DataRequired

app = Flask(__name__)


app.config['SECRET_KEY'] = 'mysecretkey'
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir,'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config.update(DEBUG=True,
                    MAIL_SERVER='smtp.123-reg.co.uk',
                    MAIL_PORT=465,
                    MAIL_USE_SSL=True,
                    MAIL_USE_TLS = False,
                    MAIL_SUPPRESS_SEND = False,
                    MAIL_DEBUG = True,
                    TESTING = False,
                    MAIL_USERNAME='info@hofhsalon.co.uk',
                    MAIL_PASSWORD='Qw!2er34')

db = SQLAlchemy(app)

mail = Mail(app)
Migrate(app,db)

def initial_invoice():
    if Invoices.query.all() == []:
        first_invoice = Invoices()
        db.session.add(first_invoice)
        db.session.commit()
    else:
        pass

class DataForm(FlaskForm):
    name = StringField('First Name',validators=[DataRequired()])
    last_name = StringField('Last Name',validators=[DataRequired()])
    email = StringField('Email',validators=[DataRequired()])
    p_number = StringField('Phone Number',validators=[DataRequired()])
    line1 = StringField('Address line1',validators=[DataRequired()])
    line2 = StringField('Address line2',validators=[DataRequired()])
    postCode = StringField('Post Code',validators=[DataRequired()])
    city = StringField('City',validators=[DataRequired()])
    submit = SubmitField('Submit')


class User(db.Model):

    __tablename__ = 'users'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.Text)
    last_name = db.Column(db.String)
    email = db.Column(db.Text, unique=True)
    received_invoices = db.relationship('Invoices',backref='user',lazy='dynamic')
    p_number = db.Column(db.String)
    line1 = db.Column(db.String)
    line2 = db.Column(db.String)
    postCode = db.Column(db.String)
    city = db.Column(db.String)

    #def __init__(self,name, last_name, email):
        #self.name = name
        #self.email = email
        #self.last_name = last_name



class Invoices(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    date = db.Column(db.String)
    salon_user_id = db.Column(db.Integer,db.ForeignKey('salon.id'))
    receiver_user_id = db.Column(db.Integer,db.ForeignKey('users.id'))
    text = db.Column(db.Text)

    def from_to(self):
        return [Salon.query.filter_by(id=self.salon_user_id).first().name, User.query.filter_by(id=self.receiver_user_id).first().name]


class Salon(db.Model):

    __tablename__ = 'salon'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.Text)
    addresse = db.Column(db.String)
    email = db.Column(db.Text, unique=True)
    p_number = db.Column(db.Text)
    sent_invoices = db.relationship('Invoices',backref='salon',lazy='dynamic')
    line1 = db.Column(db.String)
    line2 = db.Column(db.String)
    postCode = db.Column(db.String)
    city = db.Column(db.String)


def salon_query():
    if Salon.query.all():
        return Salon.query.all()
    else:
        return 'No salon found'

def salon_query():
    if User.query.all():
        return User.query.all()
    else:
        return 'No users found'

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/send_invoice')
def send_invoice():
    return render_template('send_invoice.html', users=salon_query(), salons=salon_query())

@app.route('/tenats')
def tenants():
    return render_template('tenants.html', users=salon_query())


@app.route('/add_new_tenant', methods=['GET','POST'])
def add_new_tenant():
    form = DataForm()
    if form.validate_on_submit():
        user = User(name=form.name.data,
                    last_name=form.last_name.data,
                    email=form.email.data,
                    p_number=form.p_number.data,
                    line1=form.line1.data,
                    line2=form.line2.data,
                    postCode=form.postCode.data,
                    city=form.city.data)
        db.session.add(user)
        db.session.commit()
        return redirect((url_for('tenants')))

    return render_template('add_new_tenant.html', form=form)


@app.route('/update_tenant', methods=['GET','POST'])
def update_tenant():
    form=DataForm()
    userId = int(request.form['userId'])
    user=User.query.filter_by(id=userId).first()
    if form.validate_on_submit():
        user.name=form.name.data
        user.last_name=form.last_name.data
        user.email=form.email.data
        user.p_number=form.p_number.data
        user.line1=form.line1.data
        user.line2=form.line2.data
        user.postCode=form.postCode.data
        user.city=form.city.data
        db.session.add(user)
        db.session.commit()
        return redirect((url_for('tenants')))
    return render_template('user_form.html',form=form, user=user)


@app.route('/update_tenant02', methods=['POST'])
def update_tenant02():
    pass



@app.route('/invoice01', methods=['POST'])
def invoice01():
    userId = int(request.form['userId'])
    salonId = int(request.form['salonId'])
    session['userId']=userId
    session['salonId']=salonId
    session['invoiceId']=Invoices.query.all()[-1].id
    session['date']=str(datetime.now().date())
    return render_template('invoice01.html',
                            user=User.query.filter_by(id=session['userId']).first(),
                            salon=Salon.query.filter_by(id=session['salonId']).first(),
                            date=datetime.now().date())


@app.route('/invoivc02', methods=['POST'])
def invoice02():
    invoiceData = request.form
    print(invoiceData)
    serviceList=[]
    for item in invoiceData.keys():
        if item.split('_')[0]=='item' and invoiceData[item] != '':
            serviceList.append([invoiceData['item_'+str(item.split('_')[1])],
                                float(invoiceData['value_'+str(item.split('_')[1])]),
                                invoiceData['description_'+str(item.split('_')[1])],
                                int(invoiceData['quantity_'+str(item.split('_')[1])]), # item quantity
                                float(invoiceData['value_'+str(item.split('_')[1])])*int(invoiceData['quantity_'+str(item.split('_')[1])]),
                                int(item.split('_')[1])]) #item number
    valueList = [value[4] for value in serviceList]
    total = sum(valueList)
    session['invoiceData']=invoiceData
    session['serviceList']=serviceList
    session['total']=total
    invoice_to_send = Invoices.query.filter_by(id=session['invoiceId']).first()
    invoice_to_send.receiver_user_id=session['userId']
    invoice_to_send.salon_user_id=session['salonId']
    invoice_to_send.date=session['date']
    invoice_to_send.text=json.dumps(session['serviceList'])
    db.session.commit()
    return render_template('example1-1.html',
                            invoiceData=session['invoiceData'],
                            user=User.query.filter_by(id=int(session['userId'])).first(),
                            salon=Salon.query.filter_by(id=int(session['salonId'])).first(),
                            invoiceId=session['invoiceId'],
                            date=session['date'],
                            serviceList=session['serviceList'],
                            total=session['total'])


@app.route('/send_mail/')
def send_mail():
    try:
        msg = Message('Invoice form 2J-ART Ltd.',
        sender='info@hofhsalon.co.uk',
        recipients=[User.query.filter_by(id=int(session['userId'])).first().email])
        msg.add_recipient("artursnatarovs@gmail.com")
        msg.body = "If you can't read this email please contact us."
        msg.html = render_template('example1.html',
                                    invoiceData=session['invoiceData'],
                                    user=User.query.filter_by(id=int(session['userId'])).first(),
                                    salon=Salon.query.filter_by(id=int(session['salonId'])).first(),
                                    invoiceId=session['invoiceId'],
                                    date=session['date'],
                                    serviceList=session['serviceList'],
                                    total=session['total'])
        mail.send(msg)
        msg.subject='COPY of Invoice form 2J-ART Ltd.'
        msg.recipients=['info@hofhsalon.co.uk']
        mail.send(msg)
    except Exception as e:
        return str(e)


    new_invoice=Invoices()
    db.session.add(new_invoice)
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/show_invoices')
def show_invoices():
    return render_template('show_invoices.html', invoices=reversed(Invoices.query.all()), Salon=Salon)


if __name__ == '__main__':
    db.create_all()
    initial_invoice()
    app.run(debug=True)



#.\envir\Scripts\flask db migrate -m "added breed column"
#.\envir\Scripts\flask db upgrade
