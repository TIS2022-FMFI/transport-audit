#pip install flask
#pip install flask-sqlalchemy
#pip install flask-restful
#pip install mysqlclient
#Odporúčam testovať cez PostMan-a
#SSL bude riešené až v WSGI spolu s apache / NGIX
from flask import Flask, request,jsonify,make_response
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ARRAY, BigInteger, Boolean, Column, DateTime, ForeignKey, Table, Text, text
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import INT4RANGE
from sqlalchemy.ext.declarative import declarative_base
#vytvorí inštanciu Flasku
app = Flask(__name__)
# Vytvorí api objekt
api = Api(app)

#Vytvorí databázu
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://admin:Verejne_zname_heslo_47@server.nahovno.eu:5432/audit-preprav'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#SQL alchemy inštancia
db = SQLAlchemy(app)

# Definicia tabuliek
Base = db.Model
metadata = Base.metadata

class Customer(Base):
    __tablename__ = 'Customer'

    Name = Column(Text)
    id = Column(Text, primary_key=True, server_default=text("uuid_in((md5(((random())::text || (random())::text)))::cstring)"))


class General(Base):
    __tablename__ = 'General'

    Last_changes = Column(DateTime)
    Last_available = Column(DateTime)
    Automatic_export = Column(Boolean)
    id = Column(Text, primary_key=True, server_default=text("uuid_in((md5(((random())::text || (random())::text)))::cstring)"))


class StillageType(Base):
    __tablename__ = 'Stillage_type'

    Name = Column(Text)
    id = Column(Text, primary_key=True, server_default=text("uuid_in((md5(((random())::text || (random())::text)))::cstring)"))


class UserRole(Base):
    __tablename__ = 'User_Role'

    name = Column(Text)
    id = Column(Text, primary_key=True, server_default=text("uuid_in((md5(((random())::text || (random())::text)))::cstring)"))


class Vehicle(Base):
    __tablename__ = 'Vehicle'

    SPZ = Column(Text)
    id = Column(Text, primary_key=True, server_default=text("uuid_in((md5(((random())::text || (random())::text)))::cstring)"))


class Config(Base):
    __tablename__ = 'Config'

    id = Column(Text, primary_key=True, server_default=text("uuid_in((md5(((random())::text || (random())::text)))::cstring)"))
    Customer_id = Column(ForeignKey('Customer.id'))
    Vehicle_id = Column(ForeignKey('Vehicle.id'))

    Customer = relationship('Customer')
    Vehicle = relationship('Vehicle')


class Pattern(Base):
    __tablename__ = 'Pattern'

    id = Column(Text, primary_key=True, server_default=text("uuid_in((md5(((random())::text || (random())::text)))::cstring)"))
    Customer_id = Column(ForeignKey('Customer.id'))

    Customer = relationship('Customer')


class User(Base):
    __tablename__ = 'User'

    code = Column(BigInteger, primary_key=True)
    Name = Column(Text)
    Last_name = Column(Text)
    User_Role_id = Column(ForeignKey('User_Role.id', match='FULL'))

    User_Role = relationship('UserRole')


class AdvancedUser(Base):
    __tablename__ = 'Advanced_user'

    id = Column(Text, primary_key=True, server_default=text("uuid_in((md5(((random())::text || (random())::text)))::cstring)"))
    Config_id = Column(ForeignKey('Config.id'))
    User_code = Column(ForeignKey('User.code'))

    Config = relationship('Config')
    User = relationship('User')


class PatternItem(Base):
    __tablename__ = 'Pattern_Item'

    Number = Column(BigInteger)
    id = Column(Text, primary_key=True, server_default=text("uuid_in((md5(((random())::text || (random())::text)))::cstring)"))
    Pattern_id = Column(ForeignKey('Pattern.id'))
    Stillage_type_id = Column(ForeignKey('Stillage_type.id'))

    Pattern = relationship('Pattern')
    Stillage_type = relationship('StillageType')


class Shipment(Base):
    __tablename__ = 'Shipment'

    User_code = Column(ForeignKey('User.code'))
    Date_time_close = Column(DateTime)
    id = Column(Text, primary_key=True, server_default=text("uuid_in((md5(((random())::text || (random())::text)))::cstring)"))
    Customer_id = Column(ForeignKey('Customer.id'))
    Vehicle_id = Column(ForeignKey('Vehicle.id'))

    Customer = relationship('Customer')
    User = relationship('User')
    Vehicle = relationship('Vehicle')


class WorkStatement(Base):
    __tablename__ = 'Work_statement'

    User_code = Column(ForeignKey('User.code'))
    Work = Column(BigInteger)
    Time_start = Column(DateTime)
    Time_end = Column(DateTime)
    id = Column(Text, primary_key=True, server_default=text("uuid_in((md5(((random())::text || (random())::text)))::cstring)"))

    User = relationship('User')


class Stillage(Base):
    __tablename__ = 'Stillage'

    Date_time_start = Column(DateTime)
    Date_time_end = Column(DateTime)
    Stillage_number = Column(BigInteger)
    TLS_range = Column(INT4RANGE)
    Stillage_Number_on_Header = Column(BigInteger)
    First_scan_product = Column(BigInteger)
    Last_scan_product = Column(BigInteger)
    JLR_Header_NO = Column(BigInteger)
    Carriage_L_JLR_H = Column('Carriage_L+JLR_H', Text)
    Check = Column(BigInteger)
    Note = Column(ARRAY(Text()))
    First_scan_TLS_code = Column(BigInteger)
    Last_scan_TLS_code = Column(BigInteger)
    id = Column(Text, primary_key=True, server_default=text("uuid_in((md5(((random())::text || (random())::text)))::cstring)"))
    Stillage_Type_id = Column(ForeignKey('Stillage_type.id'))
    Shipment_id = Column(ForeignKey('Shipment.id'))

    Shipment = relationship('Shipment')
    Stillage_Type = relationship('StillageType')


#Beží ako post a autentifikácia je cez json "api-heslo" s heslom "
class Get(Resource):
    def post(self):
        if request.is_json:

            if(request.json['api-heslo']=="YouWontGuessThisOne"):
                employees = General.query.all()
                emp_list = []
                for emp in employees:
                    emp_data = {'Id': emp.id, 'Meno': emp.meno, 'Priezvisko': emp.priezvisko}
                    emp_list.append(emp)
                return {"Všetci pracovníci": emp_list}, 200
        else:
            return {'error': 'Formát musí byť JSON'}, 400

# Bude bezat na /pridat - táto funkcia v skutocnosti nie je potrebna,
# pretože potrebujeme iba get, pridavanie pojde cez php my admin
# class Pridať(Resource):
#     def post(self):
#         if request.is_json:
#             emp = Pracovnik(meno=request.json['meno'], priezvisko=request.json['priezvisko'])
#             db.session.add(emp)
#             db.session.commit()
#             # vrátim json odpoveď
#             return make_response(jsonify({'id': emp.id, 'meno': emp.meno, 'priezvisko': emp.priezvisko}), 201)
#         else:
#             return {'error': 'Formát musí byť JSON'}, 400

api.add_resource(Get, '/')
#api.add_resource(Pridať, '/pridat') # do buducna zmazať
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5100)
