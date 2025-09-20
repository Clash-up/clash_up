from invoke import task


@task
def run_postgres(c):
    c.run(
        "docker run --name clash_up -e POSTGRES_USER=clash_up -e POSTGRES_PASSWORD=clash_up -e POSTGRES_DB=clash_up -p 5432:5432 -d postgres"  # noqa: E501
    )
