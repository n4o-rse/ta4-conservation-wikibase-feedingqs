__author__ = "Florian Thiery"
__copyright__ = "MIT Licence 2024, Florian Thiery, LEIZA"
__credits__ = ["Florian Thiery"]
__license__ = "MIT"
__version__ = "beta"
__maintainer__ = "Florian Thiery"
__email__ = "florian.thiery@leiza.de"
__status__ = "beta"
__update__ = "20234-04-22"

# import dependencies
import uuid
import requests
import io
import pandas as pd
import os
import codecs
import datetime
import importlib
import sys
import hashlib
from pathlib import Path  # for file management

# set UTF8 as default
importlib.reload(sys)

# set starttime
starttime = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ")
qs = []
lines = []

# set paths I
file_name = "wikibase.csv"
dir_path = os.path.dirname(os.path.realpath(__file__))

def get_project_root() -> Path:
    return Path(__file__).parent.parent

Path = get_project_root()

# joinpath used to join parts of the path together. Path as project root
file_in = Path.joinpath("csv").joinpath(file_name)
url = "https://docs.google.com/spreadsheets/d/1HKatD3XhOvcnF_c5t1pP9C9i_YuS6LPrHu2-q0C0asU/export?gid=0&format=csv"

# read csv file
data = pd.read_csv(
    url,
    encoding='utf-8',
    usecols=['identifier', 'prefLabel', 'description', 'type'],
    na_values=['.', '??', 'NULL']  # take any '.' or '??' values as NA
)
print("*****************************************")
print(data.info())

# create quickstatements from dataframe
lineNo = 2
tmp = ""
for index, row in data.iterrows():
    # tmpno = lineNo - 2
    # lineNo += 1
    qs.append("CREATE")
    tmp = "LAST" + "\t" + "Lde" + "\t" + "\"" + str(row['prefLabel']) + "\""
    qs.append(tmp)
    if str(row['description']) != 'nan':
        tmp = "LAST" + "\t" + "Dde" + "\t" + "\"" + str(row['description']) + "\""
    qs.append(tmp)
    tmp = "LAST" + "\t" + "Len" + "\t" + "\"" + str(row['prefLabel']) + "\""
    qs.append(tmp)
    if str(row['description']) != 'nan':
        tmp = "LAST" + "\t" + "Den" + "\t" + "\"" + str(row['description']) + "\""
    qs.append(tmp)
    tmp = "LAST" + "\t" + "P2" + "\t" + "Q2"
    qs.append(tmp)
    tmp = "LAST" + "\t" + "P4" + "\t" + "\"" + str(row['identifier']) + "\""
    qs.append(tmp)

    qs.append("")

# write output file
filename = dir_path.replace("\\py", "\\qs") + "\\" + "conservation_wikibase_init.qs"
file = codecs.open(filename, "w", "utf-8")
for i, line in enumerate(qs):
    file.write(line)
    file.write("\r\n")
print(" > conservation_wikibase_init.qs")
file.close()

print("*****************************************")
print("SUCCESS: closing script")
print("*****************************************")