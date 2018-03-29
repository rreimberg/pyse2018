
from sample.app import celery, db
from sample.models import User


@celery.task(name='save_on_database', queue='save-on-database')
def save_on_database(uuid, name, email):
    user = User(
        uuid=uuid,
        name=name,
        email=email,
    )

    db.session.add(user)
    db.session.commit()
