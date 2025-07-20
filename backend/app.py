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
            k.vorname,
            k.nachname,
            a.Datum,
            a.Gesamtpreis,
            p.Produkt_Nr,
            p.Produktname,
            i.Produkt_Anzahl,
            i.Produktgröße
        FROM auftrag a
        JOIN kunde k ON a.kunden_Nr = k.Kunden_Nr
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
                "vorname": row["vorname"],
                "nachname": row["nachname"],
                "Datum": row["Datum"].strftime("%Y-%m-%d"),
                "Gesamtpreis": row["Gesamtpreis"],
                "produkte": []
            }
        if row["Produkt_Nr"]:
            auftraege[nr]["produkte"].append({
                "Produkt_Nr": row["Produkt_Nr"],
                "Produktname": row["Produktname"],
                "Produkt_Anzahl": row["Produkt_Anzahl"],
                "Produktgröße": row["Produktgröße"]
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

@app.route('/api/anzahl_auftrag', methods=['POST'])
def anzahl_auftrag():
    data = request.get_json()
    vorname = data.get('vorname')
    nachname = data.get('nachname')

    if not vorname or not nachname:
        return jsonify({"error": "Vorname und Nachname erforderlich"}), 400
    
    result = db.session.execute(db.text("""
        SELECT COUNt(a.Auftrag_Nr) AS anzahl,
                COALESCE(SUM(a.Gesamtpreis), 0) AS umsatz
        FROM auftrag a
        JOIN kunde k ON a.kunden_Nr = k.Kunden_Nr
        WHERE k.vorname = :vorname AND k.nachname = :nachname
    """), {"vorname": vorname, "nachname": nachname}).mappings().first()

    return jsonify({"anzahl": result["anzahl"], "umsatz": result["umsatz"]})

@app.route('/api/get_kunde_by_auftrag', methods=['POST'])
def get_kunde_by_auftrag():
    data = request.get_json()
    Auftrag_Nr = data.get('Auftrag_Nr')

    result = db.session.execute(db.text("""
        SELECT k.vorname, k.nachname
        FROM auftrag a
        LEFT JOIN kunde k ON a.kunden_Nr = k.Kunden_Nr
        WHERE a.Auftrag_Nr = :Auftrag_Nr
    """), {"Auftrag_Nr": Auftrag_Nr}).fetchone()

    if result is not None:
        return jsonify({"vorname": result[0], "nachname": result[1]})
    else:
        return jsonify({"message": "Kein Kunde zu dieser Auftragsnummer gefunden"}), 404

@app.route('/api/produkt_order', methods=['POST'])
def produkt_order():
    data = request.get_json()
    produktname = data.get('produktname')
    print(produktname)
    if not produktname:
        return jsonify({"error": "Produktname erforderlich"}), 400

    result = db.session.execute(db.text("""
        SELECT COUNT(*) FROM ist_teil_von i
        JOIN produkt p ON i.produkt_Nr = p.produkt_Nr
        WHERE p.Produktname = :produktname
    """), {"produktname": produktname}).scalar()

    return jsonify({"anzahl": result})

@app.route('/api/produkte_monat', methods=['POST'])
def produkte_im_monat():
    data = request.get_json()
    monat = data.get('monat')

    if not monat:
        return jsonify({"error": "Monat erforderlich"}), 400

    result = db.session.execute(db.text("""
        SELECT p.Produktname, SUM(i.produkt_Anzahl) AS anzahl
        FROM Produkt p
        JOIN ist_teil_von i ON p.produkt_Nr = i.produkt_Nr
        JOIN Auftrag a ON i.auftrag_Nr = a.auftrag_Nr
        WHERE DATE_FORMAT(a.Datum, '%Y-%m') = :monat
        GROUP BY p.Produktname
    """), {"monat": monat}).mappings().all()

    return jsonify([dict(row) for row in result])

@app.route('/api/unbestellte_produkte', methods=['GET'])
def unbestellte_produkte():
    result = db.session.execute(db.text("""
        SELECT p.produktname
        FROM Produkt p
        LEFT JOIN ist_teil_von ap ON p.produkt_Nr = ap.produkt_Nr
        WHERE ap.produkt_Nr IS NULL;
    """)).scalars().all()

    return jsonify([{"produktname": name} for name in result])

@app.route('/api/produkte_together', methods=['POST'])
def produkte_together():
    data = request.get_json()
    p1 = data.get('produktnameA')
    p2 = data.get('produktnameB')

    if not p1 or not p2:
        return jsonify({"error": "Beide Produktnamen erforderlich"}), 400

    result = db.session.execute(db.text("""
        SELECT COUNT(*) AS gemeinsame_bestellungen
        FROM (
            SELECT i.auftrag_Nr
            FROM ist_teil_von i
            JOIN produkt p ON i.produkt_Nr = p.produkt_Nr
            WHERE p.Produktname IN (:p1, :p2)
            GROUP BY i.auftrag_Nr
            HAVING COUNT(DISTINCT p.Produktname) = 2
        ) AS gemeinsame
    """), {"p1": p1, "p2": p2}).scalar()

    return jsonify({"anzahl": result})

@app.route('/api/auftrag_hinzufuegen', methods=['POST'])
def auftrag_hinzufuegen():
    data = request.get_json()
    kundenNr = data.get('kundenNr')
    datum = data.get('datum')
    gesamtpreis = data.get('gesamtpreis')
    produkte = data.get('produkte', [])

    if not all([kundenNr, datum, gesamtpreis, produkte]):
        return jsonify({"message": "Alle Felder erforderlich"}), 400

    result = db.session.execute(db.text("""
        INSERT INTO auftrag (kunden_Nr, Datum, Gesamtpreis)
        VALUES (:kundenNr, :datum, :gesamtpreis)
    """), {"kundenNr": kundenNr, "datum": datum, "gesamtpreis": gesamtpreis})

    auftrag_id = db.session.execute(db.text("""SELECT LAST_INSERT_ID()""")).scalar()

    for p in produkte:
        db.session.execute(db.text("""
            INSERT INTO ist_teil_von (auftrag_Nr, produkt_Nr, Produkt_Anzahl, Produktgröße)
            VALUES (:auftrag, :produkt, :anzahl, :groesse)
        """), {"auftrag": auftrag_id, "produkt": p["produktNr"], "anzahl": p["menge"], "groesse": p["groesse"]})

    db.session.commit()
    return jsonify({"message": "Bestellung erfolgreich hinzugefügt"}), 201

@app.route('/api/produkt_add', methods=['POST'])
def produkt_add():
    data = request.get_json()
    name = data.get('name')

    if not name:
        return jsonify({"message": "Produktname erforderlich"}), 400

    db.session.execute(db.text("""
        INSERT INTO produkt (Produktname)
        VALUES (:name)
    """), {"name": name})

    db.session.commit()
    return jsonify({"message": "Produkt erfolgreich hinzugefügt"}), 201

# Information
@app.route('/api/dsgvo_information', methods=['POST'])
def dsgvo_information():
    data = request.get_json()
    vorname = data.get('vorname')
    nachname = data.get('nachname')

    result = db.session.execute(db.text("""
        SELECT k.Kunden_Nr, k.Vorname, k.Nachname, a.Stra_e, a.Haus_Nr, a.PLZ, a.Ort
        FROM kunde k
        JOIN adresse a ON k.Adress_Nr = a.Adress_Nr
        WHERE k.Vorname = :vorname AND k.Nachname = :nachname
    """), {'vorname': vorname, 'nachname': nachname}).mappings().fetchone()

    if result:
        return jsonify(dict(result))
    else:
        return jsonify({"message": "Kunde nicht gefunden"}), 404

# delet
@app.route('/api/dsgvo_delet', methods=['POST'])
def dsgvo_delet():
    data = request.get_json()
    vorname = data.get('vorname')
    nachname = data.get('nachname')

    # 1. Search for customers by first and last name
    kunde = db.session.execute(db.text("""
        SELECT * FROM kunde WHERE Vorname = :vor AND Nachname = :nach
    """), {'vor': vorname, 'nach': nachname}).mappings().fetchone()

    if not kunde:
        return jsonify({"message": "Kunde nicht gefunden"}), 404

    kundenNr = kunde['Kunden_Nr']
    adressNr = kunde['Adress_Nr']
 
    # 2. Check if orders are < 10 years old
    bestellungen = db.session.execute(db.text("""
        SELECT COUNT(*) AS anz FROM auftrag
        WHERE kunden_Nr = :id AND Datum >= DATE_SUB(CURDATE(), INTERVAL 10 YEAR)
    """), {'id': kundenNr}).mappings().fetchone()

    if bestellungen['anz'] > 0:
        db.session.execute(db.text("""
            UPDATE kunde SET Vorname = 'Anonymisiert', Nachname = 'Anonymisiert'
            WHERE Kunden_Nr = :id
        """), {'id': kundenNr})
        db.session.commit()
        return jsonify({"message": "Kunde anonymisiert wegen aktiver Aufträge"}), 200

    # 3. Check address
    adress_verwendung = db.session.execute(db.text("""
        SELECT COUNT(*) AS anz FROM kunde
        WHERE Adress_Nr = :adr AND Kunden_Nr != :id
    """), {'adr': adressNr, 'id': kundenNr}).mappings().fetchone()

    # 4. Delete orders + customer
    db.session.execute(db.text("""
        DELETE FROM ist_teil_von WHERE auftrag_Nr IN (
            SELECT Auftrag_Nr FROM auftrag WHERE kunden_Nr = :id
        )
    """), {'id': kundenNr})
    db.session.execute(db.text("DELETE FROM auftrag WHERE kunden_Nr = :id"), {'id': kundenNr})
    db.session.execute(db.text("DELETE FROM kunde WHERE kunden_Nr = :id"), {'id': kundenNr})
 
    # 5. Delete address if no longer used
    if adress_verwendung['anz'] == 0:
        db.session.execute(db.text("DELETE FROM adresse WHERE Adress_Nr = :adr"), {'adr': adressNr})

    db.session.commit()
    return jsonify({"message": "Kunde und zugehörige Daten gelöscht"}), 200

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
