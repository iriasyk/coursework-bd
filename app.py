from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

from forms.user_form import FormTable, FormTableUpdate, StudentTableForm, StudentTableFormUpdate, DepartamentTableForm, \
    DepartamentTableFormUpdate, AnswersTableForm, AnswersTableFormUpdate, NeuralForm
from sklearn.neural_network import MLPClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import MinMaxScaler, OneHotEncoder, FunctionTransformer
from sklearn.compose import ColumnTransformer
import numpy as np
import plotly.graph_objs as go

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
        'SQLALCHEMY_DATABASE_URI'] = 'postgres://ysddjibomrqxyq:50528618c5ff45de5797f6383377f9c939bb22c0922bedfe3fa2f79aa73bc7b9@ec2-23-21-249-0.compute-1.amazonaws.com:5432/dfc1evd9hjiukk'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class ormStudent(db.Model):
    __tablename__ = 'Students'

    student_email = db.Column(db.String(30), primary_key=True)
    department_number = db.Column(db.Integer, db.ForeignKey('Departaments.department_number'), nullable=False)
    form_name = db.Column(db.String(30), db.ForeignKey('Forms.form_name'), nullable=False)
    answers_on_questions = db.Column(db.String(30), db.ForeignKey('Answers.answers_on_questions'), nullable=False)
    student_name = db.Column(db.String(20), nullable=False)
    student_age = db.Column(db.Integer, nullable=False)
    student_gender = db.Column(db.String(10), nullable=False)
    student_location = db.Column(db.String(15), nullable=False)
    family_state = db.Column(db.String(10), nullable=False)


class ormForm(db.Model):
    __tablename__ = 'Forms'

    form_name = db.Column(db.String(30), primary_key=True)
    questions = db.Column(db.String(150), nullable=False)

    students__ = db.relationship('ormStudent')


class ormDepartament(db.Model):
    __tablename__ = 'Departaments'

    department_number = db.Column(db.Integer, primary_key=True)
    departament_name = db.Column(db.String(30), nullable=False)
    departament_location = db.Column(db.String(15), nullable=False)

    students_ = db.relationship('ormStudent')


class ormAnswer(db.Model):
    __tablename__ = 'Answers'

    answers_on_questions = db.Column(db.String(150), primary_key=True)
    answers_priority = db.Column(db.String(30), nullable=True)

    students___ = db.relationship('ormStudent')


# db.drop_all()
db.create_all()
# db.session.query(ormStudent).delete()
# db.session.query(ormForm).delete()
# db.session.query(ormDepartament).delete()
# db.session.query(ormAnswer).delete()

# Student1 = ormStudent(student_email='ihor.riasyk@gmail.com', department_number='132', form_name='Development',
#                       answers_on_questions='Data science', student_name='Ihor Riasyk', student_age=20,
#                       student_gender='male', student_location='Kiyv', family_state='unmarried')
# Student2 = ormStudent(student_email='alla.makarenko@gmail.com', department_number='133', form_name='Subjects',
#                       answers_on_questions='KPI', student_name='Alla Makarenko', student_age=19,
#                       student_gender='female', student_location='Other cities', family_state='unmarried')
# Student3 = ormStudent(student_email='serhiy28kpi@gmail.com', department_number='134', form_name='Justice',
#                       answers_on_questions='Not always', student_name='Sergiy Gorodnuk', student_age=21,
#                       student_gender='male', student_location='Kiyv', family_state='married')
# Student4 = ormStudent(student_email='artemenko.yaroslav@gmail.com', department_number='133', form_name='Development',
#                       answers_on_questions='Not always', student_name='Artemenko Yaroslav', student_age=23,
#                       student_gender='male', student_location='Abroad', family_state='unmarried')
# Student5 = ormStudent(student_email='anastasia.grigorenko@gmail.com', department_number='134', form_name='Subjects',
#                       answers_on_questions='Yep', student_name='Anastasia Grigorenko', student_age=20,
#                       student_gender='female', student_location='Kiyv', family_state='married')
# Student6 = ormStudent(student_email='alex.buts@gmail.com', department_number='133', form_name='Justice',
#                       answers_on_questions='Not always', student_name='Alex Buts', student_age=24,
#                       student_gender='male', student_location='Abroad', family_state='unmarried')
# Student7 = ormStudent(student_email='ivan.vovchenko@gmail.com', department_number='132', form_name='Development',
#                       answers_on_questions='Frontend', student_name='Ivan Vovchenko', student_age=21,
#                       student_gender='male', student_location='Other cities', family_state='married')
# Student8 = ormStudent(student_email='ekaterina.buchinska@gmail.com', department_number='134', form_name='Justice',
#                       answers_on_questions='Yep', student_name='Ekaterina Buchinska', student_age=19,
#                       student_gender='female', student_location='Abroad', family_state='married')
# Student9 = ormStudent(student_email='maks.milev@gmail.com', department_number='133', form_name='Development',
#                       answers_on_questions='Data science', student_name='Maks Milev', student_age=22,
#                       student_gender='male', student_location='Kiyv', family_state='married')

# Form1 = ormForm(form_name='Development', questions='What areas of development are you most interested in?')
# Form2 = ormForm(form_name='Subjects', questions='Which institute do you like most?')
# Form3 = ormForm(form_name='Justice', questions='Do you think the attitude towards students at the department is fair?')

# Departament1 = ormDepartament(department_number=132, departament_name='FPM', departament_location='Kiyv')
# Departament2 = ormDepartament(department_number=133, departament_name='IPSA', departament_location='Other cities')
# Departament3 = ormDepartament(department_number=134, departament_name='FIOT', departament_location='Abroad')

# Answer1 = ormAnswer(answers_on_questions='Data science', answers_priority='Highest')
# Answer2 = ormAnswer(answers_on_questions='KPI', answers_priority='Medium')
# Answer3 = ormAnswer(answers_on_questions='Not always', answers_priority='Lowest')
# Answer4 = ormAnswer(answers_on_questions='Yep', answers_priority='Lowest')
# Answer5 = ormAnswer(answers_on_questions='Frontend', answers_priority='Highest')

# Departament1.students_.append(Student1)
# Departament2.students_.append(Student2)
# Departament3.students_.append(Student3)
# Departament3.students_.append(Student4)
# Departament1.students_.append(Student5)
# Departament2.students_.append(Student6)
# Departament1.students_.append(Student7)
# Departament3.students_.append(Student8)
# Departament2.students_.append(Student9)


# Form1.students__.append(Student1)
# Form2.students__.append(Student2)
# Form3.students__.append(Student3)
# Form1.students__.append(Student4)
# Form2.students__.append(Student5)
# Form3.students__.append(Student6)
# Form1.students__.append(Student7)
# Form3.students__.append(Student8)
# Form1.students__.append(Student9)

# Answer1.students___.append(Student1)
# Answer2.students___.append(Student2)
# Answer3.students___.append(Student3)
# Answer3.students___.append(Student4)
# Answer4.students___.append(Student5)
# Answer3.students___.append(Student6)
# Answer5.students___.append(Student7)
# Answer4.students___.append(Student8)
# Answer1.students___.append(Student9)

# db.session.add_all([Student1, Student2, Student3, Student4, Student5, Student6, Student7, Student8, Student9])
# db.session.add_all([Departament1, Departament2, Departament3])
# db.session.add_all([Form1, Form2, Form3])
# db.session.add_all([Answer1, Answer2, Answer3, Answer4, Answer5])

# db.session.commit()


# main page
@app.route('/', methods=['GET', 'POST'])
def root():
    return render_template('index.html')


# students
@app.route('/students', methods=['GET'])
def students():
    result = db.session.query(ormStudent).all()

    return render_template('students.html', students=result)


@app.route('/new_students', methods=['GET', 'POST'])
def new_student():
    form = StudentTableForm()

    if request.method == 'POST':
        if form.validate() == False:
            return render_template('student_form.html', form=form, form_name="New student", action="new_students")
        else:
            new_user = ormStudent(
                student_email=form.student_email.data,
                department_number=form.department_number.data,
                form_name=form.form_name.data,
                answers_on_questions=form.answers_on_questions.data,
                student_name=form.student_name.data,
                student_age=form.student_age.data,
                student_gender=form.student_gender.data,
                student_location=form.student_location.data,
                family_state=form.family_state.data
            )
            try:
                db.session.add(new_user)
                db.session.commit()
                return redirect('/students')
            except:
                form.student_email.errors = ['This name already exists!']
                return render_template('student_form.html', form=form, form_name="New student", action="new_students")

    return render_template('student_form.html', form=form, form_name="New student", action="new_students")


@app.route('/edit_students/<string:x>', methods=['GET', 'POST'])
def edit_student(x):
    form = StudentTableFormUpdate()

    user = db.session.query(ormStudent).filter(ormStudent.student_email == x).one()

    if request.method == 'GET':
        return render_template('student_form_update.html', form=form, form_name="Edit student")

    else:
        if form.validate() == False:
            return render_template('student_form_update.html', form=form, form_name="Edit student")
        else:
            user.student_name = form.student_name.data
            user.student_age = form.student_age.data
            user.student_gender = form.student_gender.data
            user.student_location = form.student_location.data
            user.family_state = form.family_state.data
            db.session.commit()

            return render_template('ok.html')


@app.route('/delete_students/<string:x>', methods=['GET'])
def delete_student(x):
    result = db.session.query(ormStudent).filter(ormStudent.student_email == x).one()

    db.session.delete(result)
    db.session.commit()

    return render_template('ok.html')


# answers page
@app.route('/answers', methods=['GET'])
def answer():
    result = db.session.query(ormAnswer).all()

    return render_template('answers.html', answers=result)


@app.route('/new_answers', methods=['GET', 'POST'])
def new_answer():
    form = AnswersTableForm()

    if request.method == 'POST':
        if form.validate() == False:
            return render_template('answer_form.html', form=form, form_name="New Answers", action="new_answers")
        else:
            new_user = ormAnswer(
                answers_on_questions=form.answers_on_questions.data,
                answers_priority=form.answers_priority.data
            )

            try:
                db.session.add(new_user)
                db.session.commit()
                return redirect('/answers')
            except:
                form.answers_on_questions.errors = ['This name already exists!']
                return render_template('answer_form.html', form=form, form_name="New user", action="new_answers")

    return render_template('answer_form.html', form=form, form_name="New Answers", action="new_answers")


@app.route('/edit_answers/<string:x>', methods=['GET', 'POST'])
def edit_answer(x):
    form = AnswersTableFormUpdate()
    user = db.session.query(ormAnswer).filter(ormAnswer.answers_on_questions == x).one()

    if request.method == 'GET':
        return render_template('answer_form_update.html', form=form, form_name="Edit answers")

    else:
        if form.validate() == False:
            return render_template('answer_form_update.html', form=form, form_name="Edit answers")
        else:
            user.answers_priority = form.answers_priority.data
            db.session.commit()

            return render_template('ok.html')


@app.route('/delete_answer/<string:x>', methods=['GET'])
def delete_answer(x):
    result = db.session.query(ormAnswer).filter(ormAnswer.answers_on_questions == x).one()
    result1 = db.session.query(ormStudent).filter(ormStudent.answers_on_questions == x).all()

    for i in result1:
        db.session.delete(i)

    db.session.delete(result)
    db.session.commit()

    return render_template('ok.html')


# departament page
@app.route('/departament', methods=['GET'])
def departament():
    result = db.session.query(ormDepartament).all()

    return render_template('departaments.html', departaments=result)


@app.route('/new_departament', methods=['GET', 'POST'])
def new_departament():
    form = DepartamentTableForm()

    if request.method == 'POST':
        if form.validate() == False:
            return render_template('departament_form.html', form=form, form_name="New Departament",
                                   action="new_departament")
        else:
            new_user = ormDepartament(
                department_number=form.department_number.data,
                departament_name=form.departament_name.data,
                departament_location=form.departament_location.data
            )
            try:
                db.session.add(new_user)
                db.session.commit()
                return redirect('/departament')
            except:
                form.department_number.errors = ['This name already exists!']
                return render_template('departament_form.html', form=form, form_name="New Departament", action="new_departament")

    return render_template('departament_form.html', form=form, form_name="New Departament", action="new_departament")


@app.route('/edit_departments/<string:x>', methods=['GET', 'POST'])
def edit_department(x):
    form = DepartamentTableFormUpdate()
    user = db.session.query(ormDepartament).filter(ormDepartament.department_number == x).one()

    if request.method == 'GET':
        return render_template('departament_form_update.html', form=form, form_name="Edit departament")

    else:
        if form.validate() == False:
            return render_template('departament_form_update.html', form=form, form_name="Edit departament")
        else:
            user.departament_name = form.departament_name.data
            user.departament_location = form.departament_location.data

            db.session.commit()

            return redirect(url_for('departament'))


@app.route('/delete_departments/<string:x>', methods=['GET'])
def delete_departament(x):
    result = db.session.query(ormDepartament).filter(ormDepartament.department_number == x).one()
    result1 = db.session.query(ormStudent).filter(ormStudent.department_number == x).all()

    for i in result1:
        db.session.delete(i)

    db.session.delete(result)
    db.session.commit()

    return render_template('ok.html')


# form page
@app.route('/forms', methods=['GET'])
def form():
    result = db.session.query(ormForm).all()

    return render_template('forms.html', forms=result)


@app.route('/new_form', methods=['GET', 'POST'])
def new_form():
    form = FormTable()

    if request.method == 'POST':
        if form.validate() == False:
            return render_template('form_form.html', form=form, form_name="New form")

        else:
            new_user = ormForm(
                form_name=form.form_name.data,
                questions=form.questions.data
            )
            try:
                db.session.add(new_user)
                db.session.commit()
                return redirect('/forms')
            except:
                form.form_name.errors = ['This name already exists!']
                return render_template('form_form.html', form=form, form_name="New form")

    return render_template('form_form.html', form=form, form_name="New form")


@app.route('/edit_form/<string:x>', methods=['GET', 'POST'])
def edit_form(x):
    form = FormTableUpdate()
    user = db.session.query(ormForm).filter(ormForm.form_name == x).one()

    if request.method == 'GET':
        return render_template('form_form_update.html', form=form, form_name="Edit form")


    elif request.method == 'POST':

        if form.validate() == False:
            return render_template('form_form_update.html', form=form, form_name="Edit form")
        else:
            user.questions = form.questions.data
            db.session.commit()

            return render_template('ok.html')


@app.route('/delete_form/<string:x>', methods=['GET'])
def delete_form(x):
    result = db.session.query(ormForm).filter(ormForm.form_name == x).one()

    result1 = db.session.query(ormStudent).filter(ormStudent.form_name == x).all()

    for i in result1:
        db.session.delete(i)

    db.session.delete(result)
    db.session.commit()

    return render_template('ok.html')

# neural
@app.route('/NeuralForm', methods=['GET', 'POST'])
def NeuralForm_():
    form = NeuralForm()

    Sample = db.session.query(ormStudent).all()

    X = []
    y = []
    for i in Sample:
        X.append([i.student_age, i.student_gender, i.student_location, i.family_state])
        y.append(i.answers_on_questions)

    Coder1 = ColumnTransformer(transformers=[('code1', OneHotEncoder(), [1, 2, 3])])

    Coder2 = MinMaxScaler(feature_range=(-1, 1))

    Model = MLPClassifier(hidden_layer_sizes=(6, 5))

    Model = Pipeline(steps=[('code1', Coder1), ('code2', Coder2), ('neur', Model)])
    Model.fit(X, y)

    if request.method == 'POST':
        if form.validate() == False:
            return render_template('neuralForm.html', form=form)

        new_user = [
            [form.student_age.data, form.student_gender.data, form.student_location.data, form.family_state.data]]
        y_ = Model.predict(new_user)

        return render_template('neuralFormOk.html', result=y_[0])
    elif request.method == 'GET':
        return render_template('neuralForm.html', form=form)


# dashboard
@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    query1 = (
        db.session.query(
            ormStudent.student_location,
            func.count(ormStudent.student_age).label('age')
        ).
            group_by(ormStudent.student_location)
    ).all()

    query2 = (
        db.session.query(
            ormStudent.student_gender,
            func.count(ormStudent.student_email).label('email')
        ).
            group_by(ormStudent.student_gender)
    ).all()

    query3 = (
        db.session.query(
            ormStudent.student_age,
            func.count(ormStudent.student_email).label('email')
        ).
            group_by(ormStudent.student_age)
    ).all()

    names, skill_counts = zip(*query1)
    bar = go.Bar(
        x=names,
        y=skill_counts
    )

    skills, user_count = zip(*query2)
    pie = go.Pie(
        labels=skills,
        values=user_count
    )

    a,b = zip(*query3)
    scat = go.Scatter(
        x=a,
        y=b,
        mode='markers'
    )

    data = {
        "bar": [bar],
        "pie": [pie],
        "scatter":[scat]
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
