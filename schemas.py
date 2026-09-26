from pydantic import BaseModel

class AskRequest(BaseModel):
    question : str
    source_kb : str | None = None

class AskResponse(BaseModel):
    answer : str
    citation : list[dict]
