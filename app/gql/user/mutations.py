from graphene import Mutation, String, Int, Field, Boolean
from app.db.database import Session
from app.db.models import User
from graphql import GraphQLError
from argon2.exceptions import VerifyMismatchError
from app.utils import generate_token, verify_password
from app.gql.types import UserObject
from app.utils import hash_password, get_authenticated_user
from app.utils import admin_user

class AddUser(Mutation):
    class Arguments:
        email = String(required=True)
        password = String(required=True)
        role = String(required=True)
        username = String(required=True)

    user = Field(lambda: UserObject)
    

    @admin_user
    def mutate(root, info, username, email, password, role):
        session = Session()
        user = session.query(User).filter(User.email == email).first()
        if user:
            raise GraphQLError("User with email already exist's")
        h_password = hash_password(password)
        user = User(email=email, username=username, password_hash=h_password, role=role)
        session.add(user)
        session.commit()
        session.refresh(user)
        return AddUser(user=user)
        

class LoginUser(Mutation):
    class Arguments():
        email = String(required=True)
        password = String(required=True)
    
    token = String()
    
    @staticmethod
    def mutate(root, info, email, password):
        session = Session()
        user = session.query(User).filter(User.email == email).first()
        if not user:
            raise GraphQLError("Invalid email or password")
        verify_password(user.password_hash, password)
        token = generate_token(email)
        return LoginUser(token=token)
