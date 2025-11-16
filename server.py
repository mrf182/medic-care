
from flask import Flask
from flask_cors import CORS
from app.routes import routes

app = Flask(__name__, static_folder="app/static", template_folder="app/templates")
app.secret_key = 'your_secret_key_here'
CORS(app)

app.register_blueprint(routes)

if __name__ == '__main__':
    app.run(port=3000, debug=True)
