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