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

        for row in reader:
            stories.append(
                CHStory(
                    name=get_value_by_mapping(name=mapping.name, row=row),
                    description=get_value_by_mapping(name=mapping.description, row=row),
                    project_id=project_id,
                    epic_id=epic_id,
                )
            )

        return stories


def get_value_by_mapping(*, name: Optional[str], row: Dict[str, str]) -> Optional[str]:
    if name is None:
        return None

    return row.get(cast(str, name), "")
