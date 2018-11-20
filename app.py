from flask import Flask ,render_template , url_for,flash,redirect
from flask import request,session
from forms import Formname,LoginForm




app = Flask(__name__)
app.config['SECRET_KEY'] = 'sdfghjkllkjhgfdfghjkkjhgfddfgytrk'


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
        return redirect(url_for('home'))
    return render_template('register.html', formpage = formpage , title='Register Page')


@app.route("/login",methods=['POST','GET'])
def login():
    formpage=LoginForm()
    if formpage.validate_on_submit():
        # TODO do query db for login or use login from flask
        session['email']=formpage.email.data
    return render_template('login.html', formpage = formpage, email=session.get('email',False) , title='Login Page')


@app.route('/bro')
def bro():
    user_agent = request.headers.get('User-Agent')
    return '<p>Your browser is %s</p>' % user_agent

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(e):
    return render_template('500.html'), 500


if __name__ == '__main__':
    app.run(debug=True)
