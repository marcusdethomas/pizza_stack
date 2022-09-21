from flask_app import app
from flask import render_template, redirect, request, flash, session
from flask_app.models.pizza import Pizza 
from flask_app.models.user import User
from flask_app.models.topping import Topping

    #user_role = User.get_by_id(data)
    #print(user_role.role)
@app.route('/add')
def add_topping():
    role ={
        'role': session['user_role']
    }
    if not User.is_admin(session['user_role']):
        return redirect('/dashboard')
    print(session['user_role'])
    #User.is_admin_check(role)
    return render_template('/new_topping.html')

@app.route('/new', methods = ['POST'])
def add_new(): 
    if 'user_id' not in session:
        return redirect ('/logout')
    if not Topping.validate_entry(request.form):
        return redirect('/add')
    if not Topping.check_duplicate(request.form):
        return redirect('/add')
    data = {
    "topping_name": request.form["topping_name"],
    "user_id": session['user_id']
    }   
    Topping.save(data)
    return redirect('/show_all')

@app.route('/topping/<int:id>')
def show_topping(id):
    if 'user_id' not in session:
        redirect ('/logout')
    data = {
        'id': id
    }
    owner = Topping.get_by_id(data)
    user_id = owner.user_id
    owner_data ={
        'id' : user_id
    }
    return render_template('/show_toppings.html', topping = Topping.get_by_id(data),owner = User.get_by_id(owner_data))

@app.route('/topping/edit/<int:id>')
def edit_topping(id):
    if 'user_id' not in session:
        redirect ('/logout')
    data = {
        'id':id,
    }
    user_data = {
        "id":session['user_id']
    }
    return render_template('edit_topping.html', toppings = Topping.get_by_id(data), user = User.get_by_id(user_data))

@app.route('/topping/update', methods =['POST'])
def update_topping():
    if 'user_id' not in session:
        return redirect ('/logout')
    if not Topping.validate_entry(request.form):
        edit = {
            "id": request.form['id'],
            "topping_name":request.form['topping_name']
        }
        print("Temp: ", edit)
        return redirect("/topping/edit/<int:id>")
    if not Topping.check_duplicate(request.form):
        return redirect('/add')
    data = {
    "topping_name": request.form["topping_name"],
    "id": request.form['id']
    }
    print("Edit topping data: ", data)
    Topping.update(data)
    return redirect('/show_all')


@app.route('/show_all')
def show_all():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'id': session['user_id'],
    }
    toppings = Topping.get_all()
    print(toppings)
    return render_template('/all_toppings.html', user = User.get_by_id(data), topping = Topping.get_all())


@app.route('/delete_topping/<int:id>')
def delete_topping(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    if not Topping.check_if_deletable(data):
        return redirect ('/show_all')
    Topping.destroy(data)
    return redirect('/show_all')
