from dht.dhtNode import models
from djangosolr import documents

class dht_node(documents.Document):
    file_query_list = []
    file_count = 0
    file_max_size = ''
    class Meta:
        model = models.TorrentInfo
        type = '*'