from app.db.models import Jobs, Employer
from graphene import Mutation, String, Int, Field, ObjectType, Boolean
from app.gql.types import EmployerObject
from app.db.database import Session

import jwt
from app.configs.config import ALGORITUM, SECRET_KEY


import pdb
from app.utils import get_authenticated_user


class AddEmployer(Mutation):
    class Arguments:
        name = String()
        contact_email = String()
        industry = String()

    employer = Field(EmployerObject)
    authenticated_as = Field(String)
    @staticmethod
    def mutate(root, info, name, contact_email, industry):
        emp = Employer(name=name, contact_email=contact_email, industry=industry)
        user = get_authenticated_user(info.context)
        with Session() as s:
            s.add(emp)
            s.commit()
            s.refresh(emp)
        return AddEmployer(employer=emp, authenticated_as=user.email)


class UpdateEmployer(Mutation):
    class Arguments:
        emp_id = Int(required=True)
        name = String()
        contact_email = String()
        industry = String()

    employer = Field(EmployerObject)
    @staticmethod
    def mutate(root, info, emp_id, name, contact_email, industry):
        with Session() as s:
            curr_emp = s.query(Employer).filter(Employer.id == emp_id).first()
            if not curr_emp:
                raise Exception("Emp Does not exist's")
            if name is not None:
                curr_emp.name = name
            if contact_email is not None:
                curr_emp.contact_email = contact_email
            if industry is not None:
                curr_emp.industry = industry
            s.commit()
            s.refresh(curr_emp)
        return UpdateEmployer(curr_emp)

class DeleteEmployer(Mutation):
    class Arguments:
        id = Int(required=True)
    
    success = Boolean()
    @staticmethod
    def mutate(root, info, id):
        with Session() as s:
            curr_emp = s.query(Employer).filter(Employer.id == id).first()
            if curr_emp is not None:
                raise Exception("Employer Does not exist's")
            s.delete(curr_emp)
            s.commit()
        return DeleteEmployer(True)
