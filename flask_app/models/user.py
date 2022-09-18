from unittest import result
from flask_app.controllers import users
from flask_app.config.mysqlconnection import MySQLConnection, connectToMySQL
from flask import flash
from pickle import TRUE, FALSE
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

class User:
    my_db='pizza_stack'
    def __init__(self, data):
        self.id =  data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.role = data['role']
        self.pizza_id = data['pizza_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def create_login(cls, data):
        query = 'INSERT INTO user (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s)'
        results = MySQLConnection(cls.my_db).query_db(query, data)
        return results
        
    @classmethod
    def get_all(cls):
        query = 'SELECT * FROM user;'
        results = connectToMySQL(cls.my_db).query_db(query)
        users = []
        for row in results:
            users.append( cls(row))
        return users
        
    @classmethod
    def get_by_email(cls,data):
        query = 'SELECT * FROM user WHERE email = %(email)s;'
        results = connectToMySQL(cls.my_db).query_db(query,data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod
    def get_by_id(cls,data):
        query = "SELECT * FROM user WHERE id = %(id)s;"
        results = connectToMySQL(cls.my_db).query_db(query,data)
        return cls(results[0])
        

    @classmethod
    def check_duplicate(cls, data):
        is_duplicate = True
        query = 'SELECT email FROM  user where email = (%(email)s)'
        results = MySQLConnection(cls.my_db).query_db(query, data)
        if len(results) >= 1:
                flash('Email already exists.')
                is_duplicate = False
        return is_duplicate

    @staticmethod
    def verify_login(data):
        is_valid = TRUE
        if len(data['first_name']) < 2:
                flash('First name must be at least 2 characters or more.')
                is_valid =  False
        if len(data['last_name']) < 2:
                flash('Last name must be at least 2 characters or more.')
                is_valid =  False
        if len(data['password']) < 8:
                flash('Password must be at least 8 characters or more.')
                is_valid =  False
        if (data['password']) != (data['confirm_password']):
                flash('Password does not match.')
                is_valid =  False
        if not EMAIL_REGEX.match(data['email']): 
            if len(data['email']) < 1:
                flash('Email field cannot be blank.')
            else:
                flash("Enter a valid email address!")
            is_valid = False
        return is_valid
