from flask import Flask,request,jsonify
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy import func
from sqlalchemy import text
import os 

app = Flask(__name__)
app.config['DATABASE_URL'] = 'postgresql://trung:trung@localhost/englishQuest'
app.config['SQLALCHEMY_TRACKING_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)
CORS(app)

class Student(db.Model) :
    studentid = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(50))
    password = db.Column(db.String(20))
    marks = db.Column(db.Integer)

    def __init__(self, username,password,marks):
        self.username = username
        self.password = password
        self.marks = marks

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
        fields = ('studentid', 'username', 'password','marks')



engquest_schema = StudentSchema()
engquests_schema = StudentSchema(many = True)
question_schema = QuestionSchema()
questions_schema = QuestionSchema(many= True)


@app.route('/showquestion', methods = ['GET'])
def showquestion():
    question = Question.query.all()
    result = questions_schema.jsonify(question)
    return result



if __name__ == '__main__':
    app.run(debug=True)