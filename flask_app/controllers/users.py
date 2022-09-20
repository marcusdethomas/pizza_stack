from flask_app import app
from flask import render_template, redirect, request, flash, session
from flask_app.controllers.pizza import pizzas
from flask_app.models.pizza import Pizza
from flask_app.models.user import User
from flask_app.models.topping import Topping
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register',methods=['POST'])
def register():
    if not User.verify_login(request.form):
        return redirect('/')
    if not User.check_duplicate(request.form):
        return redirect('/')
    data ={ 
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": bcrypt.generate_password_hash(request.form['password']),
        "role": [request.form['role']]
    }
    print("Data Role:", data)
    id = User.create_login(data) 
    session['user_id'] = id
    session['user_role'] = request.form['role']
    return redirect('/dashboard')
    
@app.route('/login', methods=['POST'])
def login():
    user = User.get_by_email(request.form)
    if not user:
        flash("Invalid Email","login")
        return redirect('/')
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash("Invalid Password","login")
        return redirect('/')
    session['user_id'] = user.id
    session['user_role'] = user.role
    return redirect('/dashboard')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'id': session['user_id']
    }
    role ={
        'role': session['user_role']
    }
    user = User.get_by_id(data)
    session['user_role'] = user.role
    return render_template('/dashboard.html', user = User.get_by_id(data),  pizzas = Pizza.get_all())

@app.route('/new')
def new_show():
    return redirect('/')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')
