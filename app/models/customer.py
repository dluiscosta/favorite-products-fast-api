import pydantic


class CustomerModel(pydantic.BaseModel):
    full_name: str
    email: pydantic.EmailStr
