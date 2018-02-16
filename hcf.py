#!/usr/bin/env python


import re

csv_file_1 = open( "test.csv",'r')
csv_file_2 = open( "test2.csv",'r')
delim = " "
hosts = {}
comment_re = re.compile(r'(\w+ ){3,}|\W{2,}', re.VERBOSE) 
class Host: pass

def parse_csv( f ):
    headings = f.readline()
    col_key, col_data = headings.strip().split( delim )

    for line in f:
        if not comment_re.match(line): 
            ''' 
            First column of each line is treated as key
            '''
            print line
            host_key, host_data = line.strip().split( delim )
            if host_key not in hosts.keys():
                host = Host()
                setattr( host, col_data, host_data ) 
                hosts[ host_key ] = host 
            else:
                host_tmp = hosts[ host_key ]
                setattr( host_tmp, col_data, host_data )
                hosts[ host_key ] = host_tmp

parse_csv(csv_file_1)
parse_csv(csv_file_2)

for host in sorted( hosts.keys() ):
    pkg, app = hosts[ host ].__dict__.values()
    print host , pkg, app

