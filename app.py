import os
from flask import Flask ,render_template , url_for,flash,redirect
from flask import request,session
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_mail import Mail, Message
from flask_uploads import UploadSet, configure_uploads, IMAGES, patch_request_class





app = Flask(__name__)
app.config['SECRET_KEY'] = 'sdfghjkllkjhgfdfghjkkjhgfddfgytrk'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///website.db'
app.config['UPLOADED_PHOTOS_DEST'] = os.getcwd()+"/photos"
app.config['MAIL_SERVER']='smtp.mail.com'
app.config['MAIL_PORT']=587
app.config['MAIL_TLS']=True
app.config['MAIL_USERNAME']=os.environ['EMAIL_USERNAME']
app.config['MAIL_PASSWORD']=os.environ['EMAIL_PASSWORD']


db=SQLAlchemy(app)
bcrypt=Bcrypt(app)
mailobject=Mail(app)

photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)
patch_request_class(app)  # set maximum file size, default is 16MB



class Student(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    student_no=db.Column(db.String(20),unique=True,nullable=True)
    email=db.Column(db.String(50),unique=True,nullable=True)
    name=db.Column(db.String(100),nullable=True)
    password=db.Column(db.String(100),nullable=True)
    role_id=db.Column(db.Integer,db.ForeignKey('role.id'))

    def __repr__(self):
        return "<Student %r>" % self.name


class Role(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(10),nullable=True)
    students=db.relationship('Student',backref='role',lazy=True)

    def __repr__(self):
        return "<Role %r>" % self.name


from forms import Formname,LoginForm,UploadForm



#dictionary
posts = [
    {
        'author': 'Mohammad Ghz',
        'title': 'Flask is 1',
        'content': 'First content',
        'date_posted': 'Nov. 11, 2018'
    },
    {
        'author': 'Lia morra',
        'title': 'Exam 2',
        'content': 'Second content',
        'date_posted': 'Nov. 2, 2018'
    },
    {
        'author': 'Student 1',
        'title': 'Post 3',
        'content': 'Third content',
        'date_posted': 'Oct. 20, 2018'
    }
]

def send_mail(to,subject,template,**kwargs):
    msg=Message(subject,recipients=[to],sender=app.config['MAIL_USERNAME'])
    msg.body= render_template(template + '.txt',**kwargs)
    msg.html= render_template(template + '.html',**kwargs)
    mailobject.send(msg)



@app.route('/mail')
def mail():
    send_mail('m.ghazivakili@gmail.com','Test message','mail',message_body='Hi this is a test')
    return 'message has beed send!'

@app.route('/')
@app.route('/home')
def home():
    return render_template('index.html', posts=posts)


@app.route("/about")
def about():
    return render_template('about.html', title='About')

@app.route("/register",methods=['POST','GET'])
def register():
    formpage=Formname()
    if formpage.validate_on_submit():
        password_1=bcrypt.generate_password_hash(formpage.password.data).encode('utf-8')
        reg=Student(name=formpage.name.data,
                email=formpage.email.data,
                student_no=formpage.student_no.data,
                password=password_1,
                role_id=1) #role=Role.query.filter_by(name='Student'))
        db.session.add(reg)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('register.html', formpage = formpage , title='Register Page')


@app.route("/login",methods=['POST','GET'])
def login():
    formpage=LoginForm()
    if formpage.validate_on_submit():
        # TODO do query db for login or use login from flask
        st=Student.query.filter_by(email=formpage.email.data).first()
        if st and bcrypt.check_password_hash(st.password,formpage.password.data):
            session['email']=st.name
    return render_template('login.html', formpage = formpage,
                           email=session.get('email',False) ,
                           title='Login Page')


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))


@app.before_first_request
def setup_all():
    db.create_all()

@app.route("/fillrole")
def filldata():
    db.session.add(Role(name="Student"))
    db.session.commit()


@app.route("/profile")
def profiles():
    st=Student.query.filter_by(email="ghazivakili55@gmail.com").all()
    return render_template("profile.html",students=st)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(e):
    return render_template('500.html'), 500



@app.route("/upload",methods=["POST","GET"])
def upload():
    formupload=UploadForm()
    if formupload.validate_on_submit():
        filename = photos.save(formupload.file.data)
        file_url = photos.url(filename)
        return redirect(file_url)
    return render_template("upload.html",formupload=formupload)

#
#
# def send_mail(to, subject, template, **kwargs):
#     msg=Message(subject,
#                 sender=app.config['MAIL_USERNAME'],
#                 recipients=[to])
#     # msg.body=render_template(template+'.txt',**kwargs)
#     msg.html=render_template(template+'.html',**kwargs)
#     mail.send(msg)
#
#
#
# @app.route("/mail")
# def testmail():
#
#     send_mail('m.ghazivakili@gmail.com',
#               'Hi I am test mail'
#               ,'mail',user='mohammad')
#
#     return 'mail has been send'

if __name__ == '__main__':
    app.run(debug=True)
