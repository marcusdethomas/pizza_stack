from flask_app.config.mysqlconnection import MySQLConnection, connectToMySQL
from flask_app.controllers import users
from pickle import TRUE, FALSE
from flask import flash, session
from flask_app.models.user import User
from flask_app.models.pizza import Pizza

class Topping:
    my_db = 'pizza_stack'
    def __init__(self, data):
        self.id = data['id']
        self.topping_name = data['topping_name']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.owner = None

    @classmethod
    def get_by_id(cls,data):
        query = "SELECT * FROM topping left join user on topping.user_id = user.id WHERE topping.id = %(id)s;"
        results = connectToMySQL(cls.my_db).query_db(query,data)
        return cls(results[0])

    @classmethod
    def save(cls, data):
        query = "INSERT INTO topping (topping_name, user_id) VALUES  (%(topping_name)s, %(user_id)s);"
        return connectToMySQL(cls.my_db).query_db(query, data)

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM topping join user on topping.user_id = user.id;"
        results =  connectToMySQL(cls.my_db).query_db(query)
        all_toppings = []
        for row in results:
            all_toppings.append(cls(row))
        return results

    @classmethod
    def update(cls, data):
        query = "UPDATE topping SET topping_name=%(topping_name)s, updated_at=NOW() WHERE id = %(id)s;"
        return connectToMySQL(cls.my_db).query_db(query,data)
    
    @classmethod
    def destroy(cls,data):
        query = "DELETE FROM topping WHERE id = %(id)s;"
        print('Destroy')
        return connectToMySQL(cls.my_db).query_db(query,data)

    @staticmethod   
    def validate_entry(data):
        is_valid = TRUE
        if len(data['topping_name']) < 3:
                flash('Topping name must be at least three characters or more.')
                is_valid =  False
        return is_valid
        
    @classmethod
    def check_duplicate(cls, data):
        is_duplicate = True
        query = 'SELECT * FROM  topping where topping_name = (%(topping_name)s)'
        results = MySQLConnection(cls.my_db).query_db(query, data)
        if len(results) >= 1:
                flash('Topping already exists.')
                is_duplicate = False
        return is_duplicate