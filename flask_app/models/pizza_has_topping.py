from flask_app.config.mysqlconnection import MySQLConnection, connectToMySQL
from flask_app.controllers import users
from pickle import TRUE, FALSE
from flask import flash, session
from flask_app.models.user import User
from flask_app.models.pizza import Pizza

class Pizza_has_toppings:
    my_db = 'pizza_stack'
    def __init__(self, data):
        self.pizza_id = data['pizza_id']
        self.topping_id = data['topping_id']
        self.owner = None

    @classmethod
    def get_by_id(cls,data):
        query = "SELECT * FROM topping left join user on topping.user_id = user.id WHERE topping.id = %(id)s;"
        results = connectToMySQL(cls.my_db).query_db(query,data)
        return cls(results[0])

    @classmethod
    def save(cls, data, pizza_id, topping_list):
        print("Save toppings list: ", topping_list) 
        
        for i in topping_list:
            print("I: ",i)
            data = {
            "pizza_id": pizza_id,
            "topping_id": i
            }
            query = "INSERT INTO pizza_has_topping (pizza_id, topping_id) VALUES  (%(pizza_id)s, %(topping_id)s);"    
            results = connectToMySQL(cls.my_db).query_db(query,data)
            #print("Save toppings list: ", data) 
        return 

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM pizza_has_topping"
        results =  connectToMySQL(cls.my_db).query_db(query)
        pizza_has_topping = []
        for row in results:
            pizza_has_topping.append(cls(row))
        return results

    @classmethod
    def get_full_pie(cls):
        query = "SELECT * FROM pizza inner join pizza_has_topping on pizza.id = pizza_has_topping.pizza_id inner join topping on topping.id = topping_id "
        results =  connectToMySQL(cls.my_db).query_db(query)
        pizza_has_topping = []
        for row in results:
            pizza_has_topping.append(cls(row))
        return results
    @classmethod
    def update(cls, data):
        print(data)
        query = "UPDATE pizza_has_topping SET topping_name=%(topping_name)s, date=%(date)s, updated_at=NOW() WHERE id = %(id)s;" #fix
        return connectToMySQL(cls.my_db).query_db(query,data)
    
    @classmethod
    def destroy(cls,data):
        query = "DELETE FROM pizza_has_topping WHERE pizza_id = %(id)s;"
        return connectToMySQL(cls.my_db).query_db(query,data)
