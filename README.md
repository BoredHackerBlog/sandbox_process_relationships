# sandbox_process_relationships

This repo contains some scripts that can take in CAPE sandbox task report or hybrid-analysis publicfeed json, extract process info, and store it into duckdb.

Duckdb database can queried via duckdb command line interface or python.

You can ask questions like:
- what process launched ping? `select parent_name, proc_commandline from joined_proc_list where proc_commandline ilike '%ping.exe%';`
- what process launched powershell with command line to add Defender exclusion? `select parent_name, proc_commandline from joined_proc_list where proc_commandline ilike '%add-mppreference%';`
- what processes launch wscript? `select parent_name, count(*) as count from joined_proc_list where proc_commandline ilike '%wscript%' group by parent_name`
- what does cmd.exe launch from the appdata folder? `select parent_name, proc_name from joined_proc_list where parent_name ilike '%cmd.exe%' AND proc_path ilike '%appdata%';`

obviously you can append report_id in your select statement so you get information about the actual sample responsible for the event.

# Blog:

https://www.boredhackerblog.info/2022/10/looking-at-process-relationships-from.html
