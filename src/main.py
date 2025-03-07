from flask import Flask
from app.views import views_bp
from celery import Celery
from flask_cors import CORS
from config.settings import CELERY_BACKEND_URL, CELERY_BROCKER_URL


app = Flask(__name__)
CORS(app)
app.register_blueprint(views_bp)
app.config['CELERY_BROKER_URL'] = CELERY_BROCKER_URL
app.config['CELERY_BACKEND_URL'] = CELERY_BACKEND_URL



celery = Celery(app.name, backend= app.config['CELERY_BACKEND_URL'], broker=app.config['CELERY_BROKER_URL'])

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)


