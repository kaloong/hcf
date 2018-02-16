#!/usr/bin/env python


import re
import argparse

hosts = {}
regex_0 = re.compile(r'\w+\S+\w+$',re.IGNORECASE) 
'''
regex_1 = re.compile(r'(\w+\d+\w+\S+\s)+|\w+ \w+$') 
'''
regex_1 = re.compile(r'(\w+\d+( |: )\w.*))+',re.IGNORECASE) 
regex_2 = re.compile(r'^\s*$|={1,}|-{1,}|(\w+\d+)|(\w+(\s|\W))',re.IGNORECASE) 
class Host: pass

def parse_csv( f, delim ):
    headings = f.readline()
    col_key, col_data = headings.strip().split( delim )

    for line in f:
        print "+0", regex_0.match(line)
        print "+1", regex_1.match(line)
        print "+2", regex_2.match(line)
        if regex_1.match(line) and not regex_2.match(line): 
            ''' 
            First column of each line is treated as key
            '''
            host_key, host_data = line.strip().split( delim )
            if host_key.upper() not in hosts.keys():
                host = Host()
                setattr( host, col_data, host_data ) 
                hosts[ host_key.upper() ] = host 
                print "-", host_key.upper(), host
            else:
                host_tmp = hosts[ host_key.upper() ]
                setattr( host_tmp, col_data, host_data )
                hosts[ host_key.upper() ] = host_tmp
                print "-", host_key.upper(), host_tmp

def main():
    parser = argparse.ArgumentParser(description='[i] Process CSV and convert each entry into Nagios hosts/hostgroups file.')
    parser.add_argument('-c1', "--csv1", help='[i] Specify CSV file 1 to be merged.')
    parser.add_argument('-c2', "--csv2", help='[i] Specify CSV file 2 to be merged.')
    parser.add_argument('-o', "--outfile", default="output.csv", help='[i] Specify output directory for generated files.')
    parser.add_argument('-f', "--delimiter", default=" ", help='[i] Specify delimiter to be used.')
    args = parser.parse_args()
    if args.csv1 and args.csv2:
        ''' Read in first file '''
        with open( args.csv1, 'r' ) as infile:
            parse_csv(infile, args.delimiter )

        ''' Read in second file '''
        with open( args.csv2, 'r' ) as infile:
            parse_csv(infile, args.delimiter )

        print("******** Export file *********\n")

        with open( args.outfile, 'wb') as outfile:
            for host in sorted( hosts.keys() ):
                print "---", hosts[ host ].__dict__.values()
                pkg, app = hosts[ host ].__dict__.values()
                print app, host , pkg
                outfile.writelines("%s %s %s\n"%(app, host , pkg))

    print("\n****** Export completed ******")

if __name__ == '__main__':
    main()
