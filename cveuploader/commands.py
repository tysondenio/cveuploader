from .clubhouse import ClubhouseClient
from .csv import convert_csv_to_stories
from .settings import Settings
from .types import CSVStoryMapping
from pathlib import Path
from typing import Optional

import asyncio
import click
import logging


logger = logging.getLogger()


@click.group()
@click.option("--env-file", type=click.Path(exists=True, dir_okay=False))
def cli(env_file: Optional[str]):
    if env_file is not None:
        import dotenv

        dotenv.load_dotenv(env_file)

    logging.basicConfig(level=logging.DEBUG)


@click.command()
@click.argument("csv-file", type=click.Path(exists=True, dir_okay=False), required=True)
@click.argument("epic-id", type=str, required=True)
@click.argument("project-id", type=str, required=True)
@click.option("-n", "--name-field", type=str, default=None)
@click.option("-d", "--description-field", type=str, default=None)
@click.option("--dry-run", type=bool, default=False, is_flag=True)
def upload_csv(
    csv_file: str,
    epic_id: str,
    project_id: str,
    name_field: Optional[str] = None,
    description_field: Optional[str] = None,
    dry_run: bool = False,
):

    settings = Settings()

    logger.info(f"Converting {csv_file} to Clubhouse Stories")
    # Create CSV to Story mapping
    mapping = CSVStoryMapping(name=name_field, description=description_field)

    stories = convert_csv_to_stories(
        csv_path=Path(csv_file), mapping=mapping, project_id=project_id, epic_id=epic_id
    )
    logger.info(f"Converted {len(stories)} rows to stories")

    if dry_run is True:
        logging.info("Dry Run, not updating Clubhouse")
        logging.info("Stories that would have been created:")
        for story in stories:
            logging.info(story.json(exclude_none=True))

        return

    logger.info("Uploading stories to Clubhouse")
    client = ClubhouseClient(api_key=settings.clubhouse_token)

    uploaded_stories = asyncio.run(client.create_stories(data=stories))
    logger.info(f"Uploaded {len(uploaded_stories)} to Clubhouse")

    for story in uploaded_stories:
        logger.info(f"Created story {story.id} - {story.name}")


@click.command()
def list_projects():
    settings = Settings()
    client = ClubhouseClient(api_key=settings.clubhouse_token)

    logger.info("Fetching projects from Clubhouse")

    async def _run(client):
        projects = await client.get_projects()
        await client.close()

        return projects

    projects = asyncio.run(_run(client))

    for project in projects:
        logger.info(f"Project {project.name} - {project.id}")


@click.command()
def list_epics():
    settings = Settings()
    client = ClubhouseClient(api_key=settings.clubhouse_token)

    logger.info("Fetching epics from Clubhouse")

    async def _run(client):
        epics = await client.get_epics()
        await client.close()

        return epics

    epics = asyncio.run(_run(client))

    for epic in epics:
        logger.info(f"Epic {epic.name} - {epic.id}")


cli.add_command(upload_csv)
cli.add_command(list_projects)
cli.add_command(list_epics)
