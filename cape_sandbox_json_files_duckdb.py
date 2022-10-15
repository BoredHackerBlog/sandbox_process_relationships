#download json files from CAPE sandbox and put them in the same directory as the script
#or
#use requests module to download json files from CAPE
#path: https://CAPE/apiv2/tasks/get/report/$task_id/json/

import json
import duckdb
import glob

con = duckdb.connect(database='process.duckdb')
#con = duckdb.connect(':memory:')
con.execute("create table processes(report_id varchar, pid varchar, ppid varchar, name varchar, path varchar, commandline varchar)")
con.execute("create view joined_proc_list as select p.report_id as report_id, pp.pid as parent_pid, pp.ppid as parent_ppid, pp.name as parent_name, pp.path as parent_path, pp.commandline as parent_commandline, p.pid as proc_pid, p.name as proc_name, p.path as proc_path, p.commandline as proc_commandline from processes p join processes pp on p.ppid = pp.pid AND p.report_id = pp.report_id")

files = glob.glob("*.json")
for jsonfile in files:
    with open(jsonfile, "r") as fileread:
        try:
            jsonout = json.loads(fileread.read())
            report_id = jsonout.get('info').get('id')
            for process in jsonout['behavior']['processes']:
                pid = process.get('process_id')
                ppid = process.get('parent_id')
                name = process.get('process_name')
                path = process.get('module_path')
                commandline = process.get('environ').get('CommandLine')
                con.execute("insert into processes values (?, ?, ?, ?, ?, ?)", [report_id, pid, ppid, name, path, commandline])
        except:
            pass

con.close()
