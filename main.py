from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_pyfile("config.py")

#instancia do db com SQLAlchemy
db = SQLAlchemy(app)

from views.views import  *
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8080)