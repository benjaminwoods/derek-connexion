# derek-connexion
A Python API built on top of derek, using connexion.

## What is this repo?

This repo contains all of the code required to deploy your own API that uses [`derek-py`](https://github.com/benjaminwoods/derek).

## Development

### `SQLALCHEMY_URL` env var

Currently, `alembic` is used to manage database migrations.

To connect to a database, you will need to set the `SQLALCHEMY_URL` env var. You can do that either as a true env var (`export SQLALCHEMY_URL`; `$env:SQLALCHEMY_URL`; etc.), or you can use a `.env`.

NOTE: `alembic` will read from the **current working directory** when you invoke commands. As `poetry` is set up for this repo, it is implicitly expected that you will run commands from the repo root; it is therefore sensible to keep your **.env** in the repo root as well.

Don't forget to not commit secrets! -- your URL typically includes your password. Avoid committing this.