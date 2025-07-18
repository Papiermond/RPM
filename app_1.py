from flask import Flask, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import pymysql

pymysql.install_as_MySQLdb()

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root@localhost/test1'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Initial leer lassen
Kunde = None
adresse = None
auftrag = None


@app.route('/api/kunde')
def get_kunde():
    daten = Kunde.query.all()
    return jsonify([
        {col: getattr(s, col) for col in s.__table__.columns.keys()}
        for s in daten
    ])

@app.route('/api/adresse')
def get_adresse():
    daten = adresse.query.all()
    return jsonify([
        {col: getattr(s, col) for col in s.__table__.columns.keys()}
        for s in daten
    ])

@app.route('/api/auftrag')
def get_auftrag():
    daten = auftrag.query.all()
    return jsonify([
        {col: getattr(s, col) for col in s.__table__.columns.keys()}
        for s in daten
    ])

@app.route('/api/data')
def get_data():
    return jsonify({"message": "Hello from Data"})

@app.route('/api/auth')
def get_auth():
    return jsonify({"message": "Hello from Authentication"})

@app.route('/api/expo')
def get_expoerter():
    return jsonify({"message": "Hello from exporter"})

@app.route('/api/download')
def get_downloader():
    return jsonify({"message": "Hello from download"})

if __name__ == '__main__':
    with app.app_context():
        # Jetzt ist Flask-Kontext aktiv → JETZT darfst du das Model definieren
        class Kunde(db.Model):
            __tablename__ = 'kunde'
            __table_args__ = {'autoload_with': db.engine}
        # Jetzt darfst du den Server starten
        app.run(debug=True)
