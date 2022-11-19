#pip install flask
#pip install flask-sqlalchemy
#pip install flask-restful
#pip install SQLAlchemy-serializer
#pip install psycopg2
#Odporúčam testovať cez PostMan-a
#SSL bude riešené až v WSGI spolu s apache / NGIX
from sqlalchemy_serializer import SerializerMixin
import json
import decimal, datetime
from flask import Flask, request,jsonify,make_response
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ARRAY, BigInteger, Boolean, Column, DateTime, ForeignKey, Table, Text, text
from sqlalchemy.orm import relationship
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

def alchemyencoder(obj):
    """JSON encoder function for SQLAlchemy special classes."""
    if isinstance(obj, datetime.date):
        return obj.isoformat()
    elif isinstance(obj, decimal.Decimal):
        return float(obj)

class Customer(Base, SerializerMixin):
    __tablename__ = 'Customer'

    Name = Column(Text)
    id = Column(Text, primary_key=True, server_default=text("uuid_in((md5(((random())::text || (random())::text)))::cstring)"))


class General(Base, SerializerMixin):
    __tablename__ = 'General'

    Last_changes = Column(DateTime)
    Last_available = Column(DateTime)
    Automatic_export = Column(Boolean)
    id = Column(Text, primary_key=True, server_default=text("uuid_in((md5(((random())::text || (random())::text)))::cstring)"))


class Stillage_type(Base, SerializerMixin):
    __tablename__ = 'Stillage_type'

    Name = Column(Text)
    id = Column(Text, primary_key=True, server_default=text("uuid_in((md5(((random())::text || (random())::text)))::cstring)"))


class User_Role(Base, SerializerMixin):
    __tablename__ = 'User_Role'

    name = Column(Text)
    id = Column(Text, primary_key=True, server_default=text("uuid_in((md5(((random())::text || (random())::text)))::cstring)"))


class Vehicle(Base, SerializerMixin):
    __tablename__ = 'Vehicle'

    SPZ = Column(Text)
    id = Column(Text, primary_key=True, server_default=text("uuid_in((md5(((random())::text || (random())::text)))::cstring)"))


class Config(Base, SerializerMixin):
    __tablename__ = 'Config'

    id = Column(Text, primary_key=True, server_default=text("uuid_in((md5(((random())::text || (random())::text)))::cstring)"))
    Customer_id = Column(ForeignKey('Customer.id'))
    Vehicle_id = Column(ForeignKey('Vehicle.id'))

    #Customer = relationship('Customer')
    #Vehicle = relationship('Vehicle')


class Pattern(Base, SerializerMixin):
    __tablename__ = 'Pattern'

    id = Column(Text, primary_key=True, server_default=text("uuid_in((md5(((random())::text || (random())::text)))::cstring)"))
    Customer_id = Column(ForeignKey('Customer.id'))

    #Customer = relationship('Customer')


class User(Base, SerializerMixin):
    __tablename__ = 'User'

    code = Column(BigInteger, primary_key=True)
    Name = Column(Text)
    Last_name = Column(Text)
    User_Role_id = Column(ForeignKey('User_Role.id', match='FULL'))

    #User_Role = relationship('UserRole')


class Advanced_user(Base, SerializerMixin):
    __tablename__ = 'Advanced_user'

    id = Column(Text, primary_key=True, server_default=text("uuid_in((md5(((random())::text || (random())::text)))::cstring)"))
    Config_id = Column(ForeignKey('Config.id'))
    User_code = Column(ForeignKey('User.code'))

    #Config = relationship('Config')
    #User = relationship('User')


class Pattern_Item(Base, SerializerMixin):
    __tablename__ = 'Pattern_Item'

    Number = Column(BigInteger)
    id = Column(Text, primary_key=True, server_default=text("uuid_in((md5(((random())::text || (random())::text)))::cstring)"))
    Pattern_id = Column(ForeignKey('Pattern.id'))
    Stillage_type_id = Column(ForeignKey('Stillage_type.id'))

    #Pattern = relationship('Pattern')
    #Stillage_type = relationship('StillageType')


class Shipment(Base, SerializerMixin):
    __tablename__ = 'Shipment'

    User_code = Column(ForeignKey('User.code'))
    Date_time_close = Column(DateTime)
    id = Column(Text, primary_key=True, server_default=text("uuid_in((md5(((random())::text || (random())::text)))::cstring)"))
    Customer_id = Column(ForeignKey('Customer.id'))
    Vehicle_id = Column(ForeignKey('Vehicle.id'))

    #Customer = relationship('Customer')
    #User = relationship('User')
    #Vehicle = relationship('Vehicle')


class Work_statement(Base, SerializerMixin):
    __tablename__ = 'Work_statement'

    User_code = Column(ForeignKey('User.code'))
    Work = Column(BigInteger)
    Time_start = Column(DateTime)
    Time_end = Column(DateTime)
    id = Column(Text, primary_key=True, server_default=text("uuid_in((md5(((random())::text || (random())::text)))::cstring)"))

    #User = relationship('User')


class Stillage(Base, SerializerMixin):
    __tablename__ = 'Stillage'

    Date_time_start = Column(DateTime)
    Date_time_end = Column(DateTime)
    Stillage_number = Column(BigInteger)
    Stillage_Number_on_Header = Column(BigInteger)
    First_scan_product = Column(BigInteger)
    Last_scan_product = Column(BigInteger)
    JLR_Header_NO = Column(BigInteger)
    Carriage_L_JLR_H = Column('Carriage_L_JLR_H', Text)
    _Check = Column(BigInteger)
    First_scan_TLS_code = Column(BigInteger)
    Last_scan_TLS_code = Column(BigInteger)
    id = Column(Text, primary_key=True, server_default=text("uuid_in((md5(((random())::text || (random())::text)))::cstring)"))
    Stillage_Type_id = Column(ForeignKey('Stillage_type.id'))
    Shipment_id = Column(ForeignKey('Shipment.id'))
    TLS_range_start = Column(BigInteger)
    TLS_range_stop = Column(BigInteger)
    Note = Column(Text)

    #Shipment = relationship('Shipment')
    #Stillage_Type = relationship('StillageType')


#Beží ako post a autentifikácia je cez json "api-heslo" s heslom "
class Get(Resource):
    def post(self):
        if request.is_json and ("tabulka" in request.json) and (request.json['api-heslo']=="YouWontGuessThisOne"):
            db.session.execute('SET TRANSACTION ISOLATION LEVEL SERIALIZABLE;')
            tabulka = []
            if(request.json['tabulka'] == "General"):
                tabulka = General.query.all()

            elif(request.json['tabulka'] == "User_Role"):
                tabulka = User_Role.query.all()

            elif(request.json['tabulka'] == "Customer"):
                tabulka = Customer.query.all()

            elif(request.json['tabulka'] == "Vehicle"):
                tabulka = Vehicle.query.all()

            elif(request.json['tabulka'] == "User"):
                tabulka = User.query.all()

            elif(request.json['tabulka'] == "Config"):
                tabulka = Config.query.all()

            elif(request.json['tabulka'] == "Shipment"):
                tabulka = Shipment.query.all()

            elif(request.json['tabulka'] == "Pattern"):
                tabulka = Pattern.query.all()

            elif(request.json['tabulka'] == "Work_statement"):
                tabulka = Work_statement.query.all()

            elif(request.json['tabulka'] == "Stillage_type"):
                tabulka = Stillage_type.query.all()

            elif(request.json['tabulka'] == "Advanced_user"):
                tabulka = Advanced_user.query.all()

            elif(request.json['tabulka'] == "Stillage"):
                tabulka = Stillage.query.all()

            elif(request.json['tabulka'] == "Pattern_Item"):
                tabulka = Pattern_Item.query.all()
            else:
                return {'error': 'Netrafil si tabuľku'}, 400

            return [r.to_dict() for r in tabulka], 200
        else:
            return {'error': 'Formát musí byť JSON'}, 400


class Post(Resource):
    def post(self):
        if request.is_json and ("tabulka" in request.json) and (request.json['api-heslo']=="YouWontGuessThisOne"):
            db.session.execute('SET TRANSACTION ISOLATION LEVEL SERIALIZABLE;')
            data = request.json['data']
            for riadok in data:
                if(request.json['tabulka']=="User"):
                    prikaz = f"{request.json['tabulka']}.query.filter_by(code=riadok.get('code')).first()"
                else:
                    prikaz = f"{request.json['tabulka']}.query.filter_by(id=riadok.get('id')).first()"
                vysledok = eval(prikaz)
                if(vysledok):
                    pass
                else:
                    prikaz = f"db.session.add({request.json['tabulka']}(**riadok))"
                    eval(prikaz)
            db.session.commit()

            return {'ok': 'spracovane'}, 200

            # emp = Pracovnik(meno=request.json['meno'], priezvisko=request.json['priezvisko'])
            # db.session.add(emp)
            # db.session.commit()
            # vrátim json odpoveď
            # return make_response(jsonify({'id': emp.id, 'meno': emp.meno, 'priezvisko': emp.priezvisko}), 201)
        else:
            return {'error': 'Formát musí byť JSON'}, 400

api.add_resource(Get, '/Get') #Funkcia vracia obsah pozadovanej tabulky
api.add_resource(Post, '/Post') # Funkcia si nahrá poslaný riadok do tabulky
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5100)
