from app import app, database
from models.User import User
from models.Order import Order
from models.Status import Status

app.app_context().push()
database.create_all()
