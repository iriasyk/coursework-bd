import sqlalchemy
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

from forms.user_form import QuestionTable, QuestionTableUpdate, StudentTableForm, StudentTableFormUpdate, SubjectTableForm, AnswerTableForm
from sklearn.neural_network import MLPClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import MinMaxScaler, OneHotEncoder, FunctionTransformer
from sklearn.compose import ColumnTransformer
import numpy as np

import plotly
import json
from flask_sqlalchemy import SQLAlchemy
import plotly.graph_objs as go
from sqlalchemy.sql import func

app = Flask(__name__)
app.secret_key = 'key'

ENV = 'prod'

if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:bd@localhost/postgres'
else:
    app.debug = False
    app.config[
        'SQLALCHEMY_DATABASE_URI'] = 'postgres://wwgngemtejetor:043405da3c53bb9f6040f2f59492e609ea759dd3a97e1742bffaffb943e21824@ec2-3-220-90-40.compute-1.amazonaws.com:5432/dai73et06jeb7t'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class ormStudent(db.Model):
    __tablename__ = 'Students'

    email = db.Column(db.String(30), primary_key=True)
    name_student = db.Column(db.String(30), nullable=False)
    status_at_the_departament = db.Column(db.String(20), nullable=False)
    grade_at_the_departament = db.Column(db.Integer, nullable=False)
    expected_grade_point = db.Column(db.Integer, nullable=False)
    mood = db.Column(db.String(20), nullable=False)
    subject = db.Column(db.String(80), db.ForeignKey('Subject.subject'), nullable=False)
    answer = db.Column(db.String(20), db.ForeignKey('Answer.answer'), nullable=False)


class ormQuestion(db.Model):
    __tablename__ = 'Question'

    subject_matter = db.Column(db.String(20), primary_key=True)
    question = db.Column(db.String(150), nullable=False)


class ormSubject(db.Model):
    __tablename__ = 'Subject'

    subject = db.Column(db.String(80), primary_key=True)
    students_ = db.relationship('ormStudent')


class ormAnswer(db.Model):
    __tablename__ = 'Answer'

    answer = db.Column(db.String(20), primary_key=True)
    students___ = db.relationship('ormStudent')


db.drop_all()
db.create_all()
db.session.query(ormStudent).delete()
db.session.query(ormQuestion).delete()
db.session.query(ormSubject).delete()
db.session.query(ormAnswer).delete()

Student1 = ormStudent(email='korinyosyp@gmail.com', name_student='Joseph Korin', status_at_the_departament='bachelor', grade_at_the_departament=85, expected_grade_point=85, mood='enthusiastic', subject='Statistical modeling', answer='{5, 4}')
Student2 = ormStudent(email='anastacyg7@gmail.com', name_student='Grigorenko Anastasia', status_at_the_departament='bachelor', grade_at_the_departament=85, expected_grade_point=100, mood='enthusiastic', subject='DB', answer='{5, 3}')
Student3 = ormStudent(email='s1a2s3h4a656@gmail.com', name_student='Hrydko Sasha', status_at_the_departament='bachelor', grade_at_the_departament=80, expected_grade_point=85, mood='enthusiastic', subject='DB', answer='{5, 3}')
Student4 = ormStudent(email='lex.buts98@gmail.com', name_student='Aleksandr Buts', status_at_the_departament='bachelor', grade_at_the_departament=75, expected_grade_point=89, mood='enthusiastic', subject='Systems engineering systems of Data Science', answer='{5, 5}')
Student5 = ormStudent(email='sergiy45ap@gmail.com', name_student='Serhii Muzhylivskyi', status_at_the_departament='graduate', grade_at_the_departament=75, expected_grade_point=100, mood='enthusiastic', subject='Construction of REST-services', answer='{5, 3}')
Student6 = ormStudent(email='trishyna1998anutka@gmail.com', name_student='Anna Trishyna', status_at_the_departament='graduate', grade_at_the_departament=78, expected_grade_point=90, mood='enthusiastic', subject='Front-end Development', answer='{5, 3}')
Student7 = ormStudent(email='zlata_khodos@ukr.net', name_student='Zlata Khodos', status_at_the_departament='bachelor', grade_at_the_departament=88, expected_grade_point=95, mood='disappointed', subject='System analysis', answer='{5, 2}')
Student8 = ormStudent(email='zlata_khodos2@ukr.net', name_student='Zlata Khodos', status_at_the_departament='bachelor', grade_at_the_departament=88, expected_grade_point=75, mood='enthusiastic', subject='DB', answer='{5, 5}')
Student9 = ormStudent(email='zlata_khodos3@ukr.net', name_student='Zlata Khodos', status_at_the_departament='bachelor', grade_at_the_departament=88, expected_grade_point=90, mood='disappointed', subject='Software quality assurance', answer='{4, 2}')
Student10 = ormStudent(email='a.argent383@gmail.com', name_student='Olha Milevska', status_at_the_departament='bachelor', grade_at_the_departament=75, expected_grade_point=85, mood='enthusiastic', subject='Statistical modeling', answer='{4, 3}')
Student11 = ormStudent(email='bellamy1313@gmail.com', name_student='Servatmand Mariam', status_at_the_departament='bachelor', grade_at_the_departament=78, expected_grade_point=79, mood='disappointed', subject='Structure and interpretation of computer programs', answer='{4, 3}')
Student12 = ormStudent(email='andriyha98@gmail.com', name_student='Hladkiy Andriy', status_at_the_departament='bachelor', grade_at_the_departament=65, expected_grade_point=75, mood='disappointed', subject='Front-end Development', answer='{4, 2}')
Student13 = ormStudent(email='kingaskong12666@gmail.com', name_student='Yevlentiev Mykhailo', status_at_the_departament='bachelor', grade_at_the_departament=68, expected_grade_point=70, mood='enthusiastic', subject='Front-end Development', answer='{5, 3}')
Student14 = ormStudent(email='yarok1999@gmail.com', name_student='Yaroslav Artemenko', status_at_the_departament='bachelor', grade_at_the_departament=75, expected_grade_point=90, mood='enthusiastic', subject='C++ programming', answer='{5, 4}')
Student15 = ormStudent(email='adolphina13@gmail.com', name_student='Kateryna Buchynska', status_at_the_departament='bachelor', grade_at_the_departament=80, expected_grade_point=60, mood='disappointed', subject='C++ programming', answer='{4, 3}')
# Student16 = ormStudent(email='name.random14@gmail.com', name_student='Name Random', status_at_the_departament='bachelor', grade_at_the_departament=68, expected_grade_point=75, mood='enthusiastic', subject='Scala programming', answer='{4, 3}')
# Student17 = ormStudent(email='name.random15@gmail.com', name_student='Name Random', status_at_the_departament='master', grade_at_the_departament=72, expected_grade_point=85, mood='enthusiastic', subject='Scala programming', answer='{5, 5}')
# Student18 = ormStudent(email='name.random16@gmail.com', name_student='Name Random', status_at_the_departament='bachelor', grade_at_the_departament=82, expected_grade_point=100, mood='disappointed', subject='Scala programming', answer='{4, 4}')
# Student19 = ormStudent(email='name.random17@gmail.com', name_student='Name Random', status_at_the_departament='graduate', grade_at_the_departament=65, expected_grade_point=60, mood='enthusiastic', subject='Scala programming', answer='{3, 3}')
# Student20 = ormStudent(email='name.random18@gmail.com', name_student='Name Random', status_at_the_departament='bachelor', grade_at_the_departament=73, expected_grade_point=70, mood='disappointed', subject='Scala programming', answer='{2, 2}')
# Student21 = ormStudent(email='name.random19@gmail.com', name_student='Name Random', status_at_the_departament='graduate', grade_at_the_departament=91, expected_grade_point=80, mood='enthusiastic', subject='Scala programming', answer='{4, 5}')

Question1 = ormQuestion(subject_matter='utility in points', question='What is the utility in points?')
Question2 = ormQuestion(subject_matter='difficulty in points', question='What is the difficulty in points?')

Subject1 = ormSubject(subject='DB')
Subject2 = ormSubject(subject='Java programming')
Subject3 = ormSubject(subject='C# programming')
Subject4 = ormSubject(subject='C++ programming')
Subject5 = ormSubject(subject='Software quality assurance')
Subject6 = ormSubject(subject='Automated software testing')
Subject7 = ormSubject(subject='Cryptographic methods of information protection')
Subject8 = ormSubject(subject='Multimedia software and tools')
Subject9 = ormSubject(subject='Mathematical foundations of computer graphics and multimedia')
Subject10 = ormSubject(subject='Algorithmic bases of computational geometry and computer graphics')
Subject11 = ormSubject(subject='Functional programming')
Subject12 = ormSubject(subject='Structure and interpretation of computer programs')
Subject13 = ormSubject(subject='Scala programming')
Subject14 = ormSubject(subject='Mathematical programming')
Subject15 = ormSubject(subject='Practical aspects of numerical optimization')
Subject16 = ormSubject(subject='Nonlinear programming')
Subject17 = ormSubject(subject='Random processes')
Subject18 = ormSubject(subject='Statistical modeling')
Subject19 = ormSubject(subject='Markov models')
Subject20 = ormSubject(subject='Front-end Development')
Subject21 = ormSubject(subject='Construction of REST-services')
Subject22 = ormSubject(subject='Web data visualization technologies')
Subject23 = ormSubject(subject='Data Science for Business')
Subject24 = ormSubject(subject='Manipulating DataFrames with Pandas')
Subject25 = ormSubject(subject='Introduction to Data Engineering')
Subject26 = ormSubject(subject='Systems of Data Science')
Subject27 = ormSubject(subject='Systems engineering of Data Science')
Subject28 = ormSubject(subject='Systems engineering systems of Data Science')
Subject29 = ormSubject(subject='System analysis')
Subject30 = ormSubject(subject='Fundamentals of decision theory')
Subject31 = ormSubject(subject='Fundamentals of information systems theory')


Answer1 = ormAnswer(answer='{0, 1}')
Answer2 = ormAnswer(answer='{0, 2}')
Answer3 = ormAnswer(answer='{0, 3}')
Answer4 = ormAnswer(answer='{0, 4}')
Answer5 = ormAnswer(answer='{0, 5}')
Answer6 = ormAnswer(answer='{1, 0}')
Answer7 = ormAnswer(answer='{1, 1}')
Answer8 = ormAnswer(answer='{1, 2}')
Answer9 = ormAnswer(answer='{1, 3}')
Answer10 = ormAnswer(answer='{1, 4}')
Answer11 = ormAnswer(answer='{1, 5}')
Answer12 = ormAnswer(answer='{2, 0}')
Answer13 = ormAnswer(answer='{2, 1}')
Answer14 = ormAnswer(answer='{2, 2}')
Answer15 = ormAnswer(answer='{2, 3}')
Answer16 = ormAnswer(answer='{2, 4}')
Answer17 = ormAnswer(answer='{2, 5}')
Answer18 = ormAnswer(answer='{3, 0}')
Answer19 = ormAnswer(answer='{3, 1}')
Answer20 = ormAnswer(answer='{3, 2}')
Answer21 = ormAnswer(answer='{3, 3}')
Answer22 = ormAnswer(answer='{3, 4}')
Answer23 = ormAnswer(answer='{3, 5}')
Answer24 = ormAnswer(answer='{4, 0}')
Answer25 = ormAnswer(answer='{4, 1}')
Answer26 = ormAnswer(answer='{4, 2}')
Answer27 = ormAnswer(answer='{4, 3}')
Answer28 = ormAnswer(answer='{4, 4}')
Answer29 = ormAnswer(answer='{4, 5}')
Answer30 = ormAnswer(answer='{5, 0}')
Answer31 = ormAnswer(answer='{5, 1}')
Answer32 = ormAnswer(answer='{5, 2}')
Answer33 = ormAnswer(answer='{5, 3}')
Answer34 = ormAnswer(answer='{5, 4}')
Answer35 = ormAnswer(answer='{5, 5}')

# Subject1.students_.append(Student1)

db.session.add_all([Student1, Student2, Student3, Student4, Student5, Student6, Student7, Student8, Student9, Student10, Student11, Student12, Student13, Student14, Student15])
db.session.add_all([Subject1, Subject2, Subject3, Subject4, Subject5, Subject6, Subject7, Subject8, Subject9, Subject10, Subject11, Subject12, Subject13, Subject14, Subject15, Subject16, Subject17, Subject18, Subject19, Subject20, Subject21, Subject22, Subject23, Subject24, Subject25, Subject26, Subject27, Subject28, Subject29, Subject30, Subject31])
db.session.add_all([Question1, Question2])
db.session.add_all([Answer1, Answer2, Answer3, Answer4, Answer5, Answer6, Answer7, Answer8, Answer9, Answer10, Answer11, Answer12, Answer13, Answer14, Answer15, Answer16, Answer17, Answer18, Answer19, Answer20, Answer21, Answer22, Answer23, Answer24, Answer25, Answer26, Answer27, Answer28, Answer29, Answer30, Answer31, Answer32, Answer33, Answer34, Answer35])

db.session.commit()


# main page
@app.route('/', methods=['GET', 'POST'])
def root():
    return render_template('index.html')


# students
@app.route('/students', methods=['GET'])
def students():
    result = db.session.query(ormStudent).all()

    return render_template('student.html', students=result)


@app.route('/new_student', methods=['GET', 'POST'])
def new_student():
    form = StudentTableForm()

    if request.method == 'POST':
        if form.validate() == False:
            return render_template('student_form.html', form=form, form_name="New student", action="new_student")
        else:
            new_user = ormStudent(
                email=form.email.data,
                name_student=form.name_student.data,
                status_at_the_departament=form.status_at_the_departament.data,
                grade_at_the_departament=form.grade_at_the_departament.data,
                expected_grade_point=form.expected_grade_point.data,
                mood=form.mood.data,
                subject=form.subject.data,
                answer=form.answer.data
            )
            try:
                db.session.add(new_user)
                db.session.commit()
                return redirect('/students')
            except:
                form.email.errors = ['Maybe this name already exists!']
                form.subject.errors = ['Perhaps this name does not exist, from the parent tables where it should exist!']
                form.answer.errors = ['Perhaps this name does not exist, from the parent tables where it should exist!']
                return render_template('student_form.html', form=form, form_name="New student", action="new_student")

    return render_template('student_form.html', form=form, form_name="New student", action="new_student")


@app.route('/edit_students/<string:x>', methods=['GET', 'POST'])
def edit_student(x):
    form = StudentTableFormUpdate()

    user = db.session.query(ormStudent).filter(ormStudent.email == x).one()

    if request.method == 'GET':
        return render_template('student_form_update.html', form=form, form_name="Edit student")

    else:
        if form.validate() == False:
            return render_template('student_form_update.html', form=form, form_name="Edit student")
        else:
            user.name_student = form.name_student.data
            user.status_at_the_departament = form.status_at_the_departament.data
            user.grade_at_the_departament = form.grade_at_the_departament.data
            user.expected_grade_point = form.expected_grade_point.data
            user.mood = form.mood.data
            db.session.commit()

            return render_template('ok.html')


@app.route('/delete_student/<string:x>', methods=['GET'])
def delete_student(x):
    result = db.session.query(ormStudent).filter(ormStudent.email == x).one()

    db.session.delete(result)
    db.session.commit()

    return render_template('ok.html')


# answer
@app.route('/answer', methods=['GET'])
def answer():
    result = db.session.query(ormAnswer).all()

    return render_template('answer.html', answers=result)


@app.route('/new_answer', methods=['GET', 'POST'])
def new_answer():
    form = AnswerTableForm()

    if request.method == 'POST':
        if form.validate() == False:
            return render_template('answer_form.html', form=form, form_name="New Answers", action="new_answer")
        else:
            new_user = ormAnswer(
                answer=form.answer.data
            )

            try:
                db.session.add(new_user)
                db.session.commit()
                return redirect('/answer')
            except:
                form.answer.errors = ['This name already exists!']
                return render_template('answer_form.html', form=form, form_name="New user", action="new_answer")

    return render_template('answer_form.html', form=form, form_name="New Answers", action="new_answer")


@app.route('/delete_answer/<string:x>', methods=['GET'])
def delete_answer(x):
    result = db.session.query(ormAnswer).filter(ormAnswer.answer == x).one()
    result1 = db.session.query(ormStudent).filter(ormStudent.answer == x).all()

    for i in result1:
        db.session.delete(i)

    db.session.delete(result)
    db.session.commit()

    return render_template('ok.html')


# subject
@app.route('/subject', methods=['GET'])
def departament():
    result = db.session.query(ormSubject).all()

    return render_template('subject.html', subjects=result)


@app.route('/new_subject', methods=['GET', 'POST'])
def new_departament():
    form = SubjectTableForm()

    if request.method == 'POST':
        if form.validate() == False:
            return render_template('subject_form.html', form=form, form_name="New Subject", action="new_subject")
        else:
            new_user = ormSubject(
                subject=form.subject.data
            )
            try:
                db.session.add(new_user)
                db.session.commit()
                return redirect('/subject')
            except:
                form.subject.errors = ['This name already exists!']
                return render_template('subject_form.html', form=form, form_name="New Subject", action="new_subject")

    return render_template('subject_form.html', form=form, form_name="New Subject", action="new_subject")


@app.route('/delete_subject/<string:x>', methods=['GET'])
def delete_departament(x):
    result = db.session.query(ormSubject).filter(ormSubject.subject == x).one()
    result1 = db.session.query(ormStudent).filter(ormStudent.subject == x).all()

    for i in result1:
        db.session.delete(i)

    db.session.delete(result)
    db.session.commit()

    return render_template('ok.html')


# question
@app.route('/question', methods=['GET'])
def form():
    result = db.session.query(ormQuestion).all()

    return render_template('question.html', questions=result)


@app.route('/new_question', methods=['GET', 'POST'])
def new_form():
    form = QuestionTable()

    if request.method == 'POST':
        if form.validate() == False:
            return render_template('question_form.html', form=form, form_name="Question form")

        else:
            new_user = ormQuestion(
                subject_matter=form.subject_matter.data,
                question=form.question.data
            )
            try:
                db.session.add(new_user)
                db.session.commit()
                return redirect('/question')
            except:
                form.subject_matter.errors = ['This name already exists!']
                return render_template('question_form.html', form=form, form_name="New question")

    return render_template('question_form.html', form=form, form_name="New question")


@app.route('/edit_question/<string:x>', methods=['GET', 'POST'])
def edit_form(x):
    form = QuestionTableUpdate()
    user = db.session.query(ormQuestion).filter(ormQuestion.subject_matter == x).one()

    if request.method == 'GET':
        return render_template('question_form_update.html', form=form, form_name="Edit question")


    elif request.method == 'POST':

        if form.validate() == False:
            return render_template('question_form_update.html', form=form, form_name="Edit question")
        else:
            user.question = form.question.data
            db.session.commit()

            return render_template('ok.html')


@app.route('/delete_question/<string:x>', methods=['GET'])
def delete_form(x):
    result = db.session.query(ormQuestion).filter(ormQuestion.subject_matter == x).one()

    db.session.delete(result)
    db.session.commit()

    return render_template('ok.html')


# dashboard
@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    query1 = (
        db.session.query(
            ormStudent.answer,
            func.count(ormStudent.email).label('email')
        ).
            group_by(ormStudent.answer)
    ).all()

    query2 = (
        db.session.query(
            ormStudent.mood,
            func.count(ormStudent.email).label('email')
        ).
            group_by(ormStudent.mood)
    ).all()

    query3 = (
        db.session.query(
            ormStudent.expected_grade_point,
            func.count(ormStudent.grade_at_the_departament).label('expected_grade_point')
        ).
            group_by(ormStudent.expected_grade_point)
    ).all()

    query4 = (
        db.session.query(
            ormStudent.status_at_the_departament,
            func.count(ormStudent.email).label('email')
        ).
            group_by(ormStudent.status_at_the_departament)
    ).all()

    query5 = (
        db.session.query(
            ormStudent.subject,
            func.count(ormStudent.email).label('email')
        ).
            group_by(ormStudent.subject)
    ).all()

    answer, email = zip(*query1)
    bar = go.Bar(
        x=answer,
        y=email
    )

    mood, email = zip(*query2)
    pie = go.Pie(
        labels=mood,
        values=email
    )

    grade_at_the_departament, expected_grade_point = zip(*query3)
    scat = go.Scatter(
        x=grade_at_the_departament,
        y=expected_grade_point,
        mode='markers'
    )

    status_at_the_departament, email = zip(*query4)
    bar2 = go.Bar(
        x=status_at_the_departament,
        y=email
    )

    subject, email = zip(*query5)
    bar3 = go.Bar(
        x=subject,
        y=email
    )

    status_at_the_departament, email = zip(*query4)
    pie2 = go.Pie(
        labels=status_at_the_departament,
        values=email
    )

    subject, email = zip(*query5)
    pie3 = go.Pie(
        labels=subject,
        values=email
    )

    data = {
        "bar": [bar],
        "bar2": [bar2],
        "bar3": [bar3],
        "pie": [pie],
        "pie2": [pie2],
        "pie3": [pie3],
        "scatter": [scat]
    }
    graphsJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)

    x = []
    y = []

    for i in query3:
        x.append(i[0])
        y.append(i[1])
    corr_coef = np.corrcoef(x, y)[0][1]

    return render_template('dashboard.html', graphsJSON=graphsJSON, corr_coef=corr_coef)


#     =================================================================================================

if __name__ == '__main__':
    app.run(debug=True)
