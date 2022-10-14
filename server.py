#pip install flask
#pip install flask-sqlalchemy
#pip install flask-restful
#pip install mysqlclient
#Odporúčam testovať cez PostMan-a
#SSL bude riešené až v WSGI spolu s apache / NGIX
from flask import Flask, request,jsonify,make_response
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy

#vytvorí inštanciu Flasku
app = Flask(__name__)
# Vytvorí api objekt
api = Api(app)

#Vytvorí databázu
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@127.0.0.1/test'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#SQL alchemy inštancia
db = SQLAlchemy(app)

# Definicia pracovnika
class Pracovnik(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    meno = db.Column(db.String(80), nullable=False)
    priezvisko = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        return f"{self.meno} - {self.priezvisko}"


#Beží ako post a autentifikácia je cez json "api-heslo" s heslom "
class Get(Resource):
    def post(self):
        if request.is_json:

            if(request.json['api-heslo']=="YouWontGuessThisOne"):
                employees = Pracovnik.query.all()
                emp_list = []
                for emp in employees:
                    emp_data = {'Id': emp.id, 'Meno': emp.meno, 'Priezvisko': emp.priezvisko}
                    emp_list.append(emp_data)
                return {"Všetci pracovníci": emp_list}, 200
        else:
            return {'error': 'Formát musí byť JSON'}, 400

# Bude bezat na /pridat - táto funkcia v skutocnosti nie je potrebna,
# pretože potrebujeme iba get, pridavanie pojde cez php my admin
class Pridať(Resource):
    def post(self):
        if request.is_json:
            emp = Pracovnik(meno=request.json['meno'], priezvisko=request.json['priezvisko'])
            db.session.add(emp)
            db.session.commit()
            # vrátim json odpoveď
            return make_response(jsonify({'id': emp.id, 'meno': emp.meno, 'priezvisko': emp.priezvisko}), 201)
        else:
            return {'error': 'Formát musí byť JSON'}, 400

api.add_resource(Get, '/')
api.add_resource(Pridať, '/pridat') # do buducna zmazať
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5100)
