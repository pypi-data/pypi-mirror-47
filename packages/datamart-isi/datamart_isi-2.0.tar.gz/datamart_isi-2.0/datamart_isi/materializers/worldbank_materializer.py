from datamart_isi.materializers.materializer_base import MaterializerBase
import dateutil.parser as parser
import requests
import os
import json
import pandas as pd
from pandas.io.json import json_normalize

LOCATION_COLUMN_INDEX = 5


class WorldBankMaterializer(MaterializerBase):

    def __init__(self, **kwargs):
        MaterializerBase.__init__(self, **kwargs)
        self.headers = None
        resources_path = os.path.join(os.path.dirname(__file__), "../resources")
        with open(os.path.join(resources_path, 'country_to_id.json'), 'r') as json_file:
            reader = json.load(json_file)
            self.country_to_id_map = reader

    def get(self, metadata: dict = None, constrains: dict = None) -> pd.DataFrame:
        if not constrains:
            constrains = dict()

        date_range = constrains.get("date_range", None)

        locations = constrains.get("named_entity", {}).get(LOCATION_COLUMN_INDEX, None)
        dataset_url = metadata['materialization']['arguments']['url']
        dataset_id = dataset_url.split('/')[5].split('?')[0]
        return self.fetch_data(date_range=date_range, locations=locations, dataset_id=dataset_id)

    def fetch_data(self, date_range: dict = None, locations: list = None, dataset_id: str = None):
        if date_range:
            start_date = date_range.get("start", None)
            if start_date:
                start_year = parser.parse(start_date).year
            end_date = date_range.get("end", None)
            if end_date:
                end_year = parser.parse(end_date).year

        URL_ind_metadata = 'https://api.worldbank.org/v2/indicators/' + dataset_id + '?format=json'
        response_metadata = requests.get(url=URL_ind_metadata)
        json_respose_metadata = json.loads(response_metadata.content)
        json_respose_metadata = json_respose_metadata[1][0]
        sourceNote = json_respose_metadata['sourceNote']
        sourceOrganization = json_respose_metadata['sourceOrganization']

        if not locations:
            if not date_range:
                URL_ind = 'https://api.worldbank.org/v2/countries/' + "ALL" + '/indicators/' + dataset_id + '?format=json'
            else:
                URL_ind = 'https://api.worldbank.org/v2/countries/' + "ALL" + '/indicators/' + dataset_id + '?format=json&date=' + str(
                    start_year) + ':' + str(end_year)
            response_ind = requests.get(url=URL_ind)
            json_respose_ind = json.loads(response_ind.content)

            pages_per_ind = json_respose_ind[0]['pages']
            all_data = []
            for i in range(1, pages_per_ind + 1):
                p = {'page': i}
                response_pagewise = requests.get(url=URL_ind, params=p)
                json_pagewise = json.loads(response_pagewise.content)
                all_data.extend(json_pagewise[1])
            appended_data = pd.io.json.json_normalize(all_data)
            appended_data['sourceNote'] = sourceNote
            appended_data['sourceOrganization'] = sourceOrganization
            return appended_data

        appended_data = None
        for location in locations:
            location_id = self.country_to_id_map.get(location, None)
            if location_id is None:
                continue
            if not date_range:
                URL_ind = 'https://api.worldbank.org/v2/countries/' + location_id + '/indicators/' + dataset_id + '?format=json'
            else:
                URL_ind = 'https://api.worldbank.org/v2/countries/' + location_id + '/indicators/' + dataset_id + '?format=json&date=' + str(
                    start_year) + ':' + str(end_year)
            response_ind = requests.get(url=URL_ind)
            json_respose_ind = json.loads(response_ind.content)

            pages_per_ind = json_respose_ind[0]['pages']
            all_data = []
            for i in range(1, pages_per_ind + 1):
                p = {'page': i}
                response_pagewise = requests.get(url=URL_ind, params=p)
                json_pagewise = json.loads(response_pagewise.content)
                all_data.extend(json_pagewise[1])
            df = pd.io.json.json_normalize(all_data)
            df['sourceNote'] = sourceNote
            df['sourceOrganization'] = sourceOrganization
            if appended_data is None:
                appended_data = df.copy()
            else:
                appended_data = pd.concat([appended_data, df], axis=0, ignore_index=True)
        return appended_data
