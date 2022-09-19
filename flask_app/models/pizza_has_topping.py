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
    def save(cls, data, topping_list):
        #print("Full pizza: ",data)
        print("Save toppings list: ", topping_list)
        for topping in topping_list:
            query = "INSERT INTO pizza_has_topping (pizza_id, topping_id) VALUES  (%(pizza_id)s, topping);"     #need to fix
        return connectToMySQL(cls.my_db).query_db(query, data)

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM pizza_has_topping"
        results =  connectToMySQL(cls.my_db).query_db(query)
        pizza_has_topping = []
        for row in results:
            pizza_has_topping.append(cls(row))
        return results

    @classmethod
    def update(cls, data):
        print(data)
        query = "UPDATE topping SET topping_name=%(topping_name)s, date=%(date)s, updated_at=NOW() WHERE id = %(id)s;"
        return connectToMySQL(cls.my_db).query_db(query,data)
    
    @classmethod
    def destroy(cls,data):
        query = "DELETE FROM topping WHERE id = %(id)s;"
        return connectToMySQL(cls.my_db).query_db(query,data)

    @staticmethod   
    def validate_entry(data):
        is_valid = TRUE
        if len(data['topping_name']) < 3:
                flash('Topping name must be at least three characters or more.')
                is_valid =  False
        return is_valid
        