from QAsystem.QaSystem import QASystem

class User:
    def __init__(self, username, email):
        self.username = username
        self.email = email 
        self.qasys = QASystem()
        