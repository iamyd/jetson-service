from watson_developer_cloud import DiscoveryV1
import logging
#I made dis.
class Discovery():
    creds = {}
    api_ids = {}

    def __init__(self, url, username, password, collection_id, config_id, environment_id):
        self.creds['url'] = url
        self.creds['username'] = username
        self.creds['password'] = password

        self.api_ids['collection_id'] = collection_id
        self.api_ids['configuration_id'] = config_id
        self.api_ids['environment_id'] = environment_id

        self.discovery = DiscoveryV1(
            username=self.creds['username'],
            password=self.creds['password'],
            version='2017-09-01'
        )

    def query(self, queryString, label):
        logging.info("discvoery query(): querystring: " + queryString + " label: " + label + "\n")
        filterString = 'label::"'+label+'"'
        qopts = {
                    'natural_language_query': queryString,
                    'filter': filterString,
                    'passages': 'true',
                    'text': 'true',
                    'html': 'true',
                    'return': 'text,html'
            }
        my_query = self.discovery.query(self.api_ids['environment_id'],
                                        self.api_ids['collection_id'],
                                        qopts)

        matches = my_query['results']
        htmlList = []
        max_score = matches[0]['score']
        for i in range(len(matches[0:3])):
            if (max_score - matches[i]['score'] < 0.2 * max_score):
                htmlList.append(matches[i])

        return htmlList
