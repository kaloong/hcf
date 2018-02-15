#!/usr/bin/env python

csv_file_1 = open( "test.csv",'r')
csv_file_2 = open( "test2.csv",'r')

hosts = {}
class Host: pass

def parse_csv( f ):
    headings = f.readline()
    header_key, header_data = headings.strip().split(" ")

    for line in f:
        host_key, host_data = line.strip().split(" ")
        if host_key not in hosts.keys():
            host = Host()
            setattr( host, header_data, host_data ) 
            hosts[ host_key ] = host 
        else:
            host_tmp = hosts[ host_key ]
            setattr( host_tmp, header_data, host_data )
            hosts[ host_key ] = host_tmp

parse_csv(csv_file_1)
parse_csv(csv_file_2)

for i in sorted( hosts.keys() ):
    print i, hosts[i].__dict__

