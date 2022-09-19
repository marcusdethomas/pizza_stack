from flask_app import app
from flask import render_template, redirect, request, flash, session
from flask_app.models.pizza import Pizza
from flask_app.models.topping import Topping 
from flask_app.models.user import User
from flask_app.models.pizza_has_topping import Pizza_has_toppings

@app.route('/pizza')
def add_pizza():
    return render_template('/new_pizza.html', toppings = Topping.get_all(), has_topping=Pizza_has_toppings.get_full_pie())

@app.route('/new_pizza', methods = ['POST'])
def add_new_pizza(): 
    if 'user_id' not in session:
        return redirect ('/logout')
    if not Pizza.validate_entry(request.form):
        return redirect('/pizza')
    data = {
    "pizza_name": request.form["pizza_name"],
    "user_id": session['user_id']
    }
    Pizza.save(data)
    new_pizza = Pizza.get_by_name(data)
    pizza_id = new_pizza.id
    topping_list = request.form.getlist("topping_id")
    all_data = {
    "pizza_id": pizza_id,
    "topping_id": topping_list
    }
    Pizza_has_toppings.save(all_data, pizza_id, topping_list) 
    print("Pizza has topping: " , all_data) # testing third table save
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
    Pizza_has_toppings.destroy(data)
    Pizza.destroy(data)
    return redirect('/dashboard')
