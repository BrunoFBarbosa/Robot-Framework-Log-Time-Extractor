from __future__ import division
import os
import errno
import csv
import glob
from lxml import etree
import xml.etree.ElementTree as ET
import datetime
import collections

#time format from the logs
fmt = '%Y%m%d %H:%M:%S.%f'

#keyword type to exclude
kw_exclude = ["for", "foritem"]

#keyword specific name to exclude
kw_specific_name_exclude = ["Capture Page Screenshot", "Replace String"]
                            
#library to exclude
kw_library_exlude = ["BuiltIn", "String", "FakerLibrary", "DateTime"]

file_count = 0

data = {
    "suite": {},
    "test": {},
    "kw": {}
}

suite_dict = {}
data_extracted = {}


def extract(file):


    print("Starting parse for %s \n" % file)
    e = etree.iterparse(file, events=("end",), tag=("suite", "test", "kw"))

    for event, item in e:

        if 'name' in item.attrib:

            if item.tag == "kw":
                kw_name = item.get("name")
                if (item.get('type') and item.get('type') in kw_exclude) or kw_name in kw_specific_name_exclude or \
                        (item.get("library") and item.get("library") in kw_library_exlude) or \
                             "Setup" in item.get("name"):

                    continue
            if item.get("source") and ".robot" not in item.get("source"):
                continue
            else:

                if item.tag == "suite":
                    item_name = os.path.split(item.get("source"))[1]
                else:
                    item_name = item.get("name")

                status = item.find("status")
                starttime = status.get("starttime")
                endtime = status.get("endtime")
                d1 = datetime.datetime.strptime(starttime, fmt)
                d2 = datetime.datetime.strptime(endtime, fmt)
                timediff = (d2-d1).total_seconds()

                if item_name not in data[item.tag].keys():
                    if item.tag == "suite":
                        data[item.tag][item_name] = {}
                        data[item.tag][item_name]["test_count"] = len(item.findall("test"))
                        data[item.tag][item_name]["timing"] = []
                        data[item.tag][item_name]["timing"].append(timediff)

                    else:
                        data[item.tag][item_name] = []
                        data[item.tag][item_name].append(timediff)
                else:
                    if item.tag == "suite":
                        data[item.tag][item_name]["timing"].append(timediff)
                    else:
                        data[item.tag][item_name].append(timediff)

        item.clear()


    del e
    return data

def write_to_csv(dict_data, mode, number_of_files):

    save_path = './results/'

    if not os.path.exists(os.path.dirname(save_path)):
        try:
            os.makedirs(os.path.dirname(save_path))
        except OSError as exc:
            if exc.errno != errno.EEXIST:
                raise
    if mode == "kw":
        fieldnames = [mode.upper(), 'AVERAGE DURATION (S)', 'AVERAGE DURATION (M)', 'OCCURRENCES PER RUN', 'TOTAL TIME PER RUN (M)']
    elif mode == "suite":
        fieldnames = [mode.upper(), 'AVERAGE DURATION (S)', 'AVERAGE DURATION (M)', "NUMBER OF TEST CASES", "AVERAGE DURATION PER TEST"]
    else:
        fieldnames = [mode.upper(), 'AVERAGE DURATION (S)', 'AVERAGE DURATION (M)']


    with open(save_path+mode.lower()+'.csv', 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for item_key, item_value in dict_data.items():

            if mode == "suite":

                total_time = sum(item_value["timing"])
                total_time_per_run = total_time / number_of_files
                occurrences = len(item_value["timing"])
                avg = total_time / occurrences
                test_cases = item_value["test_count"]

                writer.writerow(
                    {mode.upper(): item_key.encode("utf-8"), 'AVERAGE DURATION (S)': format(avg, ".4f"),
                     'AVERAGE DURATION (M)': format(avg / 60, ".4f"), 'NUMBER OF TEST CASES': test_cases, "AVERAGE DURATION PER TEST": format((avg / 60 / test_cases), ".4f")})

            elif mode == "kw":
                total_time = sum(item_value)
                total_time_per_run = total_time / number_of_files
                occurrences = len(item_value)
                occurrences_per_run = occurrences / number_of_files
                avg = total_time / occurrences

                writer.writerow(
                    {mode.upper(): item_key.encode("utf-8"), 'AVERAGE DURATION (S)': format(avg, ".4f"),
                     'AVERAGE DURATION (M)': format(avg / 60, ".4f"), 'OCCURRENCES PER RUN': format(occurrences_per_run, ".4f"),
                     'TOTAL TIME PER RUN (M)': format(total_time_per_run / 60, ".4f")})
            else:
                total_time = sum(item_value)
                total_time_per_run = total_time / number_of_files
                occurrences = len(item_value)
                occurrences_per_run = occurrences / number_of_files
                avg = total_time / occurrences
                writer.writerow(
                    {mode.upper(): item_key.encode("utf-8"), 'AVERAGE DURATION (S)': format(avg, ".4f"),
                     'AVERAGE DURATION (M)': format(avg / 60, ".4f")})

        csvfile.close()


for filename in sorted(glob.glob('./runs/*.xml')):
    data = extract(filename)
    
    file_count += 1


for item in data.keys():
    print(data[item].items())
    write_to_csv(data[item], item, file_count)




