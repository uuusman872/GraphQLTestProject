from sqlalchemy import Column, Integer, String as saString, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Employer(Base):
    __tablename__ = "employer"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(saString)
    contact_email = Column(saString)
    industry = Column(saString)
    jobs = relationship("Jobs", back_populates="employer")  # Corrected back_populates


class Jobs(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(saString)
    description = Column(saString)
    employer_id = Column(Integer, ForeignKey("employer.id"))
    employer = relationship("Employer", back_populates="jobs", lazy="joined")
    applications = relationship("JobsApplications", back_populates="job", lazy="joined")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(saString)
    email = Column(saString)
    password_hash = Column(saString)
    role = Column(saString)
    applications = relationship("JobsApplications", back_populates="user", lazy="joined")


class JobsApplications(Base):
    __tablename__ = "job_applications"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    job_id = Column(Integer, ForeignKey("jobs.id"))
    user = relationship("User", back_populates="applications", lazy="joined")
    job = relationship("Jobs", back_populates="applications", lazy="joined")
