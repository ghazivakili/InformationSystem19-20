import os
from flask import Flask ,render_template , url_for,flash,redirect
from flask import request,session
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_mail import Mail, Message
from flask_uploads import UploadSet, configure_uploads, IMAGES, patch_request_class
from flask_login import LoginManager,login_user,logout_user





app = Flask(__name__)
app.config['SECRET_KEY'] = 'sdfghjkllkjhgfdfghjkkjhgfddfgytrk'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///website.db'
app.config['UPLOADED_PHOTOS_DEST'] = os.getcwd()+"/static"
app.config['MAIL_SERVER']='smtp.mail.com'
app.config['MAIL_PORT']=587
app.config['MAIL_TLS']=True
app.config['MAIL_USERNAME']=os.environ['EMAIL_USERNAME']
app.config['MAIL_PASSWORD']=os.environ['EMAIL_PASSWORD']


db=SQLAlchemy(app)
bcrypt=Bcrypt(app)
mailobject=Mail(app)
login_manager=LoginManager()
login_manager.init_app(app)

photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)
patch_request_class(app)  # set maximum file size, default is 16MB

print IMAGES
print 'this is file path %s' % app.config['UPLOADED_PHOTOS_DEST']

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


# def send_mail(to, subject, template, **kwargs):
#     msg=Message(subject,
#                 sender=app.config['MAIL_USERNAME'],
#                 recipients=[to])
#     # msg.body=render_template(template+'.txt',**kwargs)
#     msg.html=render_template(template+'.html',**kwargs)
#     mailobject.send(msg)




def send_mail(to,subject,template,**kwargs):
    msg=Message(subject,recipients=[to],sender=app.config['MAIL_USERNAME'])
    msg.body= render_template(template + '.txt',**kwargs)
    msg.html= render_template(template + '.html',**kwargs)
    mailobject.send(msg)


class mailClass():

    template = "mail.html"
    sender = app.config['MAIL_USERNAME']
    subject = "Test"
    toList = ["m.ghazivakili@gmail.com"]
    def send(self,**kwargs):
        msg=Message(subject=self.subject,recipients=self.toList,sender=self.sender)
        msg.html=render_template(self.template,**kwargs)
        mailobject.send(msg)


def sendmail(**kwargs):

    # send_mail('m.ghazivakili@gmail.com',
    #           'Hi I am test mail'
    #           ,'mail',user='mohammad')
    mailc=mailClass()
    mailc.toList=[kwargs['email']]
    mailc.send(user=kwargs['user'])
    print "mail has been send"
    return True


# @app.route('/mail')
# def mail():
#     send_mail('m.ghazivakili@gmail.com','Test message','mail',message_body='Hi this is a test')
#     return 'message has beed send!'
@app.route('/mail')
def testmail():

    # send_mail('m.ghazivakili@gmail.com',
    #           'Hi I am test mail'
    #           ,'mail',user='mohammad')
    mailc=mailClass()
    mailc.toList=[session.get('email')]
    mailc.send(user=session.get('name'))
    print "mail has been send"
    return render_template('index.html', posts=posts)





@app.route("/upload",methods=["POST","GET"])
def upload():
    if session.get('id'):
        if not os.path.exists('static/'+ str(session.get('id'))):
            os.makedirs('static/'+ str(session.get('id')))
        file_url = os.listdir('static/'+ str(session.get('id')))
        file_url = [ str(session.get('id')) +"/"+ file for file in file_url]
        formupload = UploadForm()
        print session.get('email')
        if formupload.validate_on_submit():
            filename = photos.save(formupload.file.data,name=str(session.get('id'))+'.jpg',folder=str(session.get('id')))
            file_url.append(filename)
        return render_template("upload.html",formupload=formupload,filelist=file_url) # ,filelist=file_url
    else:
        return redirect('login')










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
        role_1=Role.query.filter_by(name=formpage.usertype.data).first()
        password_1=bcrypt.generate_password_hash(formpage.password.data).encode('utf-8')
        reg=Student(name=formpage.name.data,
                email=formpage.email.data,
                student_no=formpage.student_no.data,
                password=password_1,
                role=role_1) #role=Role.query.filter_by(name='Student'))
        db.session.add(reg)
        db.session.commit()
        sendmail(email=formpage.email.data,user=formpage.name.data)
        return redirect(url_for('home'))
    return render_template('register.html', formpage = formpage , title='Register Page')


@app.route("/login",methods=['POST','GET'])
def login():
    formpage=LoginForm()
    if formpage.validate_on_submit():
        # TODO do query db for login or use login from flask
        st=Student.query.filter_by(email=formpage.email.data).first()
        if st and bcrypt.check_password_hash(st.password,formpage.password.data):
            session['email']=st.email
            session['name']=st.name
            session['id']=st.id
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
    if session.get('id'):
        st=Student.query.filter_by().all()
        return render_template("profile.html",students=st)
    else:
        return redirect('login')

@app.route("/map")
def map():
    return render_template("map.html")


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(e):
    return render_template('500.html'), 500







if __name__ == '__main__':
    app.run(debug=True)
