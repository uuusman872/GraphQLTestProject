from argon2 import PasswordHasher
from app.configs.config import TOKEN_EXPIRATION_TIME_MINUTES, SECRET_KEY, ALGORITUM
from datetime import datetime, timedelta, timezone
import jwt
from argon2.exceptions import VerifyMismatchError
from graphql import GraphQLError
from app.db.database import Session
from datetime import datetime, timezone
from app.db.models import User
from graphql import GraphQLError
from functools import wraps

ph = PasswordHasher()

def get_authenticated_user(context):
    request_object = context.get("request")
    auth_header = request_object.headers.get("Authorization")
    if auth_header:
        token = auth_header.split(" ")[1]
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITUM])
            if datetime.now(timezone.utc) > datetime.fromtimestamp(payload.get("exp"), tz=timezone.utc):
                raise GraphQLError("Token has expired")
            session = Session()
            user = session.query(User).filter(User.email == payload.get("sub")).first()
            if not user:
                raise GraphQLError("Could not find user")
            return user
        except jwt.exceptions.InvalidSignatureError as e:
            raise GraphQLError("Could Not authenticate user")
    else:
        raise GraphQLError("Missing Authentication token")


def generate_token(email):
    expiration_time = datetime.utcnow() + timedelta(minutes=TOKEN_EXPIRATION_TIME_MINUTES)
    payload = {
        "sub": email,
        "exp": expiration_time
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITUM)
    return token


def verify_password(pwd_hash, pwd):
    try:
        ph.verify(pwd_hash, pwd)
    except VerifyMismatchError as e:
        raise GraphQLError("Invalid Password")


def hash_password(pwd):
    return ph.hash(pwd)



def admin_user(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        info = args[1]
        user = get_authenticated_user(info.context)
        if user.role != "admin":
            raise GraphQLError("You are not authorized to perform this task")
        return func(*args, **kwargs)
    return wrapper