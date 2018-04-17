# server_for_ReCalc.py

import flask
from flask import Flask, request
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def handle_requests(data ="pineapple"):
	datafromjs = request.form['mydata']
	return(datafromjs)
