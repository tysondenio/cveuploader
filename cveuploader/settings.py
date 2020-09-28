from typing import Optional

import pydantic


class Settings(pydantic.BaseSettings):
    clubhouse_token: str
    clubhouse_url: pydantic.HttpUrl = "https://api.clubhouse.io/api/v3"

    story_type: Optional[str]
    epic_id: Optional[str]
    workflow_state_id: Optional[str]
