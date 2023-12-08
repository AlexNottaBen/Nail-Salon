from app import app, database
from models.User import User
from models.Order import Order
from models.Status import Status

app.app_context().push()
database.create_all()

for status_name in ("scheduled", "working", "completed", "rejected"):
    status: Status = Status(status_name=status_name)
    database.session.add(status)
database.session.commit()
