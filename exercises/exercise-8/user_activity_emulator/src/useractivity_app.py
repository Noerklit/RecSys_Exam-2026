import pandas as pd
import requests
from user_simulator import UserSimulator
from flask import Flask, render_template, request

app = Flask(__name__)

recommender_endpoint = 'http://my_recsys:5000'
feedback_endpoint = 'http://my_feedbackcollector:5000'
simulator = UserSimulator('../data/user_activity.bz2', recommender_endpoint, feedback_endpoint)

@app.route('/',  methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        pass
    if request.method == 'POST':
        # handle when the Start button in pushed
        if request.form['mybutton'] == 'Start':
            simulator.start()
        # handle when the Stop button in pushed
        elif request.form['mybutton'] == 'Stop':
            simulator.stop()
        else:
            pass
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0')

