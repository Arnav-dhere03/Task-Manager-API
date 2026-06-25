from pydantic import BaseModel, EmailStr
from pydantic import ConfigDict

class AddMemberRequest(BaseModel):
    email: EmailStr

class MemberResponse(BaseModel):
    id: int
    username: str
    email: EmailStr

    model_config = ConfigDict(
        from_attributes=True
    )
