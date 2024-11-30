from app.db.models import Jobs, Employer
from graphene import Mutation, String, Int, Field, ObjectType, Boolean
from app.gql.types import JobObject
from app.db.database import Session

class AddJob(Mutation):
    class Arguments:
        title = String()
        description = String()
        employer_id = Int()
    jobs = Field(lambda: JobObject)

    @staticmethod
    def mutate(root, info, title, description, employer_id):
        job = Jobs(title=title, description=description, employer_id=employer_id)
        with Session() as s:
            s.add(job)
            s.commit()
        return AddJob(jobs=job)

class UpdateJob(Mutation):
    class Arguments:
        job_id = Int(required=True)
        title = String()
        description = String()
        employer_id = Int()
    
    job = Field(JobObject)
    @staticmethod
    def mutate(root, info, job_id, title=None, description=None, employer_id=None):
        session = Session()
        curr_job = session.query(Jobs).filter(Jobs.id==job_id).first()
        if not curr_job:
            raise Exception("Record Does not exist's")
        
        if title is not None:
            curr_job.title = title
        if description is not None:
            curr_job.description = description
        if employer_id is not None:
            curr_job.employer_id = employer_id
        
        session.commit()
        session.refresh(curr_job)
        session.close()
        return UpdateJob(job=curr_job)
    

class DeleteJob(Mutation):
    class Arguments:
        id = Int(required=True)
    
    success = Boolean()
    
    @staticmethod
    def mutate(root, info, id):
        with Session() as s:
            curr = s.query(Jobs).filter(Jobs.id == id).first()
            if not curr:
                raise Exception("Does not exist's")
            s.delete(curr)
            s.commit()
        return DeleteJob(success=True)