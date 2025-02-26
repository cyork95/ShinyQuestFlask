from app import app, db
from models import User, Pokemon, Hunt
from sqlalchemy import inspect

with app.app_context():
    db.create_all()
    inspector = inspect(db.engine)
    print("Database created with tables:", inspector.get_table_names())