from pymongo import MongoClient


CELERY_BACKEND_URL = 'redis-14239.c212.ap-south-1-1.ec2.cloud.redislabs.com:14239'
CELERY_BROCKER_URL = 'redis-14239.c212.ap-south-1-1.ec2.cloud.redislabs.com:14239'

client = MongoClient('mongodb://localhost:27017/')
db = client['config']