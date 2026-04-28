from pydantic import BaseModel, ConfigDict


class UserPreferenceRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    default_search_mode: str
    preferred_llm_provider: str


class UserPreferenceUpdate(BaseModel):
    default_search_mode: str | None = None
    preferred_llm_provider: str | None = None