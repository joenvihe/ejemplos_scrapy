import traceback

import dj_database_url
import psycopg2

from twisted.internet import defer
from twisted.enterprise import adbapi
from scrapy.exceptions import NotConfigured


class PostgresqlWriter(object):
    """
    A spider that writes to MySQL databases
    """

    @classmethod
    def from_crawler(cls, crawler):
        """Retrieves scrapy crawler and accesses pipeline's settings"""

        # Get MySQL URL from settings
        postgresql_url = crawler.settings.get('POSTGRESQL_PIPELINE_URL', None)

        # If doesn't exist, disable the pipeline
        if not postgresql_url:
            raise NotConfigured

        # Create the class
        return cls(postgresql_url)

    def __init__(self, postgresql_url):
        """Opens a postgresql connection pool"""

        # Store the url for future reference
        self.postgresql_url = postgresql_url
        # Report connection error only once
        self.report_connection_error = True

        # Parse MySQL URL and try to initialize a connection
        conn_kwargs = PostgresqlWriter.parse_postgresql_url(postgresql_url)
        self.dbpool = adbapi.ConnectionPool('psycopg2',
                                            **conn_kwargs)
        #self.log("hola")

    def close_spider(self, spider):
        """Discard the database pool on spider close"""
        self.dbpool.close()

    @defer.inlineCallbacks
    def process_item(self, item, spider):
        """Processes the item. Does insert into PostgreSQL"""

        logger = spider.logger

        try:
            yield self.dbpool.runInteraction(self.do_replace, item)
        except psycopg2.OperationalError:
            if self.report_connection_error:
                logger.error("Can't connect to PostgresSQL: %s" % self.postgresql_url)
                self.report_connection_error = False
        except:
            print traceback.format_exc()

        # Return the item for the next stage
        defer.returnValue(item)

    @staticmethod
    def do_replace(tx, item):
        """Does the actual REPLACE INTO"""

        sql = """INSERT INTO public.producto (principal,categoria,subcategoria,
                                        tipo,titulo, brand,
                                        codigo_producto,imagen,estrellas,
                                        especificacion,mejor_precio,precio_normal,
                                        unidad,promocion,
                                        url,project,spider,server)
                 VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
        #print(item)
        args = (
            item["principal"][0],
            item["categoria"][0],
            item["subcategoria"][0],
            item["tipo"][0],
            item["titulo"][0],
            item["brand"][0],
            item["codigo_producto"][0],
            item["imagen"][0],
            item["estrellas"][0],
            item["especificacion"][0],
            item["mejor_precio"][0],
            item["precio_normal"][0],
            item["unidad"][0],
            item["promocion"][0],
            item["url"][0],
            item["project"][0],
            item["spider"][0],
            item["server"][0]
        )

        tx.execute(sql, args)

    @staticmethod
    def parse_postgresql_url(postgresql_url):
        """
        Parses mysql url and prepares arguments for
        adbapi.ConnectionPool()
        """

        params = dj_database_url.parse(postgresql_url)

        conn_kwargs = {}
        conn_kwargs['database'] = params['NAME']
        conn_kwargs['user'] = params['USER']
        conn_kwargs['password'] = params['PASSWORD']
        conn_kwargs['host'] = params['HOST']
        conn_kwargs['port'] = params['PORT']

        # Remove items with empty values
        conn_kwargs = dict((k, v) for k, v in conn_kwargs.iteritems() if v)

        return conn_kwargs
