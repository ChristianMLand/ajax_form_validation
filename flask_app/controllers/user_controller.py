import json
from flask import render_template,redirect,session,request,jsonify
from flask_app.models.user_model import User
from flask_app import app

#-----------------Display Routes--------#
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/success')
def success():
    return render_template('success.html')
#-----------------Action Routes---------#
@app.route('/register', methods=['POST'])
def register():
    errors = User.validate_register(request.form)
    if errors:
        return jsonify(errors)
    session['id'] = User.create(**request.form)
    return redirect('/success')

@app.route('/login', methods=['POST'])
def login():
    errors = User.validate_login(request.form)
    if errors:
        return jsonify(errors)
    user = User.retrieve_one(email=request.form['login_email'])
    session['id'] = user.id
    return redirect('/success')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')
#-----------------------------------------#