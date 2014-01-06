from datetime import date
from urllib import request
from urllib.error import HTTPError
import os

DIRECTORY = 'scratch'
AAT_PRE_URL = 'http://site.aao.gov.au/arc-bin/wdb_log/aat_database/log_book/query?night=%04i%02i%02i'
AAT_URL = 'http://site.aao.gov.au/AATdatabase/temp/log_%04i%02i%02i.txt'
AAT_FILENAME = 'log_aat_%04i%02i%02i.txt'

def get_aat_log(date_log, directory=DIRECTORY):
    """
    Save the log from a single AAT night.
    """
    pre_url = AAT_PRE_URL % (date_log.year, date_log.month, date_log.day)
    url = AAT_URL % (date_log.year, date_log.month, date_log.day)
    # Construct an opener that hides the fact this is a python script
    opener = request.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    # Have to open up the "pre" URL so that the server will generate the file
    # we actually want
    pre_page = opener.open(request.Request(pre_url))
    pre_page.read()
    pre_page.close()
    # Now we can grab the log file itself
    path_out = os.path.join(
        directory, 
        AAT_FILENAME % (date_log.year, date_log.month, date_log.day))
    try:
        with opener.open(request.Request(url)) as file_input:
            with open(path_out, 'wb') as file_output:
                file_output.write(file_input.read())
    except HTTPError:
        # Probably means there is no log for that night, for whatever reason
        pass
    return
