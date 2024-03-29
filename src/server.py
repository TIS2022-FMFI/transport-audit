#pip install flask
#pip install flask-sqlalchemy
#pip install flask-restful
#pip install SQLAlchemy-serializer
#pip install psycopg2
#pip install python-dateutil
#Odporúčam testovať cez PostMan-a
#SSL bude riešené až v WSGI spolu s apache / NGIX
import os

import psycopg2 as pscpg2
from sqlalchemy_serializer import SerializerMixin
import json
import decimal, datetime
from flask import Flask, request,jsonify,make_response, send_file, flash,redirect, url_for
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ARRAY, BigInteger, Boolean, Column, DateTime, ForeignKey, Table, Text, text
from sqlalchemy.orm import relationship
from dateutil.parser import parse
from werkzeug.utils import secure_filename
import numpy as np
#APi-heslo:
API_PASSWD='94bd18c7-91a4-4f79-b45a-7a59105631f4'
########################


#Pripojenie pre logy:

conn_logy = pscpg2.connect(
    host="127.0.0.1",
    database="wrp_audit_web",
    user="app_wrp_audit_web",
    password="lAM*c.mho`i;x^",
    options="-c search_path=public")
cur_logy = conn_logy.cursor()

#vytvorí inštanciu Flasku
app = Flask(__name__)
# Vytvorí api objekt
api = Api(app)


#Vytvorí databázu
db_hesielko = """J!i"wLJ0uQE_I/"""
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://app_wrp_audit:{db_hesielko}@127.0.0.1:5432/wrp_audit'
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
    last_sync = Column(DateTime, server_default=text("(now())::timestamp without time zone"))
    doplnok = Column(Text)
    vykonavatel = Column(BigInteger)


class General(Base, SerializerMixin):
    __tablename__ = 'General'

    Last_changes = Column(DateTime)
    Last_available = Column(DateTime)
    Automatic_export = Column(Boolean)
    id = Column(Text, primary_key=True, server_default=text("uuid_in((md5(((random())::text || (random())::text)))::cstring)"))
    last_sync = Column(DateTime, server_default=text("(now())::timestamp without time zone"))
    doplnok = Column(Text)
    vykonavatel = Column(BigInteger)


class Stillage_type(Base, SerializerMixin):
    __tablename__ = 'Stillage_type'

    Name = Column(Text)
    id = Column(Text, primary_key=True, server_default=text("uuid_in((md5(((random())::text || (random())::text)))::cstring)"))
    last_sync = Column(DateTime, server_default=text("(now())::timestamp without time zone"))
    doplnok = Column(Text)
    vykonavatel = Column(BigInteger)


class User_Role(Base, SerializerMixin):
    __tablename__ = 'User_Role'

    name = Column(Text)
    id = Column(Text, primary_key=True, server_default=text("uuid_in((md5(((random())::text || (random())::text)))::cstring)"))
    last_sync = Column(DateTime, server_default=text("(now())::timestamp without time zone"))
    doplnok = Column(Text)
    vykonavatel = Column(BigInteger)


class Vehicle(Base, SerializerMixin):
    __tablename__ = 'Vehicle'

    SPZ = Column(Text)
    id = Column(Text, primary_key=True, server_default=text("uuid_in((md5(((random())::text || (random())::text)))::cstring)"))
    last_sync = Column(DateTime, server_default=text("(now())::timestamp without time zone"))
    doplnok = Column(Text)
    vykonavatel = Column(BigInteger)


class Config(Base, SerializerMixin):
    __tablename__ = 'Config'

    id = Column(Text, primary_key=True, server_default=text("uuid_in((md5(((random())::text || (random())::text)))::cstring)"))
    Customer_id = Column(ForeignKey('Customer.id'))
    Vehicle_id = Column(ForeignKey('Vehicle.id'))
    last_sync = Column(DateTime, server_default=text("(now())::timestamp without time zone"))
    doplnok = Column(Text)
    vykonavatel = Column(BigInteger)

    #Customer = relationship('Customer')
    #Vehicle = relationship('Vehicle')


class Pattern(Base, SerializerMixin):
    __tablename__ = 'Pattern'

    id = Column(Text, primary_key=True, server_default=text("uuid_in((md5(((random())::text || (random())::text)))::cstring)"))
    Customer_id = Column(ForeignKey('Customer.id'))
    last_sync = Column(DateTime, server_default=text("(now())::timestamp without time zone"))
    doplnok = Column(Text)
    vykonavatel = Column(BigInteger)

    #Customer = relationship('Customer')


class User(Base, SerializerMixin):
    __tablename__ = 'User'

    code = Column(BigInteger, primary_key=True)
    Name = Column(Text)
    Last_name = Column(Text)
    User_Role_id = Column(ForeignKey('User_Role.id', match='FULL'))
    last_sync = Column(DateTime, server_default=text("(now())::timestamp without time zone"))
    doplnok = Column(Text)
    vykonavatel = Column(BigInteger)

    #User_Role = relationship('UserRole')


class Advanced_user(Base, SerializerMixin):
    __tablename__ = 'Advanced_user'

    id = Column(Text, primary_key=True, server_default=text("uuid_in((md5(((random())::text || (random())::text)))::cstring)"))
    Config_id = Column(ForeignKey('Config.id'))
    User_code = Column(ForeignKey('User.code'))
    last_sync = Column(DateTime, server_default=text("(now())::timestamp without time zone"))
    doplnok = Column(Text)
    vykonavatel = Column(BigInteger)

    #Config = relationship('Config')
    #User = relationship('User')


class Pattern_Item(Base, SerializerMixin):
    __tablename__ = 'Pattern_Item'

    Number = Column(BigInteger)
    id = Column(Text, primary_key=True, server_default=text("uuid_in((md5(((random())::text || (random())::text)))::cstring)"))
    Pattern_id = Column(ForeignKey('Pattern.id'))
    Stillage_type_id = Column(ForeignKey('Stillage_type.id'))
    last_sync = Column(DateTime, server_default=text("(now())::timestamp without time zone"))
    doplnok = Column(Text)
    vykonavatel = Column(BigInteger)

    #Pattern = relationship('Pattern')
    #Stillage_type = relationship('StillageType')


class Shipment(Base, SerializerMixin):
    __tablename__ = 'Shipment'

    User_code = Column(ForeignKey('User.code'))
    Date_time_close = Column(DateTime)
    id = Column(Text, primary_key=True, server_default=text("uuid_in((md5(((random())::text || (random())::text)))::cstring)"))
    Customer_id = Column(ForeignKey('Customer.id'))
    Vehicle_id = Column(ForeignKey('Vehicle.id'))
    last_sync = Column(DateTime, server_default=text("(now())::timestamp without time zone"))
    doplnok = Column(Text)
    vykonavatel = Column(BigInteger)

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
    last_sync = Column(DateTime, server_default=text("(now())::timestamp without time zone"))
    doplnok = Column(Text)
    vykonavatel = Column(BigInteger)

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
    last_sync = Column(DateTime, server_default=text("(now())::timestamp without time zone"))
    doplnok = Column(Text)
    vykonavatel = Column(BigInteger)

    #Shipment = relationship('Shipment')
    #Stillage_Type = relationship('StillageType')


#Beží ako post a autentifikácia je cez json "api-heslo" s heslom "
class Get(Resource):
    def post(self):
        if request.is_json and ("tabulka" in request.json) and (request.json['api-heslo']==API_PASSWD):
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
        if request.is_json and ("tabulka" in request.json) and (request.json['api-heslo']==API_PASSWD):
            db.session.execute('SET TRANSACTION ISOLATION LEVEL SERIALIZABLE;')
            data = request.json['data']
            for riadok in data:
                if(request.json['tabulka']=="User"):
                    prikaz = f"{request.json['tabulka']}.query.filter_by(code=riadok.get('code')).first()"
                else:
                    prikaz = f"{request.json['tabulka']}.query.filter_by(id=riadok.get('id')).first()"
                vysledok = eval(prikaz)
                if(vysledok):
                    timestamp_server = parse(str(vysledok.last_sync))
                    timestamp_client = parse(riadok.get('last_sync'))
                    if(timestamp_client > timestamp_server):
                        prikaz = f"db.session.merge({request.json['tabulka']}(**riadok))"
                        eval(prikaz)
                        #print("menim")
                    continue

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

class Log(Resource):
    def post(self):
        if request.is_json and ("tabulka" in request.json) and (request.json['api-heslo']==API_PASSWD):
            data = request.json['data']
            for riadok in data:
                if(request.json['tabulka']=="logy"):
                    cur_logy.execute("SELECT id FROM logy WHERE id = %s", (riadok.get('id'),))
                    if cur_logy.fetchone() is None:
                        id_text = "'"+riadok.get("id")+"'"
                        chyba_text= "'"+riadok.get("chyba")+"'"
                        uzivatel_text = "'" + riadok.get("uzivatel") + "'"
                        doplnok_text = "'" + riadok.get("doplnok") + "'"
                        cur_logy.execute(
                            f'INSERT INTO logy (id, kod_chyby, chyba,uzivatel,android,doplnok) VALUES ({id_text},{riadok.get("kod_chyby")},{chyba_text},{uzivatel_text},{riadok.get("android")},{doplnok_text})',
                        )
                        cur_logy.execute("COMMIT")

            return {'ok': 'spracovane'}, 200

        else:
            return {'error': 'Formát musí byť JSON'}, 400

class Report(Resource):
    def post(self):
        if request.is_json and  (request.json['api-heslo']==API_PASSWD):

            return send_file("report.csv")

        else:
            return None
upload_path = os.path.abspath(os.path.dirname(__file__)) + ""
UPLOAD_FOLDER = os.path.normpath(upload_path)
ALLOWED_EXTENSIONS = {'csv'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
class Send_report(Resource):
    def post(self):
        if request.headers.get('api-heslo') == API_PASSWD:
                np.savetxt("report_test.csv", eval(str(request.data,'utf-8')), delimiter=",", fmt='%s')
                return 200

class Send_report_web(Resource):
    def post(self):
        if request.form.get('api-heslo') == API_PASSWD:
                file = request.files['file']
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], "report.csv"))
                    return 200
                else: return 400
        else:
            return 401
api.add_resource(Get, '/Get') #Funkcia vracia obsah pozadovanej tabulky
api.add_resource(Post, '/Post') # Funkcia si nahrá poslaný riadok do tabulky
api.add_resource(Log, '/Log') # Funkcia si nahrá poslaný log do tabulky
api.add_resource(Report, '/Report') # Pošle report.csv žiadateľovi
api.add_resource(Send_report, '/Send_report') # Pošle report.csv do server api
api.add_resource(Send_report_web, '/Send_report_web') # Pošle report.csv do server api
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5100)