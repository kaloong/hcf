#!/usr/bin/env python

import re
import argparse

hosts = {}
'''
regex_0 = re.compile(r'\w+\S+\w+$',re.IGNORECASE) 
regex_1 = re.compile(r'(\w+\d+\w+\S+\s)+|\w+ \w+$') 
'''
regex_1 = re.compile(r'(\w+\d+( |: )(\w.*))+',re.IGNORECASE) 
regex_2 = re.compile(r'^\s*$|={1,}|-{1,}|(\w+\d+)|(\w+(\s|\W))',re.IGNORECASE) 
class Host: pass

def parse_csv( f, delim ):
    headings = f.readline()
    col_key, col_data = headings.strip().split( delim )

    for line in f:
        if regex_1.match(line) or not regex_2.match(line): 
            ''' 
            First column of each line is treated as key
            '''
            host_key, host_data = line.strip().split( delim )
            if host_key.upper() not in hosts.keys():
                host = Host()
                setattr( host, col_data, host_data ) 
                hosts[ host_key.upper() ] = host 
            else:
                host_tmp = hosts[ host_key.upper() ]
                setattr( host_tmp, col_data, host_data )
                hosts[ host_key.upper() ] = host_tmp

def main():
    parser = argparse.ArgumentParser(description='[i] Process CSV and convert each entry into Nagios hosts/hostgroups file.')
    parser.add_argument('-l', "--csvlist", type=str, nargs='+', help='[i] Specify CSV file list to be merged.')
    parser.add_argument('-o', "--outfile", default="output.csv", help='[i] Specify output directory for generated files.')
    parser.add_argument('-f', "--delimiter", default=": ", help='[i] Specify delimiter to be used.')
    args = parser.parse_args()
    if args.csvlist:
        for csv in args.csvlist:
            with open( csv, 'r' ) as infile:
                parse_csv( infile, args.delimiter)
        with open( args.outfile, 'wb') as outfile:
            for host in sorted(hosts.keys()):
                outfile.write( host+ ";" )
                for detail in sorted( hosts[ host ].__dict__) :
                    outfile.write( hosts[ host ].__dict__[ detail ] + ";" ) 
                outfile.write("\n") 

if __name__ == '__main__':
    main()
