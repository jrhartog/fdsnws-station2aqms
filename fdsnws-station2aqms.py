import argparse
import os
import sys

import obspy

from obspy.core import UTCDateTime
try: 
    # more recent versions of ObsPy
    from obspy.clients.fdsn import Client
except:
    # this works for 0.10.2 version
    from obspy.fdsn import Client


def create_insert_statements(inventory):
    """
        Given an obspy Inventory object, creates
        insert statements for station_data, channel_data, and simple_response
    """
    STA_SQL = "insert into station_data (net,sta,seedchan,channel,location,etc."
    return

if __name__ == "__main__":
    """
        Simple program to query a FDSN Station Webservice and output sql
        scripts that can be used to load basic meta-data into a AQMS database.
        Optionally, it will insert the data straight into a PostgreSQL database,
        rather than to files.

        Populates D_Abbreviation, Station_Data, Channel_Data, and Simple_Response
    """

    parser = argparse.ArgumentParser(description="Retrieves FDSN StationXML from a fdsn webservice \
        and writes SQL statements that can be used to populate AQMS tables station_data, channel_data, \
        and simple_response") 

    # required argument
    help_text = "Specify a network code, wildcards are allowed"
    parser.add_argument("net",help=help_text)

    # optional arguments
    help_text = "Populate a PostgreSQL database, requires environment variables DB_PORT,DB_NAME,DB_HOST,\
                 DB_USER,DB_PASSWORD. The default is to write to .sql files"
    parser.add_argument("-p","--populate",help=help_text,action="store_true")
    help_text = "Specify a station code, wildcards are allowed"
    parser.add_argument("-s","--station",help=help_text)
    help_text = "Specify a channel code, wildcards are allowed"
    parser.add_argument("-c","--channel",help=help_text)
    help_text = "Specify a location code, wildcards are allowed"
    parser.add_argument("-l","--location",help=help_text)
    help_text = "Request metadata for all times, default is active channels only!"
    parser.add_argument("-a","--all",help=help_text,action="store_true")
    help_text = "Specify Webservice to query (default=IRIS)"
    parser.add_argument("-ws","--webservice",help=help_text,default="IRIS")
    help_text = "Specify level of information (default=response)"
    parser.add_argument("-level","--level",help=help_text,default="response",choices=["station","channel","response"])
    help_text = "Be more verbose"
    parser.add_argument("-v","--verbose",help=help_text,action="store_true")
    
    args = parser.parse_args()

    client = Client(args.webservice)

    HAVE_DB = False
    if args.populate:
        try:
            import psycopg2
            DB_HOST = os.getenv("DB_HOST", "localhost")
            DB_NAME = os.getenv("DB_NAME", "rtdb")
            DB_PORT = os.getenv("DB_PORT", "5432")
            DB_USER = os.getenv("DB_USER", "browser")
            DB_PASSWORD = os.getenv("DB_PASSWORD", "browser") 
            try:
                db = psycopg2.connect(host=DB_HOST,port=DB_PORT,database=DB_NAME,user=DB_USER,password=DB_PASSWORD)
                cursor = db.cursor()
                HAVE_DB = True
            except Error as e:
                print "Error connecting to database {} on {}:{} as user {} ({}). Will create .sql files.".format(DB_NAME,
                       DB_HOST,DB_PORT,DB_USER, e)
                HAVE_DB = False
               
        except Exception as e:
            print "Error: {}".format(e)
            print "If psycopg2 db driver needs to be installed, try 'pip install psycopg2'."
            print "I will create .sql files that can  be used for loading."
            HAVE_DB = False


    kwargs = {}
    kwargs["network"] = args.net
    if not args.all:
        kwargs["endafter"] = UTCDateTime.now()
    if args.station:
        kwargs["station"] = args.station
    if args.channel:
        kwargs["channel"] = args.channel
    if args.location:
        kwargs["location"] = args.location
    if args.level:
        kwargs["level"] = args.level

    if args.verbose:
        print "Retrieving station information from {} webservice\n".format(args.webservice)
        print "Request parameters:\n"
        for key, value in kwargs.iteritems():
            print "\t{}={}".format(key,value)
        if HAVE_DB:
            print "Populating database {} on {}:{} as user {}\n".format(DB_NAME,DB_HOST,DB_PORT,DB_USER)
        else:
            print "Creating file load_metadata.sql\n"
    
    inventory = client.get_stations(**kwargs)
    inventory.write("inventory.xml", format="STATIONXML")

    if args.verbose:
        print inventory
        print len(inventory.networks)
        for network in inventory.networks:
            print len(network.stations)
            for station in network.stations:
                print len(station.channels)
                print station.__dict__
                for channel in station.channels:
                    print channel.response
                    print channel.__dict__

    statements = create_insert_statements(inventory) # returns tuple of unicode

    # clean up
    if HAVE_DB:
        cursor.close()
        db.close() 
    
