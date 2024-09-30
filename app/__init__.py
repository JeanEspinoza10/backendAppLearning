from flask import Flask
from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_seeder import FlaskSeeder
from datetime import timedelta
import os

load_dotenv()
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=int(os.getenv('JWT_ACCESS_TOKEN_EXPIRES')))
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(minutes=int(os.getenv('JWT_REFRESH_TOKEN_EXPIRES')))


db = SQLAlchemy(app)
migrate = Migrate(app, db)
CORS(app)

authorizations = {
    'Bearer': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization'
    }
}

api = Api(
    app,
    title='App Learning Ingles',
    version='0.1',
    description='Endpoints',
    authorizations=authorizations,
    doc='/swagger-ui'
)

jwt = JWTManager(app)
seeder = FlaskSeeder(app, db)