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
    usecols=['identifier', 'type', 'prefLabel', 'altLabel', 'translation', 'description', 'source', 'creator', 'closeMatch'],
    na_values=['.', '??', 'NULL']  # take any '.' or '??' values as NA
)
print("*****************************************")
print(data.info())

# create quickstatements from dataframe
lineNo = 2
tmp = ""
for index, row in data.iterrows():
    if str(row['prefLabel']) != 'nan':
        qs.append("CREATE")
        # identifier
        tmp = "LAST" + "\t" + "P4" + "\t" + "\"" + str(row['identifier']) + "\""
        qs.append(tmp)
        # type
        tmp = "LAST" + "\t" + "P2" + "\t" + str(row['type'])
        qs.append(tmp)
        # prefLabel
        tmp = "LAST" + "\t" + "Lde" + "\t" + "\"" + str(row['prefLabel']) + "\""
        qs.append(tmp)
        tmp = "LAST" + "\t" + "P21" + "\t" + "de:\"" + str(row['prefLabel']) + "\""
        # altLabel
        if str(row['altLabel']) != 'nan':
            al = str(row['altLabel'])
            als = al.split("|")
            for i in als:
                tmp = "LAST" + "\t" + "Ade" + "\t" + "\"" + i + "\""
                qs.append(tmp)
                tmp = "LAST" + "\t" + "P22" + "\t" + "de:\"" + i + "\""
                qs.append(tmp)
        # translatation
        if str(row['translation']) != 'nan':
            tr = str(row['translation'])
            trs = tr.split("|")
            for i in trs:
                tr1 = i
                tr1s = tr1.split("@")
                tmp = "LAST" + "\t" + "P23" + "\t" + tr1s[1] +  ":\"" + tr1s[0] + "\""
                qs.append(tmp)
        # description
        if str(row['description']) != 'nan':
            tmp = "LAST" + "\t" + "Dde" + "\t" + "\"" + str(row['description']) + "\""
            qs.append(tmp)
            tmp = "LAST" + "\t" + "P24" + "\t" + "de:\"" + str(row['description']) + "\""
            qs.append(tmp)
        # source
        if str(row['source']) != 'nan':
            tmp = "LAST" + "\t" + "P25" + "\t" + "\"" + str(row['source']) + "\""
            qs.append(tmp)
        # creator
        if str(row['creator']) != 'nan':
            cr = str(row['creator'])
            crs = cr.split("|")
            for i in crs:
                tmp = "LAST" + "\t" + "P20" + "\t" + i 
                qs.append(tmp)
        # closeMatch
        if str(row['closeMatch']) != 'nan':
            cm = str(row['closeMatch'])
            cms = cm.split("|")
            for i in cms:
                repo = "";
                if "getty" in i:
                    repo = "Q11"
                elif "wikidata" in i:
                    repo = "Q9"
                elif "wikipedia" in i:
                    repo = "Q10"
                else:
                    repo = ""
                tmp = "LAST" + "\t" + "P17" + "\t" + "\"" + i + "\"" + "\t" + "P18" + "\t" + "P13" + "\t" + "P19" + "\t" + repo
                qs.append(tmp)
        # new Item
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