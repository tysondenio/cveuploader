from .types import CSVStoryMapping, CHStory
from pathlib import Path
from typing import cast, Dict, List, Optional

import csv
import logging


logger = logging.getLogger(__name__)


def convert_csv_to_stories(
    *, csv_path: Path, mapping: CSVStoryMapping, project_id: str, epic_id: str
) -> List[CHStory]:
    with open(csv_path, "r") as csv_file:
        reader = csv.DictReader(csv_file)
        mapping_dict = mapping.dict(exclude_none=True)

        for key, value in mapping_dict.items():
            if value not in cast(List, reader.fieldnames):
                logger.error(
                    f"Unable to map CSV to Clubhouse Story\n{value} is not a valid column for {key}"
                )
                raise RuntimeError()

        stories: List[CHStory] = []
        story_names: List[str] = []

        for row in reader:

            name = get_value_by_mapping(name=mapping.name, row=row)

            if name is not None and name not in story_names:
                description = get_story_description(row=row)

                stories.append(
                    CHStory(
                        name=name,
                        description=description,
                        project_id=project_id,
                        epic_id=epic_id,
                    )
                )
                story_names.append(name)

        return stories


def get_story_description(row: Dict[str, str]) -> str:
    description: List[str] = []

    for key, value in row.items():
        description.append(f"# {key}")
        description.append(value)
        description.append("\n")

    return "\n".join(description)


def get_value_by_mapping(*, name: Optional[str], row: Dict[str, str]) -> Optional[str]:
    if name is None:
        return None

    return row.get(cast(str, name), "")
