from flask import Flask, request, jsonify
from prometheus_client import start_http_server, Gauge, make_wsgi_app
from werkzeug.middleware.dispatcher import DispatcherMiddleware
import numpy as np
import os
import pandas as pd
import logging

app = Flask(__name__)
errors = []

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)
user_list = set()

gauge_rmse = Gauge('rmse', 'Tracks average error')
gauge_users = Gauge('unique_users', 'Tracks number of unique users that have provided a score')

# Add prometheus wsgi middleware to route /metrics requests 
# taken from: https://prometheus.github.io/client_python/exporting/http/flask/
# This should simply make a /metrics endpoint on whatever port the application is running on, so 5000/metrics in this case
app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {
    '/metrics': make_wsgi_app()
})

@app.route("/", methods=["GET"])
def collect():
    # Extracting from request.form because 'requests.get(url, data=...)' 
    # places data in the body, not args.
    data = request.form
    
    # Data is floats for some reason, fetch them based on the name the simulator sends them with
    user_id = float(data.get('userid'))
    actual_rating = float(data.get('rating'))
    est_rating = float(data.get('estimated_rating'))
    
    # Keep track in memory
    # Calculation of rmse based on: https://stackoverflow.com/questions/21926020/how-to-calculate-rmse-using-ipython-numpy
    error_sq = (actual_rating - est_rating) ** 2
    errors.append(error_sq)
    rmse = np.sqrt(np.mean(errors))
    user_list.add(user_id)
    
    # Update gauges everytime a request has been gathered
    gauge_rmse.set(rmse)
    gauge_users.set(len(user_list))
    # Save to Volume
    log_path = "../data/feedback.csv"
    pd.DataFrame([data]).to_csv(log_path, mode='a', index=False, header=not os.path.exists(log_path))
    
    # Print to verify it works in the logs of the container
    print(f"Update: RMSE is {rmse:.4f}")
    return jsonify({"status": "ok", "rmse": rmse})

if __name__ == '__main__':
    # start_http_server(9000)
    app.run(host='0.0.0.0', port=5000)
        