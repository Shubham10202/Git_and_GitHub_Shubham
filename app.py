from flask import Flask, jsonify, request
import json
from pymongo import MongoClient

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello from Shubham's Flask App!"

@app.route("/api")
def api():
    with open("data.json", "r") as file:
        data = json.load(file)
    return jsonify(data)

@app.route("/submittodoitem", methods=["POST"])
def submit_todo_item():
    data = request.get_json()

    item_name = data.get("itemName")
    item_description = data.get("itemDescription")

    if not item_name or not item_description:
        return jsonify({
            "error": "itemName and itemDescription are required"
        }), 400

    client = MongoClient("mongodb://localhost:27017/")
    db = client["todo_database"]
    collection = db["todo_items"]

    result = collection.insert_one({
        "itemName": item_name,
        "itemDescription": item_description
    })

    return jsonify({
        "message": "Todo item saved successfully",
        "id": str(result.inserted_id)
    }), 201

if __name__ == "__main__":
    app.run(debug=True)
