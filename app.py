from flask import Flask, render_template, redirect, url_for, request, session, flash
import db, os
from db import get_db, sqlite3
from flask_bcrypt import Bcrypt, check_password_hash, generate_password_hash


app = Flask(__name__) #Application factory 
bcrypt = Bcrypt(app)
app.config ['DATABASE'] = 'mydatabase.db'


app.secret_key = "2752793d483e1221d36b22674ae4221040a68f7881ce15d29ec1b17d89c10ddd"


db.init_app(app)


@app.route('/')
def home():
    return render_template('/register.html')


#Insert user login into the database and do user authentication
#1. Get access to the database 
#2. Make a post request to insert user data into the database 
#3. Check if username and password exist in database, if not then redirect to register page. 
#4. if no errors then select username and password from database, route to add_task page. 


@app.route('/login', methods=['GET', 'POST'])
def login():
    #making post request
    if request.method == 'POST':
      username = request.form['username']
      password = request.form['password']
      db = get_db()
      user = db.execute('SELECT id, password FROM users WHERE username = ?', (username,)).fetchone()
      print(password)
      print(username)
      if user:
        if check_password_hash(user['password'], password):
            user_dict = dict(user)
            session['user'] = user_dict
            return redirect(url_for('add_task'))
      else:
        flash('Incorrect password')
        print('the check password hash did not run')
    return render_template('/login.html')


#below is link for writing the login page logic with raw sql.
# https://www.youtube.com/watch?v=YpKYBG38FbM

#links for github examples for password hashing (bcrypt) 
#https://github.com/carc1n0gen/tutorial-apps/blob/master/flask-password-hashing-bcrypt/app.py

#bcrypt documentation link
#https://flask-bcrypt.readthedocs.io/en/1.0.1/


    #  create sign up route code logic for entering a new username and password into the database.
    # username - "Bob" password - "123"
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
            db = get_db()
            print('connection to database made')
            username = request.form['username']
            password = request.form['password']
            print('form data -username, password captured')
            if username and password:
                #check that this username is not taken
                db.execute('SELECT id FROM users WHERE username = ?',
                (username,)).fetchone()
                db.commit()
                print('data selected from database')
                pw_hash = generate_password_hash(password, 10).decode('utf-8')
                 # hash password when inserting new user
                db.execute('INSERT into users (username, password) VALUES (?, ?)',
                (username, pw_hash))
                db.commit()
                print('username and password inserted in db. Password hashed')
                print('User registered successfully.') 
                return redirect(url_for('login')) 
            print('db.execute (inserting username and hashed password) did not function')
            flash('Username is taken.')        
    return render_template ('/register.html')    



@app.route("/add_task", methods=['GET', 'POST'])
def add_task():
    if 'user' in session: # checking if user is in session
        user_id = session['user']['id'] # getting logged-in user's id
        db = get_db()

        if request.method == 'POST':
            task = request.form['task']
            time_minutes = request.form['time_minutes']

            db.execute(
                'INSERT INTO tasks (task, time_minutes, user_id) VALUES (?, ?, ?)',
                (task, time_minutes, user_id)
            )
            db.commit()

        tasks = db.execute('SELECT id, task, time_minutes FROM tasks WHERE user_id = ?',
                           (user_id,)).fetchall()


        #Calculate sum of time_minutes 
        time_sum = sum(task['time_minutes'] for task in tasks)



        return render_template('add_task.html', tasks=tasks, time_sum=time_sum)

    else:
        return render_template('login')


@app.route("/delete_task/<int:task_id>", methods=['POST'])
def delete_task(task_id):
    print(f"Attempting to delete task with ID: {task_id}")
    db = get_db()
    try:
        db.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
        db.commit()
        print(f"Task ID {task_id} deleted successfully")
    except Exception as e:
        print(f"Error deleting task {e}")
        db.rollback()
    return redirect(url_for('add_task'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect("/")




if __name__ == '__main__':
    app.run(debug=True) 
