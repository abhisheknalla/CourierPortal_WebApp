from flask import jsonify,request,session,Blueprint,render_template,redirect,url_for
from app import db,requires_auth,requires_auth2
from .models import Courier

mod_courier=Blueprint('courier',__name__)

@mod_courier.route('/addNew',methods=['GET'])
@requires_auth
def just():
    return render_template('index2.html')

@mod_courier.route('/couriers',methods=['GET'])
@requires_auth
def get_all_couriers():
    couriers={"couriers":[]}
    criers=Courier.query.all()
    for c in criers:
        ans={}
        ans['name']=c.name
        ans['date']=c.date
        ans['roomno']=c.roomno
        ans['hostel']=c.hostel
        ans['typ']=c.typ
        ans['addr']=c.addr
        couriers['couriers'].append(ans)
    return jsonify(couriers)

@mod_courier.route('/addCourier',methods=['POST'])
@requires_auth
def add_courier():
    print("entering")
    name=request.form['name']
    date=request.form['date']
    roomno=request.form['roomno']
    hostel=request.form['hostel']
    typ=request.form['typ']
    addr=request.form['addr']
    courier=Courier(name,date,roomno,hostel,typ,addr)
    try:
        print("try")
        db.session.add(courier)
        db.session.commit()
        return redirect(url_for('courier.get_all_courier'))
        return "Success: added succesfully"
    except:
        print("except")
        return "Error: not added"

@mod_courier.route('/list',methods=['GET'])
@requires_auth
def get_all_courier():
    criers=Courier.query.all()
    return render_template('list.html',couriers=criers)

@mod_courier.route('/search',methods=['POST'])
@requires_auth
def list_search():
    s=request.form['search']
    if s!="":
        criers=Courier.query.filter(Courier.name.like("%"+s+"%")).all()
        return render_template('list.html',couriers=criers)
    return redirect(url_for('courier.get_all_courier'))

@mod_courier.route('/searchOthers',methods=['POST'])
@requires_auth2
def list_search_others():
    s=request.form['search']
    if s!="":
        criers=Courier.query.filter(Courier.name.like("%"+s+"%")).all()
        return render_template('list2.html',couriers=criers)
    return redirect(url_for('courier.get_all_courier_others'))

@mod_courier.route('/delete',methods=['POST'])
@requires_auth
def delete():
    id=request.form['del']
    try:
        cour=Courier.query.filter(Courier.id==id).first()
        db.session.delete(cour)
        db.session.commit()
        return redirect(url_for('courier.get_all_courier'))
    except:
        return redirect(url_for('courier.get_all_courier'))

@mod_courier.route('/listOthers',methods=['GET'])
@requires_auth2
def get_all_courier_others():
    criers=Courier.query.all()
    return render_template('list2.html',couriers=criers)
