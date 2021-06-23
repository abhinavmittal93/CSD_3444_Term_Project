from flask import Flask, request, render_template, jsonify
import dbconnection


app = Flask(__name__)

@app.route('/user')
def user():
    return render_template('form.html')






