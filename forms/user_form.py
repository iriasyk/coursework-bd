from flask_wtf import Form
from wtforms import StringField, SubmitField, IntegerField, ValidationError
from wtforms import validators
import re


# def validLocation(form, field):
#     if field.data not in ['Kiyv', 'Other cities', 'Abroad']:
#         raise ValidationError("Choose one of the three: Kiyv or Other cities or Abroad!")
#
#
# def validFormName(form, field):
#     if field.data not in ['Development', 'Subjects', 'Justice']:
#         raise ValidationError("Choose one of the three: Development or Subjects or Justice!")
#
#
# def validGender(form, field):
#     if field.data not in ['male', 'female']:
#         raise ValidationError("Choose one of the two: male or female!")
#
#
# def validFamilyState(form, field):
#     if field.data not in ['married', 'unmarried']:
#         raise ValidationError("Choose one of the two: married or unmarried!")
#
#
def validGradeAtTheDepartament(form, field):
    if 0 >= int(field.data) >= 100:
        raise ValidationError('Number should be from 1 to 100 symbols!')


def validStr(form, field):
    for i in field.data:
        if i.lower() not in list('qwertyuioplkjhgfdsazxcvbnm '):
            raise ValidationError('Enter a not number and symbol or not english!')


def validQuestion(form, field):
    if field.data[len(field.data) - 1] != '?':
        raise ValidationError('Enter as a last item a question mark is expected! Add "?" character to the end.')
    for i in range(len(field.data) - 1):
        if field.data[i].lower() not in list('qwertyuioplkjhgfdsazxcvbnm,.: '):
            raise ValidationError('Enter a not number and symbol!')


class StudentTableForm(Form):
    email = StringField("email: ", [  # primary key in table Student
        validators.Email("Please enter email!"),
    ])

    name_student = StringField("student name: ", [
        validators.DataRequired("Please enter name!"),
        validators.Length(1, 30, "Name should be from 1 to 30 symbols"),
        validStr
    ])

    status_at_the_departament = StringField("status at the departament: ", [
        validators.DataRequired("Please status at the departament!"),
        validators.Length(1, 20, "Status should be from 1 to 20 symbols"),
        validStr
    ])

    grade_at_the_departament = IntegerField("grade at the departament: ", [
        validators.DataRequired("Please enter grade at the departament!"),
        validGradeAtTheDepartament
    ])

    expected_grade_point = IntegerField("expected grade point: ", [
        validators.DataRequired("Please enter expected grade point!"),
        validGradeAtTheDepartament
    ])

    mood = StringField("mood: ", [
        validators.DataRequired("Please enter u mood!"),
        validators.Length(1, 20, "Name should be from 1 to 20 symbols"),
        validStr
    ])

    subject = StringField("subject: ", [ # primary key
        validators.DataRequired("Please enter subject!"),
        validators.Length(1, 80, "Name should be from 1 to 80 symbols"),
        validStr
    ])

    answer = StringField("answer: ", [ # primary key
        validators.DataRequired("Please enter answer!"),
        validators.Length(1, 20, "Name should be from 1 to 20 symbols")
    ])

    submit = SubmitField("Save")


class StudentTableFormUpdate(Form):
    name_student = StringField("student name: ", [
        validators.DataRequired("Please enter name!"),
        validators.Length(1, 30, "Name should be from 1 to 30 symbols"),
        validStr
    ])

    status_at_the_departament = StringField("status at the departament: ", [
        validators.DataRequired("Please status at the departament!"),
        validators.Length(1, 20, "Status should be from 1 to 20 symbols"),
        validStr
    ])

    grade_at_the_departament = IntegerField("grade at the departament: ", [
        validators.DataRequired("Please enter grade at the departament!"),
        validGradeAtTheDepartament
    ])

    expected_grade_point = IntegerField("expected grade point: ", [
        validators.DataRequired("Please enter expected grade point!"),
        validGradeAtTheDepartament
    ])

    mood = StringField("mood: ", [
        validators.DataRequired("Please enter u mood!"),
        validators.Length(1, 20, "Name should be from 1 to 20 symbols"),
        validStr
    ])

    submit = SubmitField("Save")


class QuestionTable(Form):
    subject_matter = StringField("subject matter: ", [  # primary key in table Question
        validators.DataRequired("Please enter form name!"),
        validators.Length(1, 20, "Name should be from 1 to 20 symbols"),
        validStr
    ])

    question = StringField("question: ", [
        validators.DataRequired("Please enter question!"),
        validQuestion
    ])

    submit = SubmitField("Save")


class QuestionTableUpdate(Form):
    question = StringField("question: ", [
        validators.DataRequired("Please enter question!"),
        validQuestion
    ])

    submit = SubmitField("Save")


class SubjectTableForm(Form):
    subject = StringField("subject: ", [ # primary key
        validators.DataRequired("Please enter subject!"),
        validators.Length(1, 80, "Name should be from 1 to 80 symbols"),
        validStr
    ])

    submit = SubmitField("Save")


class AnswerTableForm(Form):
    answer = StringField("answer: ", [ # primary key
        validators.DataRequired("Please enter answer!"),
        validators.Length(1, 20, "Name should be from 1 to 20 symbols")
    ])

    submit = SubmitField("Save")