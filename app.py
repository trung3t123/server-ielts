from flask import Flask,request,jsonify
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy import func
from sqlalchemy import text
import os 
import psycopg2

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://shnzpkrlakzyac:3dda21e6291cc2a070f7982051212ba2bee431042e657ea65a09328472d93fcb@ec2-174-129-255-39.compute-1.amazonaws.com:5432/d9719hkdsnjnvn'
app.config['SQLALCHEMY_TRACKING_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)
CORS(app)

class Student(db.Model) :
    studentid = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(50))
    password = db.Column(db.String(20))
    marks = db.Column(db.Integer)
    email = db.Column(db.String(50))
    

    def __init__(self, username,password,marks,email):
        self.username = username
        self.password = password
        self.marks = marks
        self.email = email

class Question(db.Model):
    questionid = db.Column(db.Integer,primary_key= True)
    categoryid = db.Column(db.Integer)
    content = db.Column(db.String(300))
    correctanswer = db.Column(db.String(100))
    answera = db.Column(db.String(100))
    answerb = db.Column(db.String(100))
    answerc = db.Column(db.String(100))
    answerd = db.Column(db.String(100))

    def __init__(self, questionid, categoryid, mark,content,correctanswer,answera,answerb,answerc,answerd):
        self.questionid =questionid
        self.categoryid = categoryid
        self.content = content
        self.correctanswer = correctanswer
        self.answera = answera
        self.answerb = answerb
        self.answerc = answerc
        self.answerd = answerd
  

class QuestionSchema(ma.Schema):
    class Meta: 
        fields = ('questionid','categoryid','content','correctanswer','answera','answerb','answerc','answerd')

class StudentSchema(ma.Schema):
     class Meta : 
        fields = ('studentid', 'username', 'password','marks','email')

student_schema = StudentSchema()
students_schema = StudentSchema(many = True)
question_schema = QuestionSchema()
questions_schema = QuestionSchema(many= True)

@app.route('/showquestion', methods = ['GET'])
def showquestion():
    question = Question.query.all()
    result = questions_schema.jsonify(question)
    return result

@app.route('/API/show80Question', methods = ['GET'])
def show80Question():
    question = Question.query.order_by(func.random()).limit(80).all()
    result = questions_schema.jsonify(question)
    return result
#uninstalled unusing package
# asdaDSdsafaf

@app.route('/API/show5Question', methods = ['GET'])
def show5Question():
    question = Question.query.order_by(func.random()).limit(5).all()
    result = questions_schema.jsonify(question)
    return result

@app.route('/loginStudentName=<StudentName>',methods =['GET'])
def login(StudentName):
    student = Student.query.filter_by(username = StudentName).first()
    result = student_schema.jsonify(student)
    return result

@app.route('/api/register',methods = ['POST'])
def register():
   user = Student(username =request.json["username"],email = request.json["email"],password = request.json["password"])
   db.session.add(user)
   db.session.commit()
   return '<p>Data update</p>'


# @app.route('/register',methods = ['POST'])
# def register(username,password,marks,email):
#     student = Student()

if __name__ == '__main__':
    app.run(debug=True)