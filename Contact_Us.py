from flask import Flask, request, render_template, jsonify
import dbconnection


app = Flask(__name__)

@app.route('/user')  # decorator defines the
def user():
    return render_template('form.html')
