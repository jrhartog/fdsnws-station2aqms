# fdsnws-station2aqms
Retrieve meta-data from a FDSN Station Web Service and populate basic AQMS meta-data tables.

# Installation
I recommend working with virtual environments. See  http://docs.python-guide.org/en/latest/dev/virtualenvs/
This script uses obspy, which needs numpy, matplotlib, scipy, and a bunch of 
other stuff. Numpy needs to be completely installed first.
Another option is to use a third-party distributor such as Anaconda ("conda").

1. `git clone https://github.com/jrhartog/fdsnws-station2aqms.git fdsnws-station2aqms`
2. `cd fdsnws-station2aqms`
3. `pip install numpy`
4. `pip install -r requirements.txt`

# Configuration
1. Edit the environment file to be appropriate for your database
2. `source environment` to create environment variables

The above procedure should have installed a very rudimentary script (`inventory2aqms`) that 
reads an "inventory.xml" file in the current working directory and tries to load it into 
the database defined by the environment variables listed in env.sh. Just like fdsnws-station2aqms, 
it will create the schema if it doesn't exist yet but not overwrite any existing tables. 
Feel free to try that, the included inventory.xml file contains meta-data for some UW, UO, or CC 
network stations.  The script leaves behind a verbose inventory2aqms.log file.

# Usage
  fdsnws-station2aqms -h

  usage: fdsnws-station2aqms [-h] [-f FILENAME] [-s STATION] [-c CHANNEL]
                             [-l LOCATION] [-a]
                             [-ws {BGR,EMSC,ETH,GEONET,GFZ,INGV,IPGP,IRIS,ISC,KOERI,LMU,NCEDC,NIEP,NOA,ODC,ORFEUS,RESIF,SCEDC,USGS,USP}]
                             [-level {station,channel,response}] [-v]
                             network
  
  Retrieves FDSN StationXML from a fdsn webservice (default=IRIS) and populates
  (PostgreSQL) AQMS tables station_data, channel_data, and simple_response.
  Database connection parameters have to be set with environment variables
  (see above). Alternatively it can be run with the -f flag to save the meta-data 
  to a StationXML file instead. Log messages are written to 
  fdsnws-station2aqms.log . 
  
  positional arguments:

    network               Specify a FDSN or Virtual network code, wildcards are
                          allowed
  
  optional arguments:

    -h, --help            show this help message and exit

    -f FILENAME, --filename FILENAME
                          Save the inventory to a file instead, provide filename

    -s STATION, --station STATION
                          Specify a station code, wildcards are allowed

    -c CHANNEL, --channel CHANNEL
                          Specify a channel code, wildcards are allowed

    -l LOCATION, --location LOCATION
                          Specify a location code, wildcards are allowed

    -a, --all             Request metadata for all times, default is active
                          channels only!

    -ws {BGR,EMSC,ETH,GEONET,GFZ,INGV,IPGP,IRIS,ISC,KOERI,LMU,NCEDC,NIEP,NOA,ODC,ORFEUS,RESIF,SCEDC,USGS,USP}, --webservice {BGR,EMSC,ETH,GEONET,GFZ,INGV,IPGP,IRIS,ISC,KOERI,LMU,NCEDC,NIEP,NOA,ODC,ORFEUS,RESIF,SCEDC,USGS,USP}
                          Specify Webservice to query (default=IRIS)

    -level {station,channel,response}, --level {station,channel,response}
                          Specify level of information (default=response)

    -v, --verbose         Be more verbose in logfile

