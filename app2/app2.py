from flask import Flask, request, flash, url_for, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
from flask import json
from flask_api import status
from flask import Response
from flask_mysqldb import MySQL
import redis

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='mysql://root:test@mysql:3306/expsys'
app.config['SECRET_KEY']='MYNAMEIS'

db=SQLAlchemy(app)

class expsys(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(40))
    email=db.Column(db.String(40))
    category=db.Column(db.String(40))
    description=db.Column(db.String(40))
    link=db.Column(db.String(80))
    estimated_costs=db.Column(db.String(40))
    submit_date=db.Column(db.String(40))
    status=db.Column(db.String(40))
    decision_date=db.Column(db.String(40))

    def __init__(self, name,email,category,description,link,estimated_costs,submit_date,status,decision_date):
        self.name=name
        self.email=email
        self.category=category
        self.description=description
        self.link=link
        self.estimated_costs=estimated_costs
        self.submit_date=submit_date
        self.status=status
        self.decision_date=decision_date


@app.route('/')
def show_all():
   return "hello from 6702"

@app.route('/v1/expenses', methods = ['GET', 'POST'])
def expensespost():
   if request.method == 'POST':


            data=request.get_json(force=True)
            employee=expsys(name=data['name'],email=data['email'],category=data['category'],
            description=data['description'],link=data['link'],estimated_costs=data['estimated_costs'],
            submit_date=data['submit_date'],status="pending",decision_date="")
            db.session.add(employee)
            db.session.commit()
            #flash('Record was successfully added')
            #queryname=data['name']
            #employee=expsys.query.filter_by(name=queryname).first()

            temp={
                'id':employee.id,
                'name':employee.name,
                'email':employee.email,
                'category':employee.category,
                'description':employee.description,
                'link':employee.link,
                'estimated_costs':employee.estimated_costs,
                'submit_date':employee.submit_date,
                'status':employee.status,
                'decision_date':employee.decision_date
             }
            return Response(response=json.dumps(temp),status=201,mimetype="application/json")
            #return resp

@app.route('/v1/expenses/<int:exp_id>', methods = ['GET', 'POST','DELETE','PUT'])
def expensesget(exp_id):
    if request.method == 'GET':
            employee=expsys.query.filter_by(id=exp_id).first_or_404()


            temp={
                'id':employee.id,
                'name':employee.name,
                'email':employee.email,
                'category':employee.category,
                'description':employee.description,
                'link':employee.link,
                'estimated_costs':employee.estimated_costs,
                'submit_date':employee.submit_date,
                'status':employee.status,
                'decision_date':employee.decision_date
             }
            resp=Response(response=json.dumps(temp),status="200",mimetype="application/json")
            return resp


    elif request.method=='PUT':
            data=request.get_json(force = True)
            employee=expsys.query.filter_by(id=exp_id).first()
            employee.estimated_costs=data['estimated_costs']
            db.session.commit()
            temp={ 'estimated_costs':employee.estimated_costs}
            resp=Response(response=json.dumps(temp),status="202",mimetype="application/json")
            return resp
    elif request.method == 'DELETE':
            emp=expsys.query.filter_by(id=exp_id).first()
            db.session.delete(emp)
            db.session.commit()
            resp=Response(response="NO content",status="204",mimetype="application/json")
            return resp






if __name__ == '__main__':
    r = redis.StrictRedis(host='redis', port=6379, db=0)
    r.set(2, '6702')
    db.create_all()
    app.run(debug = True, host = '0.0.0.0',port=6702)
