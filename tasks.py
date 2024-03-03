from celery import Celery
celery = Celery(__name__)


@celery.task
def add_chat_to_db(session_id = "123", question = "", answer =""):
    print(session_id, question, answer)
    pass