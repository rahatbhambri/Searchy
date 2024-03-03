from flask import Flask
from celery import Celery
from views import views_bp

app = Flask(__name__)
app.register_blueprint(views_bp)
app.config['CELERY_BROKER_URL'] = 'redis-14239.c212.ap-south-1-1.ec2.cloud.redislabs.com:14239'

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)



if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)


