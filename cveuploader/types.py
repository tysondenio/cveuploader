from typing import Optional

import pydantic


class CSVStoryMapping(pydantic.BaseModel):
    name: Optional[str] = None


class CHStory(pydantic.BaseModel):
    name: str
    project_id: str

    id: Optional[str]
    description: Optional[str]
    epic_id: Optional[str]
    story_type: Optional[str]
    worlkflow_state_id: Optional[str]


class CHProject(pydantic.BaseModel):
    id: str
    name: str


class CHEpic(pydantic.BaseModel):
    id: str
    name: str
