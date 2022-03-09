from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DB,bcrypt
from flask import flash
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
#-----------------Properties---------------#
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
#-----------------Create-------------------#
    @classmethod
    def create(cls, **data):
        query = '''
                INSERT INTO users
                (first_name, last_name, email, password)
                VALUES
                (%(first_name)s,%(last_name)s,%(email)s,%(password)s);
                '''
        data['password'] = bcrypt.generate_password_hash(data['password'])
        return connectToMySQL(DB).query_db(query, data)
#-----------------Retrieve-------------------#
    @classmethod
    def retrieve_one(cls,**data):
        query = 'SELECT * FROM users WHERE '
        query += ' AND '.join(f"{key} = %({key})s" for key in data)
        query += ' LIMIT 1;'
        results = connectToMySQL(DB).query_db(query, data)
        if results:
            return cls(results[0])
#-----------------Validate----------------#
    def validate_register(data):
        errors = {}

        if 'first_name' in data and len(data['first_name']) < 2:
            errors['first_name'] = 'First name should be at least 2 characters'
        if 'last_name' in data and len(data['last_name']) < 2:
            errors['last_name'] = 'Last name should be at least 2 characters'
        if 'email' in data and not EMAIL_REGEX.match(data['email']):
            errors['email'] = 'Email format is invalid'
        elif 'email' in data and User.retrieve_one(email=data['email']):
            errors['email'] = 'Email is already in use'
        if 'password' in data:
            if len(data['password']) < 8:
                errors['password'] = 'Password should be at least 8 characters'
            elif 'confirm_password' in data and data['password'] != data['confirm_password']:
                errors['confirm_password'] = 'Passwords do not match'

        return errors

    def validate_login(data):
        errors = {}
        user = User.retrieve_one(email=data['login_email'])

        if not user:
            errors['login_email'] = 'Invalid Credentials'
        elif not bcrypt.check_password_hash(user.password, data['login_password']):
            errors['login_password'] = 'Invalid Credentials'

        return errors