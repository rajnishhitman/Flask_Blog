from flask import Flask, render_template, url_for, flash, redirect
from forms import RegistrationForm, LoginForm

app = Flask(__name__)

app.config['SECRET_KEY'] = '5ac18d133c5aac78b1e3a2a9dae17c05'

posts = [
    {
        'author':'Yaman',
        'title':'Stickers',
        'content':'Give me all your stickers!, stickers here, stickers there, stickers EVERYWHERE!',
        'date_posted':'22 July, 2020'
    },
    {
        'author':'Hamsho',
        'title':"TMNT Expert",
        'content':"Why hasn't anyone watched the show??",
        'date_posted':'19 July, 2020'
    },
    {
        'author':'Rami',
        'title':'Variables',
        'content':'VARIABLES!, keep them organised for gods sake.',
        'date_posted':'19 July, 2020'
    },
    {
        'author':'Hasan',
        'title':'Front End',
        'content':'Seriously though, am I the only one working front end in here?',
        'date_posted':'30 June, 2020'
    },
    {
        'author':'Maias',
        'title':'Bot testing',
        'content':'Destroy every bot in sight!, murder them all!',
        'date_posted':'15 June, 2020'
    }
]


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html',posts=posts)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/register', methods=['POST','GET'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)


@app.route('/login', methods=['POST','GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'TMNT@blog.com' and form.password.data == 'password':
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)




if __name__ == '__main__':
    app.run(debug=True)
