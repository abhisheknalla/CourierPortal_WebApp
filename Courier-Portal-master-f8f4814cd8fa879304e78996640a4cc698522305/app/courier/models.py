from flask_sqlalchemy import SQLAlchemy
from app import db


class Courier(db.Model):
    __tablename__='couriers'
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    name=db.Column(db.String(50))
    date=db.Column(db.String(15))
    roomno=db.Column(db.Integer)
    hostel=db.Column(db.String(20))
    typ=db.Column(db.String(50))
    addr=db.Column(db.String(60))

    def __init__(self,name,date,roomno,hostel,typ,addr):
        self.name=name
        self.date=date
        self.roomno=roomno
        self.hostel=hostel
        self.typ=typ
        self.addr=addr


    def __repr__(self):
        return '%r %r %r\n'%(self.name,self.hostel,self.roomno)
