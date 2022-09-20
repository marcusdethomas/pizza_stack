from flask_app import app
from flask import render_template, redirect, request, flash, session
from flask_app.models.pizza import Pizza 
from flask_app.models.user import User
from flask_app.models.topping import Topping

@app.route('/add')
def add_topping():
    return render_template('/new_topping.html')

@app.route('/new', methods = ['POST'])
def add_new(): 
    if 'user_id' not in session:
        return redirect ('/logout')
    if not Topping.validate_entry(request.form):
        return redirect('/add')
    data = {
    "topping_name": request.form["topping_name"],
    "user_id": session['user_id']
    }
    Topping.save(data)
    return redirect('/dashboard')

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
    # role = request.form['role']  will not work because this is not a post route
    return render_template('/all_toppings.html', user = User.get_by_id(data), topping = Topping.get_all())


@app.route('/delete_topping/<int:id>')
def delete_topping(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    Topping.destroy(data)
    return redirect('/dashboard')
