from flask import Blueprint, request, session, jsonify,redirect,url_for,render_template
from sqlalchemy.exc import IntegrityError
from app import db
from .models import Others
from app.courier.controllers import mod_courier

mod_others = Blueprint('others', __name__,url_prefix='/')

@mod_others.route('api/loginpage2',methods=['GET'])
def login_page():
    return render_template('indexo.html')

@mod_others.route('api/login2', methods=['GET'])
def check_login():
    if 'user_id2' in session:
        user = Others.query.filter(Others.id == session['user_id2']).first()
        return jsonify(success=True, user=user.to_dict())

    return jsonify(success=False), 401


@mod_others.route('api/login2', methods=['POST'])
def login():
    try:
        email = request.form['email']
        password = request.form['password']
    except KeyError as e:
        return jsonify(success=False, message="%s not sent in the request" % e.args), 400

    user = Others.query.filter(Others.email == email).first()
    if user is None or not user.check_password(password):
        return redirect(url_for('others.mainPage'))
        return jsonify(success=False, message="Invalid Credentials"), 400

    session['user_id2'] = user.id

    return redirect(url_for('courier.get_all_courier_others'))
    return jsonify(success=True, user=user.to_dict())

@mod_others.route('/', methods=['POST'])
def logout():
    session.pop('user_id2')
    return render_template('indexo.html')
    return jsonify(success=True)

@mod_others.route('/',methods=['GET'])
def mainPage():
    if 'user_id2' in session:
        return redirect(url_for('courier.get_all_courier_others'))
    return render_template('indexo.html')

@mod_others.route('api/register2', methods=['POST'])
def create_user():
    try:
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
    except KeyError as e:
        return jsonify(success=False, message="%s not sent in the request" % e.args), 400

    if '@' not in email:
        return jsonify(success=False, message="Please enter a valid email"), 400

    u = Others(name, email, password)
    db.session.add(u)
    try:
        db.session.commit()
    except IntegrityError as e:
        return jsonify(success=False, message="This email already exists"), 400
    return redirect(url_for('others.mainPage'))
    return render_template('indexo.html')
    return jsonify(success=True)

@mod_others.route('api/register2',methods=['GET'])
def c_user():
    return render_template('rego.html')
