es-whois
========

Generic WHOIS server to search  Elastic Search Database
(http://www.elasticsearch.org) via whois interface.

The service is schema-agnostic but you will need to specify what index
you want to search in config file. if you want to search multiple
indexes, use alias.

We presume that indexes are created with current date. So searchindex
name means that there will be indexes with searchindex-<day><month><year>

this can be changed in the future

The core of the code was taken from  https://github.com/Rafiot/Whois-Server/
and then hacked in accordance with our orthodox obsession with Elastic Search :)



installing
==========

should be easy: pip install pyes IPy

and this should be it

Running
=======

The best way to run whois service is with supervisor:

[program:whoissrv]
directory = /path/to/es-whois
command = python whoisrv.py
autorestart = true
autostart = true

Querying
========

querying is simple:

whois -h <host>  field:value+field2:value2+rangefield:[From|To]

you can also specify count:<how many results> and
start:<startingfrom>as paramters
