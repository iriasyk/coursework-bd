from flask_wtf import Form
from wtforms import StringField, SubmitField, PasswordField, DateField, HiddenField, IntegerField, ValidationError
from wtforms import validators
import re


def validLocation(form, field):
    if field.data not in ['Kiyv', 'Other cities', 'Abroad']:
        raise ValidationError("Choose one of the three: Kiyv or Other cities or Abroad!")


def validFormName(form, field):
    if field.data not in ['Development', 'Subjects', 'Justice']:
        raise ValidationError("Choose one of the three: Development or Subjects or Justice!")


def validGender(form, field):
    if field.data not in ['male', 'female']:
        raise ValidationError("Choose one of the two: male or female!")


def validFamilyState(form, field):
    if field.data not in ['married', 'unmarried']:
        raise ValidationError("Choose one of the two: married or unmarried!")


def validAge(form, field):
    if int(field.data) <= 18:
        raise ValidationError('Enter a number greater than 18')


def validStr(form, field):
    for i in field.data:
        if i.lower() not in list('qwertyuioplkjhgfdsazxcvbnm'):
            raise ValidationError('Enter a not number and symbol!')


def validQuestion(form, field):
    if field.data[len(field.data) - 1] != '?':
        raise ValidationError('Enter as a last item a question mark is expected! Add "?" character to the end.')
    for i in range(len(field.data)-1):
        if field.data[i].lower() not in list('qwertyuioplkjhgfdsazxcvbnm,.:'):
            raise ValidationError('Enter a not number and symbol!')


class StudentTableForm(Form):
    student_email = StringField("email: ", [  # primary key in table Student
        validators.Email("Please enter email!"),
    ])

    department_number = IntegerField("department number: ", [  # primary key for table Departament
        validators.DataRequired("Please enter department number!")
    ])

    form_name = StringField("form name: ", [  # primary key for table Form
        validators.DataRequired("Please enter form name!"),
        validFormName
    ])

    answers_on_questions = StringField("Content answers on questions: ", [  # primary key in table Answers
        validators.DataRequired("Please enter array answers on questions!")
    ])

    student_name = StringField("student name: ", [
        validators.DataRequired("Please enter name!"),
        validators.Length(1, 20, "Name should be from 1 to 20 symbols"),
        validStr
    ])

    student_age = IntegerField("student age: ", [
        validators.DataRequired("Please enter age!"),
        validAge
    ])

    student_gender = StringField("student gender: ", [
        validators.DataRequired("Please enter gender!"),
        validGender
    ])

    student_location = StringField("student location: ", [
        validators.DataRequired("Please enter student location!"),
        validLocation,
        # validators.Length(1, 15, "Name should be from 1 to 15 symbols")
    ])

    family_state = StringField("family state: ", [
        validators.DataRequired("Please enter family state!"),
        validFamilyState
    ])

    submit = SubmitField("Save")


class StudentTableFormUpdate(Form):
    student_name = StringField("student name: ", [
        validators.DataRequired("Please enter name!"),
        validators.Length(1, 20, "Name should be from 1 to 20 symbols"),
        validStr
    ])

    student_age = IntegerField("student age: ", [
        validators.DataRequired("Please enter age!"),
        validAge
    ])

    student_gender = StringField("student gender: ", [
        validators.DataRequired("Please enter gender!"),
        validGender
    ])

    student_location = StringField("student location: ", [
        validators.DataRequired("Please enter student location!"),
        validLocation
        # validators.Length(1, 15, "Name should be from 1 to 15 symbols")
    ])

    family_state = StringField("family state: ", [
        validators.DataRequired("Please enter family state!"),
        validFamilyState
    ])

    submit = SubmitField("Save")


class FormTable(Form):
    form_name = StringField("form name: ", [  # primary key in table Form
        validators.DataRequired("Please enter form name!"),
        validators.Length(1, 30, "Name should be from 1 to 30 symbols")
    ])

    questions = StringField("content of the question: ", [
        validators.DataRequired("Please enter content of the array questions!"),
        validQuestion
    ])

    submit = SubmitField("Save")


class FormTableUpdate(Form):
    questions = StringField("content of the question: ", [
        validators.DataRequired("Please enter content of the array questions!"),
        validQuestion
    ])

    submit = SubmitField("Save")


class DepartamentTableForm(Form):
    department_number = IntegerField("department number: ", [  # primary key in table Departament
        validators.DataRequired("Please enter department number.")
    ])

    departament_name = StringField("Departament of the institute name: ", [
        validators.DataRequired("Please enter departament of the institute name!"),
        validators.Length(1, 30, "Name should be from 1 to 30 symbols"),
        validStr
    ])

    departament_location = StringField("Department of the institute location: ", [
        validators.DataRequired("Please enter department of the institute location!"),
        validLocation
        # validators.Length(1, 15, "Name should be from 1 to 15 symbols")
    ])

    submit = SubmitField("Save")


class DepartamentTableFormUpdate(Form):
    departament_name = StringField("Departament of the institute name: ", [
        validators.DataRequired("Please enter departament of the institute name!"),
        validators.Length(1, 30, "Name should be from 1 to 30 symbols"),
        validStr
    ])

    departament_location = StringField("Department of the institute location: ", [
        validators.DataRequired("Please enter department of the institute location!"),
        validLocation
        # validators.Length(1, 15, "Name should be from 1 to 15 symbols")
    ])

    submit = SubmitField("Save")


class AnswersTableForm(Form):
    answers_on_questions = StringField("Content answers on questions: ", [  # primary key
        validators.DataRequired("Please enter array answers on questions!")
    ])

    answers_priority = StringField("Content answer priority: ", [
        validators.Length(1, 30, "Name should be from 1 to 30 symbols"),
        validators.DataRequired("Please enter priority for answer!")
    ])

    submit = SubmitField("Save")


class AnswersTableFormUpdate(Form):
    answers_priority = StringField("Content answer priority: ", [
        validators.Length(1, 30, "Name should be from 1 to 30 symbols"),
        validators.DataRequired("Please enter priority for answer!")
    ])

    submit = SubmitField("Save")


class NeuralForm(Form):
    department_number = IntegerField("department number: ", [  # primary key in table Departament
        validators.DataRequired("Please enter department number.")
    ])

    form_name = StringField("form name: ", [  # primary key in table Form
        validators.DataRequired("Please enter form name!"),
        validFormName
    ])

    student_age = IntegerField("student age: ", [
        validators.DataRequired("Please enter age!"),
        validAge
    ])

    student_gender = StringField("student gender: ", [
        validators.DataRequired("Please enter gender!"),
        validGender
    ])

    student_location = StringField("student location: ", [
        validators.DataRequired("Please enter student location!"),
        validLocation
    ])

    family_state = StringField("family state: ", [
        validators.DataRequired("Please enter family state!"),
        validFamilyState
    ])

    submit = SubmitField("Save")
