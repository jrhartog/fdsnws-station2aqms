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
1. Edit env.sh to be appropriate for your database
2. `source env.sh`

The above procedure should have installed a very rudimentary script (`inventory2aqms`) that 
reads an "inventory.xml" file in the current working directory and tries to load it into 
the database defined by the environment variables listed in env.sh. Just like fdsnws-station2aqms, 
it will create the schema if it doesn't exist yet but not overwrite any existing tables. 
Feel free to try that, the included inventory.xml file contains meta-data for the CC (CVO) network.
The script leaves behind a verbose inventory2aqms.log file.

fdsnws-station2aqms -h
