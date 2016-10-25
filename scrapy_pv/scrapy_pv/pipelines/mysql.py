import traceback

import dj_database_url
import MySQLdb

from twisted.internet import defer
from twisted.enterprise import adbapi
from scrapy.exceptions import NotConfigured


class MysqlWriter(object):
    """
    A spider that writes to MySQL databases
    """

    @classmethod
    def from_crawler(cls, crawler):
        """Retrieves scrapy crawler and accesses pipeline's settings"""

        # Get MySQL URL from settings
        mysql_url = crawler.settings.get('MYSQL_PIPELINE_URL', None)

        # If doesn't exist, disable the pipeline
        if not mysql_url:
            raise NotConfigured

        # Create the class
        return cls(mysql_url)

    def __init__(self, mysql_url):
        """Opens a MySQL connection pool"""

        # Store the url for future reference
        self.mysql_url = mysql_url
        # Report connection error only once
        self.report_connection_error = True

        # Parse MySQL URL and try to initialize a connection
        conn_kwargs = MysqlWriter.parse_mysql_url(mysql_url)
        self.dbpool = adbapi.ConnectionPool('MySQLdb',
                                            charset='utf8',
                                            use_unicode=True,
                                            connect_timeout=5,
                                            **conn_kwargs)

    def close_spider(self, spider):
        """Discard the database pool on spider close"""
        self.dbpool.close()

    @defer.inlineCallbacks
    def process_item(self, item, spider):
        """Processes the item. Does insert into MySQL"""

        logger = spider.logger

        try:
            yield self.dbpool.runInteraction(self.do_replace, item)
        except MySQLdb.OperationalError:
            if self.report_connection_error:
                logger.error("Can't connect to MySQL: %s" % self.mysql_url)
                self.report_connection_error = False
        except:
            print traceback.format_exc()

        # Return the item for the next stage
        defer.returnValue(item)

    @staticmethod
    def do_replace(tx, item):
        """Does the actual REPLACE INTO"""

        sql = """REPLACE INTO producto (principal,categoria,subcategoria,
                                        tipo,titulo, brand,
                                        codigo_producto,imagen,estrellas,
                                        especificacion,mejor_precio,precio_normal,
                                        url,project,spider,server)
                 VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
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
            item["url"][0],
            item["project"][0],
            item["spider"][0],
            item["server"][0]
        )

        tx.execute(sql, args)

    @staticmethod
    def parse_mysql_url(mysql_url):
        """
        Parses mysql url and prepares arguments for
        adbapi.ConnectionPool()
        """

        params = dj_database_url.parse(mysql_url)

        conn_kwargs = {}
        conn_kwargs['host'] = params['HOST']
        conn_kwargs['user'] = params['USER']
        conn_kwargs['passwd'] = params['PASSWORD']
        conn_kwargs['db'] = params['NAME']
        conn_kwargs['port'] = params['PORT']

        # Remove items with empty values
        conn_kwargs = dict((k, v) for k, v in conn_kwargs.iteritems() if v)

        return conn_kwargs
