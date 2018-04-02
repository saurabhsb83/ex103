# controller

from flask import Flask , render_template , request , session , flash , redirect , url_for , g
import sqlite3
from functools import wraps

#configuration
DATABASE = 'blog.db'
USERNAME = 'admin'
PASSWORD = 'admin'
SECRET_KEY = 'hard_to_guess'

app = Flask(__name__)
app.config.from_object(__name__)

# def connect_db():
#    sqlite3.connect(app.config['DATABASE'])


def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return test(*args, **kwargs)
        else:
            flash('You need to login first')
            return redirect(url_for('login'))
    return wrap


@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    status_code = 200
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME'] or request.form['password'] != app.config['PASSWORD']:
            error = 'invalid credentials'
            status_code = 401
        else:
            session['logged_in'] = True
            return redirect(url_for('main'))
    return render_template('login.html', error=error), status_code


@app.route('/main')
@login_required
def main():
    # g.db = connect_db()
    # cur = g.db.execute('select * from posts')
    # g.db.close()
    with sqlite3.connect('blog.db') as connection:
        c = connection.cursor()
        print('test')
        c.execute('select * from posts')
        '''posts = c.fetchall()
        for r in posts:
            print('hello' + r.__str__())'''
        posts = [dict(title=row[0], post=row[1]) for row in c.fetchall()]

    return render_template('main.html', posts=posts)


@app.route('/add', methods=['POST'])
@login_required
def add():
    title = request.form['title']
    msg  = request.form['msg']
    print('title is: ' +title)
    print('msg is: ' + msg)
    if title == '' or msg == '':
        flash('all fields are mandatory')
        return redirect(url_for('main'))
    else:
        with sqlite3.connect('blog.db') as connection:
            c = connection.cursor()
            c.execute('insert into posts values(?, ?)', [request.form['title'], request.form['msg']])
            connection.commit()
            flash('the post has been posted')
            return redirect(url_for('main'))


@app.route('/logout')
def logout():
    session.pop('logged in', None)
    flash('you were logged out')
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)

