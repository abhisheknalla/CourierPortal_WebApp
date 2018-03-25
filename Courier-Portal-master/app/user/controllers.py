from flask import Blueprint, request, session, jsonify,redirect,url_for,render_template
from sqlalchemy.exc import IntegrityError
from app import db
from .models import User
from app.courier.controllers import mod_courier

mod_user = Blueprint('user', __name__, url_prefix='/')#api')

@mod_user.route('api/loginpage',methods=['GET'])
def login_page():
    if 'user_id' in session:
        return redirect(url_for('courier.get_all_courier'))
    return render_template('index.html')

@mod_user.route('api/login', methods=['GET'])
def check_login():
    if 'user_id' in session:
        user = User.query.filter(User.id == session['user_id']).first()
        return jsonify(success=True, user=user.to_dict())

    return jsonify(success=False), 401


@mod_user.route('api/login', methods=['POST'])
def login():
    try:
        email = request.form['email']
        password = request.form['password']
    except KeyError as e:
        return jsonify(success=False, message="%s not sent in the request" % e.args), 400

    user = User.query.filter(User.email == email).first()
    if user is None or not user.check_password(password):
        return jsonify(success=False, message="Invalid Credentials"), 400

    session['user_id'] = user.id

    return redirect(url_for('courier.get_all_courier'))
    return jsonify(success=True, user=user.to_dict())

@mod_user.route('api/loginpage', methods=['POST'])
def logout():
    session.pop('user_id')
    return render_template('index.html')
    return jsonify(success=True)

@mod_user.route('api/loginpage',methods=['GET'])
def mainPage():
	return render_template('index.html')

@mod_user.route('api/register', methods=['POST'])
def create_user():
    try:
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
    except KeyError as e:
        return jsonify(success=False, message="%s not sent in the request" % e.args), 400

    if '@' not in email:
        return jsonify(success=False, message="Please enter a valid email"), 400

    u = User(name, email, password)
    db.session.add(u)
    try:
        db.session.commit()
    except IntegrityError as e:
        return jsonify(success=False, message="This email already exists"), 400
    return redirect(url_for('user.mainPage'))
    return render_template('index.html')
    return jsonify(success=True)

@mod_user.route('api/register',methods=['GET'])
def c_user():
    return render_template('reg.html')



@mod_user.route('allusers')
def allUsers():
    ppl= User.query.all()
    for u in ppl:
        print(u.email)
    return "Hello"
