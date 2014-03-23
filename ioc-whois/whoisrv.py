#!/usr/bin/python

# built on the top of https://github.com/Rafiot/Whois-Server/
import sys
import os
import ConfigParser

location = os.getcwd() + "/aha"
if '__file__' in dir():
    location = __file__

sys.path.append(os.path.dirname(os.path.abspath(location)))
sys.path.append(os.path.dirname(os.path.join(os.path.abspath(location),'lib')))


config = ConfigParser.RawConfigParser()
if len(sys.argv) > 1:
	config.read(sys.argv[1])
else:
	config.read("whois-server.conf")

import syslog
syslog.openlog('Whois_Queries', syslog.LOG_PID, syslog.LOG_USER)


es_db = config.get('whois_server','es_host')
es_index = config.get('whois_server','es_index')
es_type = config.get('whois_server','es_type')
host = config.get('whois_server','listen')
port = int(config.get('whois_server','port_query'))

import SocketServer
from lib.queries.whois_query import *

class WhoisServer(SocketServer.BaseRequestHandler ):
    def handle(self):
        syslog.syslog(syslog.LOG_INFO, self.client_address[0] + ' is connected' )
        print self.client_address[0] , ' is connected' 
        query_maker = WhoisQuery(es_db, es_index, es_type)
        queries = 0
        query = self.request.recv(1024).strip()
        if query == '':
	    syslog.syslog(syslog.LOG_DEBUG, self.client_address[0] + ' is gone' )
            return
	#    break
        self.request.send("Query results:\n\n")
        if query.find(':') < 1:
            query = "banner:%s" % query
        syslog.syslog(syslog.LOG_DEBUG, 'Query of ' + self.client_address[0] + ': ' + query)
        queries += 1
        response = "%s"% (query_maker.whois_query(query))
        if queries % 10 == 0:
	  syslog.syslog(syslog.LOG_INFO, self.client_address[0] + ' made ' + str(queries) + ' queries.')
        self.request.send(response + '\n\n')



SocketServer.ThreadingTCPServer.allow_reuse_address = True
server = SocketServer.ThreadingTCPServer((host, port), WhoisServer)
server.serve_forever()
