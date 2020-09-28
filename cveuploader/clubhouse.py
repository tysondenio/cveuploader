from .types import CHStory, CHProject, CHEpic
from typing import cast
from typing import Any, Dict, List, Optional, Tuple, Union

import aiohttp


class ClubhouseAPIError(Exception):
    ...


class ClubhouseClient:
    def __init__(
        self,
        *,
        api_key: str,
        url: str = "https://api.clubhouse.io/api/v3",
        session: aiohttp.ClientSession = None,
    ):
        self.api_key = api_key
        self.url = url

        self._session = session

    @property
    def session(self) -> aiohttp.ClientSession:
        if self._session is None:
            self._session = aiohttp.ClientSession(
                headers={
                    "Clubhouse-Token": f"{self.api_key}",
                    "Content-Type": "application/json",
                    "Accepts": "application/json",
                }
            )

        return self._session

    async def close(self):
        if self._session is not None:
            await self.session.close()

    async def _call_api(
        self, *, method: str, path: str, data: Optional[Dict[str, Any]] = None
    ) -> Tuple[int, Optional[Union[Dict[str, Any], List[Any]]]]:
        async with self.session.request(
            method=method, url=f"{self.url}{path}", json=data
        ) as response:
            status_code = response.status
            data = await response.json()

            return (status_code, data)

    async def get_story(self, *, id: str) -> CHStory:
        status_code, story = await self._call_api(method="GET", path=f"/stories/{id}")

        if status_code != 200:
            raise ClubhouseAPIError(
                f"Unable to get story: Response status: {status_code}"
            )

        return CHStory.parse_obj(story)

    async def create_story(self, *, data: CHStory) -> CHStory:
        status_code, story = await self._call_api(
            method="POST", path="/stories", data=data.dict(exclude_none=True)
        )

        if status_code != 201:
            raise ClubhouseAPIError(
                f"Unable to create story: Response status: {status_code}"
            )

        return CHStory.parse_obj(story)

    async def create_stories(self, *, data: List[CHStory]) -> List[CHStory]:
        status_code, stories = await self._call_api(
            method="POST",
            path="/stories/bulk",
            data={"stories": [story.dict(exclude_none=True) for story in data]},
        )

        if status_code != 201:
            raise ClubhouseAPIError(
                f"Unable to create stories: Response status: {status_code}"
            )

        return [CHStory.parse_obj(story) for story in cast(List, stories)]

    async def search_stories(self, *, query) -> List[CHStory]:
        status_code, stories = await self._call_api(
            method="GET", path="/search/stories", data={"page_size": 10, "query": query}
        )

        if status_code != 200:
            raise ClubhouseAPIError(
                f"Unable to search stories: Response status: {status_code}"
            )

        return [
            CHStory.parse_obj(story) for story in cast(Dict[str, Any], stories)["data"]
        ]

    async def get_projects(self) -> List[CHProject]:
        status_code, projects = await self._call_api(method="GET", path="/projects")

        if status_code != 200:
            raise ClubhouseAPIError(
                f"Unable to get projects.  Response status: {status_code}"
            )

        return [
            CHProject.parse_obj(project)
            for project in cast(List[Dict[str, Any]], projects)
        ]

    async def get_epics(self) -> List[CHEpic]:
        status_code, epics = await self._call_api(method="GET", path="/epics")

        if status_code != 200:
            raise ClubhouseAPIError(
                f"Unable to get epics.  Response status: {status_code}"
            )

        return [CHEpic.parse_obj(epic) for epic in cast(List[Dict[str, Any]], epics)]
