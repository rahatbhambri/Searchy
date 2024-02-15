from user_manager import User
from flask import request, Blueprint, render_template
from QaSystem import QASystem

views_bp = Blueprint('views', __name__)

qasys = QASystem()

@views_bp.route("/")
def hello_world():
    return render_template('index.html' )

@views_bp.route("/createUser", methods =['POST'])
def create_user():
    data = request.json
    User(data.get("username", ""), data.get("email", ""))
    return "User added successfully"

@views_bp.route("/setTopic", methods = ["POST"]) 
def setTopic():
    data = request.json
    if data.get("topic", None):
        qasys.SetContext(data.get("topic"))
        return "Topic set successfully"
    else:
        return "Not a valid topic"

@views_bp.route("/answer", methods = ["GET"])
def getAnswer():
    question = request.args.get('question')
    return qasys.getAnswer(question)