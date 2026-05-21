from flask import Flask, request, jsonify
from surprise import dump
import logging

app = Flask(__name__)

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)


# IMPORTANT: Use the absolute path as discussed for Docker
model_path = '/models/model_SVD.pkl'
_, algo = dump.load(model_path)

@app.route("/", methods=["GET"])
def predict():
    # The simulator sends data in the request body
    data = request.form if request.form else request.json
    
    # Use .get() to avoid KeyErrors if the simulator hasn't started yet
    raw_u_id = data.get('userid')
    raw_i_id = data.get('itemid')
    
    if raw_u_id is None or raw_i_id is None:
        return jsonify({"error": "Missing data"}), 400
    
    # print("raw_u_id: ",raw_u_id)
    # print("raw_i_id: ", raw_i_id)
    
    u_id = int(float(raw_u_id))
    i_id = int(float(raw_i_id))
    
    # print("int_u_id: ",raw_u_id)
    # print("int_i_id: ", raw_i_id)

    prediction = algo.predict((u_id), (i_id))
    
    print("Prediction: ", prediction)
    
    # The simulator expects 'estimated_rating' as the key
    return jsonify({
        "estimated_rating": prediction.est
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)