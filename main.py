from flask import Flask, request, render_template, jsonify
import dbconnection


app = Flask(__name__)

@app.route("/")
def test():
    table_name = dbconnection.db["accounts"]
    single_record = table_name.find_one()
    # return jsonify(message=single_record)
    return render_template("home.html", data = single_record)


if __name__ == '__main__':
    app.run()