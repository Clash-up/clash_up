import asyncio
import json

from invoke import task

from shared.database import DatabaseManager, init_models
from shared.models import Player, WarEntry
from shared.settings import settings


@task
def run_postgres(c):
    c.run(
        "docker run --name clash_up -e POSTGRES_USER=clash_up -e POSTGRES_PASSWORD=clash_up -e POSTGRES_DB=clash_up -p 5432:5432 -d postgres"  # noqa: E501
    )


@task
def load_initial_data(c, path="initial_data.json"):
    async def _load_data():
        await init_models(await DatabaseManager.get_engine(settings.POSTGRES_URL, echo=True))
        async with DatabaseManager.session(settings.POSTGRES_URL) as session:
            with open(path) as f:
                data = json.load(f)

            for p in data["players"]:
                player = Player(
                    id=p["id"],
                    name=p["name"],
                    tag=p["tag"],
                    trophies=p["trophies"],
                    donations=p["donations"],
                    donations_received=p["donations_received"],
                    role=p["role"],
                    town_hall_level=p["town_hall_level"],
                )
                session.add(player)
                for e in p.get("cw_attacks", []):
                    session.add(
                        WarEntry(
                            id=e["id"],
                            war_id=e["war_id"],
                            stars=e["stars"],
                            destruction_percentage=e["destruction_percentage"],
                            duration=e["duration"],
                            player=player,
                        )
                    )
            await session.commit()

    asyncio.run(_load_data())
