#feed here: https://www.hybrid-analysis.com/feed?json 
#be sure to use Chrome or Firefox user-agent when downloading via python or wget or curl. It seems like that's required, even though the feed is public

import json
import duckdb
import pprint
pp = pprint.PrettyPrinter(indent=4)

fileread = open("public_feed.json", 'r').read()
jsonout = json.loads(fileread)

#create a database
#con = duckdb.connect(database='process.duckdb')
con = duckdb.connect(':memory:')
con.execute("create table processes(report_id varchar, pid varchar, ppid varchar, name varchar, path varchar, commandline varchar)")

for report in jsonout['data']:
    report_id = report['reporturl']
    for process in report['process_list']:
        pid = process.get('uid')
        ppid = process.get('parentuid')
        name = process.get('name')
        path = process.get('normalizedpath')
        commandline = process.get('commandline')
        con.execute("insert into processes values (?, ?, ?, ?, ?, ?)", [report_id, pid, ppid, name, path, commandline])

#create a view        
con.execute("create view joined_proc_list as select p.report_id as report_id, pp.pid as parent_pid, pp.ppid as parent_ppid, pp.name as parent_name, pp.path as parent_path, pp.commandline as parent_commandline, p.pid as proc_pid, p.name as proc_name, p.path as proc_path, p.commandline as proc_commandline from processes p join processes pp on p.ppid = pp.pid AND p.report_id = pp.report_id")

#do your queries here
pp.pprint(con.execute("select * from joined_proc_list where parent_name ILIKE '%wscript%'").fetchall())
pp.pprint(con.execute("select parent_name from joined_proc_list where proc_name ILIKE '%iexplore%' group by parent_name").fetchall())
