from flask import Flask, request, render_template, jsonify
import dbconnection


app = Flask(__name__)

@app.route("/")
def test():
    collection_name = dbconnection.db["admins"]
    single_record = collection_name.find_one()
    # return jsonify(message=single_record)
    # mydict = {"name": "John Doe", "email": "johndoe@gmail.com", "password" : "john123"}

    # x = collection_name.insert_one(mydict)
    # print(x)
    return render_template("home.html", data = single_record)


if __name__ == '__main__':
    app.run()