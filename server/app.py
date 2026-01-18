# server/app.py

from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

# Initialize app
app = Flask(__name__)
CORS(app)  # Enable CORS so React can fetch from Flask

# Configure database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chatterbox.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Models
class Message(db.Model):
    __tablename__ = 'messages'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    body = db.Column(db.String(500), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "body": self.body
        }

# Routes
@app.route("/messages", methods=["GET"])
def get_messages():
    messages = Message.query.all()
    return jsonify([msg.to_dict() for msg in messages])

@app.route("/messages", methods=["POST"])
def create_message():
    data = request.get_json()
    username = data.get("username")
    body = data.get("body")
    if not username or not body:
        return jsonify({"error": "username and body required"}), 400

    message = Message(username=username, body=body)
    db.session.add(message)
    db.session.commit()
    return jsonify(message.to_dict()), 201

# Run app
if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Create tables inside app context
    app.run(port=5555, debug=True)
