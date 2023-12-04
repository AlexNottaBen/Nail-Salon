from app import app, database
from models.User import User

app.app_context().push()
database.create_all()
