# -*- coding: utf-8 -*-
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

os.environ['DJANGO_SETTINGS_MODULE'] = 'dht.settings'
from dht.dhtNode.documents import dht_node
from djangosolr.documents.query import Query, Q

#Get all dhts
#dhts = dht_node.documents.all()

#print dhts.count()
#for dht in dhts:
#  print dht.hashInfo
hashinfo = "02fc6d2e466e41cc81cc4d5e7caf7be49d6a07a7"
dhts2 = dht_node.documents.q(Q(hashInfo=hashinfo))
print dhts2.count()
for dht in dhts2:
    files = []
    for k in eval(dht.file_list):
        files = []
        for k in eval(dht.file_list):
            title = k[0]
            unit = 'b'
            size = k[1]
            if size >= 1024:
                unit = 'K'
                size = size/1024
            if size >= 1024:
                unit = 'M'
                size = size/1024
            if size >= 1024:
                unit = 'G'
                size = size/1024
            file_info = str(k[0]) + "  " + str(size) + unit
            files.append(file_info)
            dht.file_query_list = files
for dht in dhts2:
    print dht.file_query_list
    #for item in dht.file_list:
    #   print item
    # print type(dht.file_list)
    # print len(dht.file_list)
    # for item in dht.file_list:
    #     files = eval(item)
    #     for it in files:
    #         print it[0]