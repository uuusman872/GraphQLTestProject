from starlette_graphene3 import GraphQLApp, make_graphiql_handler, make_playground_handler
from fastapi import FastAPI
from app.gql.queries import Query
from app.gql.mutations import Mutation
from graphene import Schema
from app.db.database import prepare_database, Session
from app.db.models import Employer, Jobs


schema = Schema(query=Query, mutation=Mutation)
app = FastAPI()

@app.on_event("startup")
def startup_event():
    prepare_database()


@app.get("/employers")
def get_employers():
    session = Session()
    employers_data = session.query(Employer).all()
    session.close()
    return employers_data


@app.get("/jobs")
def get_employers():
    session = Session()
    job_data = session.query(Jobs).all()
    session.close()
    return job_data


# app.mount("/graphql", GraphQLApp(schema, on_get=make_playground_handler()))
app.mount("/graphql", GraphQLApp(schema, on_get=make_graphiql_handler()))