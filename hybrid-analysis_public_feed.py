#this code is terrible but good enough for poc.

import json
import csv

def process_list_gen(process_list_original):
    process_list = {}
    for process in process_list_original:
        process_list[process['uid']] = process
    return process_list

def analyze_report(report_id, process_list):
    try:
        for process in process_list:
            uid = process_list[process]['uid']
            name = process_list[process]['name']
            path = process_list[process]['normalizedpath']
            command = process_list[process]['commandline']
            if 'parentuid' in process_list[process].keys():
                parent_process = process_list[process_list[process]['parentuid']]
                parent_process_uid = parent_process['uid']
                parent_process_name = parent_process['name']
                parent_process_path = parent_process['normalizedpath']
                parent_process_command = parent_process['commandline']
                csvwriter.writerow([report_id, parent_process_uid, parent_process_name, parent_process_path, parent_process_command, uid, name, path, command])
            else:
                csvwriter.writerow([report_id, "NA", "NA", "NA", "NA", uid, name, path, command])
    except:
        pass

fileread = open("public_feed.json", 'r').read()
jsonout = json.loads(fileread)

process_data = open('process_data.csv','w',newline='')
csvwriter = csv.writer(process_data, delimiter='\t')
csvwriter.writerow("report_id, parent_uid, parent_name, parent_path, parent_command, uid, name, path, command".split(","))

for report in jsonout['data']:
    report_id = report['reporturl']
    process_list = process_list_gen(report['process_list'])
    analyze_report(report_id, process_list)

process_data.close()
