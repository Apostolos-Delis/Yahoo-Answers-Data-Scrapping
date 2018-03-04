"""Extend your models from `Model` in this module."""
import click
import orator
from orator import Schema

# You will have to add your own settings here
from "something..." import settings

_CONFIG = {
    'mysql': {
        'driver': 'mysql',
        'host': settings.YAHOO_ANSWERS_DB_HOST,
        'port': settings.YAHOO_ANSWERS_DB_PORT,
        'database': settings.YAHOO_ANSWERS_DB_NAME,
        'user': settings.YAHOO_ANSWERS_DB_USER,
        'password': settings.YAHOO_ANSWERS_DB_PASS,
        'log_queries': settings.APP_DB_LOG_QUERIES
    }
}

_DB = orator.DatabaseManager(_CONFIG)
orator.Model.set_connection_resolver(_DB)
Model = orator.Model
raw = _DB.raw
schema = Schema(_DB)


@click.command()
def test_db_conn():
    for row in _DB.select('SHOW STATUS'):
        print(row['Variable_name'], ': ', row['Value'], sep='')


@click.group()
def cli():
    pass


cli.add_command(test_db_conn)


if __name__ == '__main__':
    cli()
