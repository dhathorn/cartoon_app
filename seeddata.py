import cartoon_app
import datetime
from cartoon_app import models, db

cartoon_app.app.test_request_context().push()
db.drop_all()
db.create_all()

db.session.add(models.User("dmhathorn@gmail.com", "testtesttest"))
db.session.commit()
