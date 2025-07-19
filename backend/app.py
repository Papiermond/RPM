from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import pymysql
from sqlalchemy import text

pymysql.install_as_MySQLdb()

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root@localhost/test1'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

Kunde = None
adresse = None
auftrag = None
produkt = None
ist_teil_von = None


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

@app.route('/api/produkte')
def get_produkt():
    daten = produkt.query.all()
    return jsonify([
        {col: getattr(s, col) for col in s.__table__.columns.keys()}
        for s in daten
    ])

@app.route('/api/ist_teil_von')
def get_ist_teil_von():
    result = db.session.execute("SELECT * FROM ist_teil_von")
    daten = [dict(row) for row in result.mapping()]
    return jsonify(daten)

@app.route('/api/kunde_with_adresse')
def kunde_with_adresse():
    result = db.session.execute(text("""
        SELECT
            k.Kunden_Nr, k.vorname, k.nachname,
            a.stra_e, a.Haus_Nr, a.plz, a.ort
            From kunde k
            JOIN adresse a ON k.adress_Nr = a.adress_Nr
    """))
    daten = [dict(row) for row in result.mappings()]
    return jsonify(daten)

@app.route('/api/auftraege')
def get_auftraege():
    sql = text("""
        SELECT
            a.Auftrag_Nr,
            a.kunden_Nr,
            a.Datum,
            a.Gesamtpreis,
            p.Produkt_Nr,
            p.Produktname
        FROM auftrag a
        LEFT JOIN ist_teil_von i ON a.Auftrag_Nr = i.Auftrag_Nr
        LEFT JOIN produkt p ON i.produkt_Nr = p.produkt_Nr
        ORDER BY a.Auftrag_Nr
    """)
    result = db.session.execute(sql).mappings().all()

    auftraege = {}
    for row in result:
        nr = row["Auftrag_Nr"]
        if nr not in auftraege:
            auftraege[nr] = {
                "Auftrag_Nr": nr,
                "kunden_Nr": row["kunden_Nr"],
                "Datum": row["Datum"].strftime("%Y-%m-%d"),
                "Gesamtpreis": row["Gesamtpreis"],
                "produkte": []
            }
        if row["Produkt_Nr"]:
            auftraege[nr]["produkte"].append({
                "Produkt_Nr": row["Produkt_Nr"],
                "Produktname": row["Produktname"]
            })
            
    return jsonify(list(auftraege.values()))

@app.route('/api/get_KundenNr', methods=['POST'])
def get_KundenNr():
    data = request.get_json()
    vorname = data.get('vorname')
    nachname = data.get('nachname')

    if not vorname or not nachname:
        return jsonify({"error": "Vor- und Nachname erforderlich"}), 400
    
    kunde = db.session.execute(
        db.text("SELECT Kunden_Nr FROM kunde WHERE vorname = :vorname AND nachname = :nachname"),
        {"vorname": vorname, "nachname": nachname}
    ).fetchone()

    if kunde:
        return jsonify({"Kunden_Nr": kunde[0]})
    else:
        return jsonify({"message": "Kein Kunde gefunden"}), 404

@app.route('/api/get_StAndOrt', methods=['POST'])
def get_StAndOrt():
    data = request.get_json()
    st = data.get('stra_e')
    ort = data.get('ort')

    if not st or not ort:
        return jsonify({"error": "Straße und Ort erforderlich"}), 400
    
    result = db.session.execute(
        db.text("""
            SELECT COUNT(*) 
            FROM kunde k
            JOIN adresse a ON k.adress_Nr = a.adress_Nr
            WHERE a.Stra_e = :st AND a.Ort = :ort
        """),
        {"st": st, "ort": ort}
    ).scalar()

    return jsonify({"anzahl": result})

@app.route('/api/ort_max', methods=['GET'])
def ort_max():
    result = db.session.execute(db.text("""
        SELECT a.ort, COUNT(*) as anzahl
        FROM kunde k
        JOIN adresse a ON k.adress_Nr = a.adress_Nr
        GROUP BY a.ort
        ORDER BY anzahl DESC
        LIMIT 1
    """)).fetchone()

    return jsonify({"ort": result[0], "anzahl": result[1]})


if __name__ == '__main__':
    with app.app_context():

        class Kunde(db.Model):
            __tablename__ = 'kunde'
            __table_args__ = {'autoload_with': db.engine}

        class adresse(db.Model):
            __tablename__ = 'adresse'
            __table_args__ = {'autoload_with': db.engine}

        class auftrag(db.Model):
            __tablename__ = 'auftrag'
            __table_args__ = {'autoload_with': db.engine}

        class produkt(db.Model):
            __tablename__ = 'produkt'
            __table_args__ = {'autoload_with': db.engine}

        class ist_teil_von(db.Model):
            __tablename__ = 'ist_teil_von'
            auftrag_Nr = db.Column(db.Integer, primary_key=True)
            produkt_Nr = db.Column(db.Integer, primary_key=True)
            anzahl = db.Column(db.Integer)

        app.run(debug=True)
