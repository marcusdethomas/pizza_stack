from flask_app.config.mysqlconnection import MySQLConnection, connectToMySQL
from flask_app.controllers import users
from pickle import TRUE, FALSE
from flask import flash, session

from flask_app.models.user import User

class Pizza:
    my_db = 'pizza_stack'
    def __init__(self, data):
        self.id = data['id']
        self.pizza_name = data['pizza_name']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.owner = None

    @classmethod
    def get_by_id(cls,data):
        query = "SELECT * FROM pizza left join user on pizza.user_id = user.id WHERE pizza.id = %(id)s;"
        results = connectToMySQL(cls.my_db).query_db(query,data)
        return cls(results[0])

    @classmethod
    def get_by_name(cls,data):
        query = "SELECT * FROM pizza left join user on pizza.user_id = user.id WHERE pizza_name = %(pizza_name)s;"
        results = connectToMySQL(cls.my_db).query_db(query,data)
        return cls(results[0])


    @classmethod
    def save(cls, data):
        query = "INSERT INTO pizza (pizza_name, user_id) VALUES  (%(pizza_name)s, %(user_id)s);"
        return connectToMySQL(cls.my_db).query_db(query, data)
        
    #get all toppings from pizzas in database
    @classmethod
    def get_pizza_toppings(cls, data):
        query = "SELECT * FROM user \
                inner join pizza inner join pizza_has_topping on pizza.id = pizza_has_topping.pizza_id \
                inner join topping on topping.id = topping_id \
                where %(id)s = pizza.id"
        return connectToMySQL(cls.my_db).query_db(query, data)
        
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM pizza join user on pizza.user_id = user.id;"
        results =  connectToMySQL(cls.my_db).query_db(query)
        all_pizzas = []
        for row in results:
            all_pizzas.append(cls(row))
        return results

    @classmethod
    def update(cls, data):
        print(data)
        query = "UPDATE pizza SET pizza_name=%(pizza_name)s, date=%(date)s, updated_at=NOW() WHERE id = %(id)s;"
        return connectToMySQL(cls.my_db).query_db(query,data)
    
    @classmethod
    def destroy(cls,data):
        query = "DELETE FROM pizza WHERE id = %(id)s;"
        return connectToMySQL(cls.my_db).query_db(query,data)

    @staticmethod   
    def validate_entry(data):
        is_valid = TRUE
        if len(data['pizza_name']) < 3:
                flash('Pizza name must be at least three characters or more.')
                is_valid =  False
        return is_valid
        