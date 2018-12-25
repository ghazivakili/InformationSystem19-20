from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,PasswordField,ValidationError,FileField
from wtforms.validators import Length,Email,EqualTo,DataRequired,regexp
from app import Student,Role

class Formname(FlaskForm):
    name = StringField('Name:', validators=[DataRequired(), Length(min=2, max=20)])
    student_no = StringField('Student No.:', validators=[DataRequired(), Length(min=2, max=10)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password_con = PasswordField('Confirm', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Submit')

    def validate_student_no(self,student_no):
        st = Student.query.filter_by(student_no=student_no.data).first()
        if st:
            raise ValidationError('You have been registerd or ...')

    def validate_email(self,email):
        st = Student.query.filter_by(email=email.data).first()
        if st:
            raise ValidationError('You have been registerd with email or ...')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email(),Length(min=4,max=50)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Submit')




class UploadForm(FlaskForm):
    file = FileField('file',validators=[DataRequired()])
    upload=SubmitField('upload')