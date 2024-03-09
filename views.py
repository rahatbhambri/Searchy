from user_manager import User
from flask import request, Blueprint, render_template
from QaSystem import QASystem
from tasks import add_chat_to_db
from settings import db
from datetime import datetime as dt

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


@views_bp.route("/answer", methods = ["GET"])
def getAnswer():
    data = {}
    curr_data =  dict(request.args)
    question = curr_data.get('question')
    session_id = int(curr_data.get('session_id'))
    user_id = curr_data.get('user_id')
    print(curr_data)
        
    data['answer'], data['img'] = qasys.getAnswer(question)
    payl = {
        'session_id' : session_id,
        'user_id' : user_id, 
        'timestamp' : dt.now(), 
        'question' : question, 
        'img' : data['img'], 
        'answer' : data['answer']   
    }
    db.chats.insert_one(payl)
    #result = add_chat_to_db(question=question, answer=data["answer"]).delay()
    return data


@views_bp.route("/get_chats", methods = ["GET"])
def getChats():
    user_id = str(request.args.get('user_id'))
    session_id = int(request.args.get('session_id'))

    data = list(db.chats.find({'user_id' : user_id, 'session_id' : session_id}, 
                              {'user_id' : 0, 'session_id' : 0, '_id' : 0}))
    #print(data, user_id, session_id) 
    return data 


@views_bp.route("/get_user", methods = ["GET"])
def getUserData():
    user_id = str(request.args.get('user_id'))
    data = db.users.find_one({'user_id' : user_id}, 
                              {'user_id' : 0, '_id' : 0})
    #print(data, user_id, session_id) 
    return data.get("sessions", []) 



@views_bp.route("/set_session", methods = ["POST"])
def setSession():
    data = request.json 
    session = data["session"]
    user_id = data["user_id"]
    
    print(session)
    db.users.find_one_and_update({'user_id' : user_id},
                                 {"$set" : {"sessions": session}}
                                 )
    return "POST successfull"
    
    

# @views_bp.route("/setTopic", methods = ["POST"]) 
    # def setTopic():
    #     data = request.json
    #     if data.get("topic", None):
    #         qasys.SetContext(data.get("topic"))
    #         return "Topic set successfully"
    #     else:
    #         return "Not a valid topic"

