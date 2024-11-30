from sqlalchemy import create_engine
from app.configs.config import DB_URL
from app.db.models import Base
from sqlalchemy.orm import sessionmaker
from app.db.data import employers_data, jobs_data, users_data, applications_data
from app.db.models import Employer, Jobs, User, JobsApplications
from argon2 import PasswordHasher


ph = PasswordHasher()
engine = create_engine(DB_URL)
conn = engine.connect()
Session = sessionmaker(bind=engine)

def prepare_database():
    from app.utils import hash_password
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    session = Session()

    for employer in employers_data:
        emp = Employer(**employer)
        session.add(emp)

    for jobs in jobs_data:
        jobs = Jobs(**jobs)
        session.add(jobs)

    for user in users_data:
        # user["password_hash"] = ph.hash(user.get("password"))
        user["password_hash"] = hash_password(user.get("password"))
        del user["password"]
        session.add(User(**user))
        
    for apps in applications_data:
        session.add(JobsApplications(**apps))

    session.commit()
