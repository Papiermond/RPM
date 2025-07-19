
@app.route('/api/get_customer', methods=['POST'])
def submit():
    data = request.get_json()
    input_value = data.get('value')
    print(f"Received from frontend: {input_value}")
   
    return jsonify({"status": "received", "value": input_value})