# test_server.py

from flask import Flask, render_template, jsonify, request
import ReCalc as rc


app = Flask(__name__)

@app.route('/')
def index():
	return render_template("ReCalc.html")

@app.route('/_calc')
def evaluate_expression():
	exp = request.args.get('exp', "", type=str)

	return jsonify(result=rc.simplify(exp))

if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0')


