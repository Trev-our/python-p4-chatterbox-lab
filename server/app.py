from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
migrate = Migrate(app, db)
CORS(app)

# GET all messages
@app.route("/messages", methods=["GET"])
def get_messages():
    messages = Message.query.order_by(Message.created_at.asc()).all()
    return jsonify([message.to_dict() for message in messages]), 200

# POST a new message
@app.route("/messages", methods=["POST"])
def create_message():
    data = request.get_json()

    try:
        new_message = Message(
            body=data["body"],
            username=data["username"]
        )
        db.session.add(new_message)
        db.session.commit()
        return jsonify(new_message.to_dict()), 201

    except Exception as e:
        return {"error": str(e)}, 400

# PATCH a message (update the body)
@app.route("/messages/<int:id>", methods=["PATCH"])
def update_message(id):
    message = db.session.get(Message, id)  # 👈 Replaces Message.query.get(id)
    if not message:
        return {"error": "Message not found"}, 404

    data = request.get_json()
    try:
        if "body" in data:
            message.body = data["body"]
        db.session.commit()
        return jsonify(message.to_dict()), 200

    except Exception as e:
        return {"error": str(e)}, 400

# DELETE a message
@app.route("/messages/<int:id>", methods=["DELETE"])
def delete_message(id):
    message = db.session.get(Message, id)  # 👈 Replaces Message.query.get(id)
    if not message:
        return {"error": "Message not found"}, 404

    try:
        db.session.delete(message)
        db.session.commit()
        return {}, 204

    except Exception as e:
        return {"error": str(e)}, 400

if __name__ == "__main__":
    app.run(port=5555, debug=True)