from graphene import ObjectType, String, Int, List, Field


class EmployerObject(ObjectType):
    id = Int()
    name = String()
    contact_email = String()
    industry = String()
    jobs = List(lambda: JobObject)

    @staticmethod
    def resolve_jobs(root, info):
        return root.jobs


class JobObject(ObjectType):
    id = Int()
    title = String()
    description = String()
    employer_id = Int()
    employer = Field(lambda: EmployerObject)
    applications = List(lambda: JobApplicationObject)

    @staticmethod
    def resolve_applications(root, info):
        return root.applications

    @staticmethod
    def resolve_employer(root, info):
        return root.employer


class UserObject(ObjectType):
    id = Int()
    username = String()
    email = String()
    role = String()
    applications = List(lambda: JobApplicationObject)

    @staticmethod
    def resolve_applications(root, info):
        return root.applications


class JobApplicationObject(ObjectType):
    id = Int()
    user_id = Int()
    job_id = Int()
    user = Field(lambda: UserObject)
    job = Field(lambda: JobObject)

    @staticmethod
    def resolve_user(root, info):
        return root.user

    @staticmethod
    def resolve_job(root, info):
        return root.job
