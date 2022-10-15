from flask import Flask, request,session 
#  ,abort 
from models import db, User
from config import ApplicationConfig
from flask_bcrypt import Bcrypt
from flask.json import jsonify
from flask_session import Session
from flask_cors import CORS, cross_origin
import logging

logging.basicConfig(filename='../log/log.log', filemode='a',encoding='utf-8', level=logging.DEBUG)


app = Flask(__name__)
app.config.from_object(ApplicationConfig)

bcrypt = Bcrypt(app)
CORS(app, supports_credentials=True)
server_session = Session(app)
db.init_app(app)

with app.app_context():
    db.create_all()


@app.route("/register", methods=["POST"])
def register_user():
    try:
        email = request.json["email"]
        password = request.json["password"]
        first_name = request.json["first_name"]
        last_name = request.json["last_name"]
        user_role="normal"
        user_exists = User.query.filter_by(email=email).first() is not None

        if user_exists:
            return jsonify({"success":False,"error": "User Already Exists"}), 409
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        
        new_user = User(email=email, password=hashed_password,first_name=first_name,last_name=last_name,user_role=user_role)
        db.session.add(new_user)
        db.session.commit()
        session["user_id"] = new_user.id
        session["user_role"] = new_user.user_role
        return jsonify({
            "success": True,
            "id": new_user.id,
            "email": new_user.email,
            "user_role":new_user.user_role,
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        })


@app.route("/@me",methods=["POST"])
def get_current_user():
    
    try:
        user_id = session.get("user_id")
        if not user_id:
            return jsonify({"success": False,"error": "Unauthorized"}), 401
        
        user = User.query.filter_by(id=user_id).first()
        return jsonify({
            "success": True,
            "id": user.id,
            "email": user.email
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        })


@app.route('/login', methods=["POST"])
def login_user():
    try:
        email = request.json["email"]
        password = request.json["password"]
        user = User.query.filter_by(email=email,).first()

        if user is None:
            return jsonify({"success": False, "error": "Unauthorized"}), 401

        if not bcrypt.check_password_hash(user.password, password):
            return jsonify({"success": False, "error": "Unauthorized"}), 401

        session["user_id"] = user.id

        # session["user_id"] = user.id
        return jsonify({
            "success": True,
            "id": user.id,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        })

@app.route('/logout',methods=["POST"])
def logout_user():
    try:
        session.pop("user_id")
        return jsonify({
            "success": True
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        })

@app.route('/dashboard',methods=["POST"])
def dashboard():
    try:
        user_id = session.get("user_id")
        user_role = session.get("user_role")
        
        if not user_id :
            return jsonify({"error": "Unauthorized"}), 401
        if user_role == "normal":
            return jsonify({"error": "Unauthorized"}), 401
        
        user = User.query.filter_by(id=user_id).first()
        return jsonify({
            "id": user.id,
            "email": user.email,
            "user_role": user.user_role,
            
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        })

if __name__ == '__main__':
    app.run(debug=True)
