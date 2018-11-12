from flask import Flask ,render_template , url_for
from flask import request
app = Flask(__name__)
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
