from datamart_isi.materializers.materializer_base import MaterializerBase
import psycopg2
import typing
import pandas as pd
from dateutil.parser import parse

DBNAME = 'faostat'
USER = 'postgres'
PASSWORD = '123123'
HOST = 'dsbox02.isi.edu'
DEFAULT_LOCATIONS = ['United States of America']
DEFAULT_START_YEAR = '0'
DEFAULT_END_YEAR = '2018'
DEFAULT_DATA_TYPE = 'trade_liveanimals_e_all_data'
LOCATION_COLUMN_INDEX = 0


class FaoMaterializer(MaterializerBase):
    def __init__(self, **kwargs):
        """ initialization and loading the city name to city id map

        """
        MaterializerBase.__init__(self, **kwargs)
        self.conn = None
        try:
            # read connection parameters
            params = dict()
            params["dbname"] = DBNAME
            params["user"] = USER
            params["password"] = PASSWORD
            params["host"] = HOST

            # connect to the PostgreSQL server
            self.conn = psycopg2.connect(**params)

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    def __del__(self):
        if self.conn is not None:
            self.conn.close()

    def get(self,
            metadata: dict = None,
            constrains: dict = None
            ) -> typing.Optional[pd.DataFrame]:
        """ API for get a dataframe.

            Args:
                metadata: json schema for data_type
                constrains: include some constrains like date_range, location and so on
        """
        if not constrains:
            constrains = dict()

        materialization_arguments = metadata["materialization"].get("arguments", {})
        date_range_start, date_range_end = DEFAULT_START_YEAR, DEFAULT_END_YEAR
        if "date_range" in constrains:
            date_range = constrains.get("date_range")
            if "start" in date_range:
                date_range_start = parse(date_range["start"]).year
            if "end" in date_range:
                date_range_end = parse(date_range["end"]).year
        named_entity = constrains.get("named_entity", {})
        locations = named_entity.get(LOCATION_COLUMN_INDEX, DEFAULT_LOCATIONS)
        data_type = materialization_arguments.get("type", DEFAULT_DATA_TYPE)

        try:

            cur = self.conn.cursor()
            table = data_type
            cur.execute("Select * FROM {0} limit 1".format(table))
            colnames = [desc[0] for desc in cur.description]

            constrains_for_query = "({0} >= {1} AND {2} <= {3}) AND (".format(colnames[3],
                                                                              date_range_start,
                                                                              colnames[3],
                                                                              date_range_end)

            for lo in locations:
                constrains_for_query += "{0} = '{1}' OR ".format(colnames[0], lo)
            constrains_for_query = constrains_for_query[:-4] + ")"
            query_builder = "SELECT * From {0} Where {1};".format(table, constrains_for_query)
            cur.execute(query_builder)
            query_res = cur.fetchall()
            result = pd.DataFrame(columns=[colnames[0], colnames[1], colnames[2], colnames[3], colnames[4]])
            for row in query_res:
                result.loc[len(result)] = row
            return result
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            return None
