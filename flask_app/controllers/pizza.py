from xml.etree.ElementTree import PI
from flask_app import app
from flask import render_template, redirect, request, flash, session
from flask_app.models.pizza import Pizza 
from flask_app.models.user import User
from flask_app.models.topping import Topping

@app.route('/pizza')
def add_pizza():
    return render_template('/new_pizza.html')

@app.route('/new_pizza', methods = ['POST'])
def add_new_pizza(): 
    if 'user_id' not in session:
        return redirect ('/logout')
    if not Pizza.validate_entry(request.form):
        return redirect('/add')
    data = {
    "pizza_name": request.form["pizza_name"],
    "user_id": session['user_id']
    }
    Pizza.save(data)
    return redirect('/dashboard')

@app.route('/pizza/<int:id>')
def pizzas(id):
    if 'user_id' not in session:
        redirect ('/logout')
    data = {
        'id': id
    }
    owner = Pizza.get_by_id(data)
    user_id = owner.user_id
    owner_data ={
        'id' : user_id
    }
    return render_template('/show_pizzas.html', pizza = Pizza.get_by_id(data),owner = User.get_by_id(owner_data), pizzas = Pizza.get_pizza_toppings(data))

@app.route('/delete/<int:id>')
def delete_pizza(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    Pizza.destroy(data)
    return redirect('/dashboard')
