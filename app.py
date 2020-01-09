from flask import Flask, request, jsonify
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy import func
from sqlalchemy import text
from sqlalchemy import desc
import os
import psycopg2


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://shnzpkrlakzyac:3dda21e6291cc2a070f7982051212ba2bee431042e657ea65a09328472d93fcb@ec2-174-129-255-39.compute-1.amazonaws.com:5432/d9719hkdsnjnvn'
app.config['SQLALCHEMY_TRACKING_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)
CORS(app)

class Student(db.Model):
    studentid = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    password = db.Column(db.String(20))
    email = db.Column(db.String(50))

    def __init__(self, username,password,email):
        self.username = username
        self.password = password
        self.email = email

class StudentSchema(ma.Schema):
    class Meta:
        fields = ('studentid', 'username', 'password', 'email')

class Question(db.Model):
    questionid = db.Column(db.Integer, primary_key=True)
    categoryid = db.Column(db.Integer)
    content = db.Column(db.String(300))
    correctanswer = db.Column(db.String(100))
    answera = db.Column(db.String(100))
    answerb = db.Column(db.String(100))
    answerc = db.Column(db.String(100))
    answerd = db.Column(db.String(100))

    def __init__(self, questionid, categoryid, mark, content, correctanswer, answera, answerb, answerc, answerd):
        self.questionid = questionid
        self.categoryid = categoryid
        self.content = content
        self.correctanswer = correctanswer
        self.answera = answera
        self.answerb = answerb
        self.answerc = answerc
        self.answerd = answerd

class QuestionSchema(ma.Schema):
    class Meta:
        fields = ('questionid', 'categoryid', 'content',
                  'correctanswer', 'answera', 'answerb', 'answerc', 'answerd')

class Record(db.Model):
    recordid = db.Column(db.Integer, primary_key = True)
    studentid = db.Column(db.Integer)
    date = db.Column(db.String(30))
    marks = db.Column(db.Integer)

    def __init__(self, studentid, date, marks):
        self.studentid = studentid
        self.date = date
        self.marks = marks

class RecordSchema(ma.Schema):
    class Meta:
        fields = ('studentid', 'date', 'marks')

record_schema = RecordSchema()
records_schema = RecordSchema(many=True)

student_schema = StudentSchema()
students_schema = StudentSchema(many=True)
question_schema = QuestionSchema()
questions_schema = QuestionSchema(many=True)


@app.route('/showquestion', methods=['GET'])
def showquestion():
    question = Question.query.all()
    result = questions_schema.jsonify(question)
    return result

@app.route('/api/showTrainingQuestion=<categoryid>', methods =['GET'])
def showTrainingQuestion(categoryid): 
    question =Question.query.filter_by(categoryid = categoryid).order_by(func.random()).limit(5).all()
    result = questions_schema.jsonify(question)
    return result


@app.route('/API/show80Question', methods=['GET'])
def show80Question():
    question = Question.query.order_by(func.random()).limit(80).all()
    result = questions_schema.jsonify(question)
    return result
# uninstalled unusing package
# asdaDSdsafaf


@app.route('/API/show5Question', methods=['GET'])
def show5Question():
    question = Question.query.order_by(func.random()).limit(5).all()
    result = questions_schema.jsonify(question)
    return result


@app.route('/loginStudentName=<StudentName>', methods=['GET'])
def login(StudentName):
    student = Student.query.filter_by(username=StudentName).first()
    result = student_schema.jsonify(student)
    return result

#api register
@app.route('/api/register',methods = ['POST'])
def register():
    student = Student(username =request.json["username"],email = request.json["email"],password = request.json["password"])
    db.session.add(student)
    db.session.commit()
    return '<p>Data update</p>'

@app.route('/api/show-question-topic=<categoryid>', methods = ['GET'])
def show10Question(categoryid):
   questions = Question.query.filter_by(categoryid = categoryid).order_by(func.random()).limit(10).all()
   result = questions_schema.jsonify(questions)
   return result

   
@app.route('/api/testQuestions', methods=['GET'])
def testQuestions():
    question1 = Question.query.order_by(func.random()).filter_by(categoryid="1").limit(15).all()
    question2 = Question.query.order_by(func.random()).filter_by(categoryid="2").limit(15).all()
    question3 = Question.query.order_by(func.random()).filter_by(categoryid="3").limit(15).all()
    question = question1 + question2 + question3

    # session.query(Customer).join(Invoice).filter(Invoice.amount == 8500)
    result = questions_schema.jsonify(question)
    return result

#api insert mark to db
@app.route('/api/insert_mark',methods = ['POST'])
def insertMark():
   mark = Record(studentid =request.json["studentId"],date = request.json["date"],marks = request.json["marks"])
   db.session.add(mark)
   db.session.commit()
   return '<p>Data update</p>'
#api get test history
@app.route('/api/show-history=<userId>', methods = ['GET'])
def showHistory(userId):
   marks = Record.query.filter_by(userId = studentid).order_by(date).all()
   result = records_schema.jsonify(marks)
   return result
#api get mark oder by descending
@app.route('/api/show-all-mark', methods = ['GET'])
def showAllMarks():
   marks = Record.query.order_by(desc(Record.marks)).all()
   result = records_schema.jsonify(marks)
   return result

if __name__ == '__main__':
    app.run(debug=True)
    
