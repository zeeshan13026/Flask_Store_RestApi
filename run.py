from code.app import app
from code.db import db

db.init_app(app)

@app.before_first_request
def create_table():
    db.create_all()