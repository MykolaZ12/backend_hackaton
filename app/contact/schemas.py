from pydantic import BaseModel, EmailStr


class ContactBase(BaseModel):
    email: EmailStr

    class Config:
        orm_mode = True


class ContactGet(ContactBase):
    id: int


class ContactCreate(ContactBase):
    pass


class ContactUpdate(ContactBase):
    pass


class EmailSchema(BaseModel):
    email: EmailStr
