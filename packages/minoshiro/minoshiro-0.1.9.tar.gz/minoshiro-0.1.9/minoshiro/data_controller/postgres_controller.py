from datetime import datetime
from json import dumps, loads
from typing import Dict, Optional

try:
    from asyncpg import InterfaceError, create_pool
    from asyncpg.pool import Pool
except ImportError:
    print('asyncpg not installed, PostgresSQL function not available.')
    Pool = None
    InterfaceError = None
    create_pool = None

from minoshiro.enums import Medium, Site
from minoshiro.logger import get_default_logger
from .abc import DataController
from .constants import tables
from .postgres_utils import make_tables, parse_record


class PostgresController(DataController):
    """
    To be able to integrate with an existing database, all tables for minoshiro
    will be put under the `minoshiro` schema unless a different schema name is
    passed to the __init__ method.
    """
    __slots__ = ('pool', 'schema')

    def __init__(self, pool: Pool, logger, schema: str = 'minoshiro'):
        """
        Init method. Create the instance with the `get_instance` method to make
        sure you have all the tables needed.

        :param pool: the `asyncpg` connection pool.

        :param logger: logger object used for logging.

        :param schema: the schema name, default is `minoshiro`
        """
        self.pool = pool
        self.schema = schema
        super().__init__(logger)

    @classmethod
    async def get_instance(cls, logger=None, connect_kwargs: dict = None,
                           pool: Pool = None, schema: str = 'minoshiro'):
        """
        Get a new instance of `PostgresController`

        This method will create the appropriate tables needed.

        :param logger: the logger object.

        :param connect_kwargs:
            Keyword arguments for the
            :func:`asyncpg.connection.connect` function.

        :param pool: an existing connection pool.

        One of `pool` or `connect_kwargs` must not be None.

        :param schema: the schema name used. Defaults to `minoshiro`

        :return: a new instance of `PostgresController`
        """
        logger = logger or get_default_logger()
        assert connect_kwargs or pool, (
            'Please either provide a connection pool or '
            'a dict of connection data for creating a new '
            'connection pool.'
        )
        if not pool:
            try:
                pool = await create_pool(**connect_kwargs)
                logger.info('Connection pool made.')
            except InterfaceError as e:
                logger.error(str(e))
                raise e
        logger.info('Creating tables...')
        await make_tables(pool, schema)
        logger.info('Tables created.')
        return cls(pool, logger, schema)

    def __get_table(self, medium: Medium) -> str:
        """
        Get a table name by medium.

        :param medium: the medium type.

        :return: the table name fot that medium.
        """
        return f'{self.schema}.{tables[medium]}'

    async def get_identifier(self, query: str,
                             medium: Medium) -> Optional[Dict[Site, str]]:
        """
        Get the identifier of a given search query.

        :param query: the search query.

        :param medium: the medium type.

        :return:
            A dict of all identifiers for this search query for all sites,
            None if nothing is found.
        """
        sql = """
        SELECT site, identifier FROM {}.lookup
        WHERE LOWER(syname)=LOWER($1) AND medium=$2;
        """.format(self.schema)

        res = await self.pool.fetch(sql, query, medium.value)
        if not res:
            return
        records = (parse_record(record) for record in res)
        return {Site(site): id_ for site, id_ in records if id_}

    async def set_identifier(self, name: str,
                             medium: Medium, site: Site, identifier: str):
        """
        Set the identifier for a given name.

        :param name: the name.

        :param medium: the medium type.

        :param site: the site.

        :param identifier: the identifier.
        """

        sql = """
        INSERT INTO {}.lookup VALUES ($1, $2, $3, $4)
        ON CONFLICT (syname, medium, site)
        DO UPDATE SET identifier=$4;
        """.format(self.schema)

        await self.pool.execute(sql, name, medium.value,
                                site.value, identifier)

    async def get_mal_title(self, id_: str, medium: Medium) -> Optional[str]:
        """
        Get a MAL title by its id.

        :param id_: th MAL id.

        :param medium: the medium type.

        :return: The MAL title if it's found.
        """
        sql = """
        SELECT title FROM {}.mal
        WHERE id=$1 AND medium=$2;
        """.format(self.schema)
        return await self.pool.fetchval(sql, id_, medium.value)

    async def set_mal_title(self, id_: str, medium: Medium, title: str):
        """
        Set the MAL title for a given id.

        :param id_: the MAL id.

        :param medium: The medium type.

        :param title: The MAL title for the given id.
        """

        sql = """
        INSERT INTO {}.mal VALUES ($1, $2, $3)
        ON CONFLICT (id, medium) DO UPDATE
        SET title=$3;
        """.format(self.schema)

        await self.pool.execute(sql, id_, medium.value, title)

    async def medium_data_by_id(self, id_: str, medium: Medium,
                                site: Site) -> Optional[dict]:
        """
        Get data by id.

        Note that if the data cache is more than 1 day old this will delete
        the row in the DB and return None.

        :param id_: the id.

        :param medium: the medium type.

        :param site: the site.

        :return: the data for that id if found.
        """
        sql = """
        SELECT dict, cachetime FROM {} WHERE id=$1 AND site=$2;
        """.format(self.__get_table(medium))
        res = await self.pool.fetchrow(sql, id_, site.value)
        if not res:
            return
        data, cachetime = parse_record(res)
        if (datetime.now() - cachetime).days < 1:
            return loads(data) if data else None
        else:
            await self.delete_medium_data(id_, medium, site)

    async def set_medium_data(self, id_: str, medium: Medium,
                              site: Site, data: dict):
        """
        Set the data for a given id.

        :param id_: the id.

        :param medium: the medium type.

        :param site: the site.

        :param data: the data for the id.
        """
        sql = """
        INSERT INTO {} VALUES ($1, $2, $3, $4)
        ON CONFLICT (id, site) DO UPDATE
        SET dict=$3, cachetime=$4;
        """.format(self.__get_table(medium))

        await self.pool.execute(
            sql, id_, site.value, dumps(data), datetime.now()
        )

    async def delete_medium_data(self, id_: str, medium: Medium, site: Site):
        """
        Delete a row in medium data table.

        :param id_: the id.

        :param medium: the medium type.

        :param site: the site.
        """
        sql = """
        DELETE FROM {} WHERE id=$1 AND site=$2
        """.format(self.__get_table(medium))

        try:
            await self.pool.execute(sql, id_, site.value)
        except Exception as e:
            self.logger.warning(str(e))
