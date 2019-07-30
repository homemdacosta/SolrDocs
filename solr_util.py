import pysolr

# Local import
import config_util

class SolrUtil():

    #solr_url_with_core = None
    solr = None

    def fire_solr_util (self):
        # Retrieve Solr configuration
        solr_url = config_util.get_configuration(section='solr', option='url')
        solr_core = config_util.get_configuration(section='solr', option='core')

        # Initializate PySolr
        self.solr = pysolr.Solr(solr_url + solr_core, always_commit=True)

    def search (self, param = '*:*', debug = False):
        results = self.solr.search(param)
        if debug:
            print("START Result of search: ")
            for result in results: 
                print(result)
            print("END Result of search.")
        return results

    def __init__(self):
        self.fire_solr_util()

solru = SolrUtil()
solru.search('"HEALTH CHECK"')