from typing import Optional, Union, Annotated, Literal
from pydantic import BaseModel, Field, model_validator

class TokenTaskBase(BaseModel):
    token_name: str
    # אפשרות ל־username או user_id (לפחות אחד חובה)
    user_id: Optional[str] = None
    username: Optional[str] = None
    base_url: str = "https://api.twitter.com/2"

    @model_validator(mode="after")
    def _require_identifier(self):
        if not self.user_id and not self.username:
            raise ValueError("Either user_id or username must be provided")
        return self

class FetchTweetsTask(TokenTaskBase):
    type: Literal["fetch"] = "fetch"
    until_id: Optional[str] = None
    max_results: int = Field(50, ge=1, le=100)

class CountTweetsTask(TokenTaskBase):
    type: Literal["count"] = "count"

TokenTask = Annotated[Union[FetchTweetsTask, CountTweetsTask], Field(discriminator="type")]
