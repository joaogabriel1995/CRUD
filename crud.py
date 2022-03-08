from flask import Flask
from models.produtos import db
from controler.produtos import app as produto_controler

app = Flask(__name__, template_folder="templates", static_folder="static")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///gti.sqlite3'

app.register_blueprint(produto_controler, url_prefix="/")


if __name__ == "__main__":
    db.init_app(app=app)
    with app.test_request_context():
        db.create_all()
    app.run(debug=True)
