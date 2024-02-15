from flask import Flask
from views import views_bp

app = Flask(__name__)
app.register_blueprint(views_bp)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

